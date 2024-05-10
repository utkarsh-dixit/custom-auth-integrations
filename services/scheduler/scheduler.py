import datetime
from abc import ABC, abstractmethod
from uuid import uuid4
from loguru import logger

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from apscheduler import events
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from .models.TaskModel import TaskModel, insert_job, update_job, delete_job
from .tasks.scheduler_tasks import SchedulerTask


SCHEDULER_TRIGGER_CRON = "cron"
SCHEDULER_TRIGGER_INTERVAL = "interval"


def parse_cron_pattern(cron_pattern: str):
    """
    Parses a cron pattern string into a dictionary that represents the cron schedule.
    cron_pattern (str): A string representing the cron pattern, e.g., "0 20 * * 1"
    Returns:
    dict: A dictionary with keys for year, month, day, week, day_of_week, hour, minute, second
    """
    # Split the cron pattern into its components
    minute, hour, day, month, day_of_week = cron_pattern.split()

    # Map cron pattern to dictionary
    cron_dict = {
        'month': month,
        'day': day,
        'week': '*',
        'day_of_week': day_of_week,
        'hour': hour,
        'minute': minute,
        'second': '0'
    }
    return cron_dict
class BaseScheduler(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def schedule(self, task:SchedulerTask, args=None, kwargs=None):
        """
        Schedule a new job.
        :param time: When the job should run
        :param task: SchedulerTask type, which will export the function to execute
        :param args: Positional arguments to pass to the job function
        :param kwargs: Keyword arguments to pass to the job function
        """
        pass

    @abstractmethod
    def remove_job(self, job_id):
        """
        Remove a scheduled job.
        :param job_id: ID of the job to remove
        """
        pass
    @abstractmethod
    def update_job(self, job_id):
        """
        update the schedule of a job
        """
        pass

class APScheduler(BaseScheduler):
    def __init__(self, conn_str):
        engine = create_engine(
            conn_str,
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        # Base = declarative_base()
        self.session = SessionLocal()
        jobstores = {
            'default': SQLAlchemyJobStore(engine=engine)
        }
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(5)
        }
        job_defaults = {
            'coalesce': False,
            'max_instances': 3
        }
        self.scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, logger=logger, job_defaults=job_defaults)
        self.scheduler.add_listener(self.on_error, events.EVENT_JOB_ERROR)
        self.scheduler.add_listener(self.on_executed, events.EVENT_JOB_EXECUTED)
        # self.scheduler.add_listener(self.on_max_instances, events.EVENT_JOB_MAX_INSTANCES)
        self.scheduler.add_listener(self.on_missed, events.EVENT_JOB_MISSED)

    def start(self):
        self.scheduler.start()

    def on_executed(self, event: events.JobExecutionEvent) -> None:
        job = self.scheduler.get_job(event.job_id)
        if job is None or job.id == 'container_inspection':
            return

        definition = job.kwargs
        exit_code, response_lines = event.retval
        response_lines = response_lines.decode().splitlines()

        logger.info(
            f'Command {definition} finished with exit code {exit_code}.',
        )
        if response_lines:
            logger.info("== BEGIN of captured stdout & stderr ==")
            for line in response_lines:
                logger.info(line)
            logger.info("== END of captured stdout & stderr ====")

    def on_error(self, event: events.JobExecutionEvent) -> None:
        definition = self.scheduler.get_job(event.job_id).kwargs
        logger.critical(
            f'An exception in scheduler job:'
        )
        logger.error(str(event.exception))

    def on_missed(self, event: events.JobExecutionEvent) -> None:
        definition = self.scheduler.get_job(event.job_id).kwargs
        logger.warning(
            f'Missed execution of {definition} at {event.scheduled_run_time}.'
        )

    def schedule(self, task:SchedulerTask, args=None, kwargs=None):
        job_id = str(uuid4())  # Generate a unique ID for the job
        webhook_url = kwargs.get("webhook_url")
        payload = kwargs.get("payload", {})
        client_id = kwargs.get("client_id")
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")
        cron_pattern = kwargs.get("cron_pattern")
        cron_args = parse_cron_pattern(cron_pattern)
        if not client_id or not webhook_url:
            raise Exception("client_id or webhook_url is empty")
        job_args = kwargs.get("job_args")
        # start a transaction
        try:
            with self.session.begin():
                next_run_time = datetime.datetime.now() + datetime.timedelta(seconds=160)
                # insert task-meta-data in `Task` table
                # this is a hack insert job in Task table first and then call scheduler.add_job()
                # apscheduler jobstore doesnt honor current session, and doesnt rollback the transaction
                insert_job(self.session, client_id, job_id, next_run_time, webhook_url, "new", cron_pattern)
                job = self.scheduler.add_job(
                    func=task.job_func,
                    trigger=SCHEDULER_TRIGGER_CRON,
                    start_date=start_date,
                    end_date=end_date,
                    id=job_id,
                    args=[job_args],
                    kwargs={"webhook_url": webhook_url, "payload": payload},
                    **cron_args,
                )
                self.session.commit()
        except Exception as e:
            # Rollback the transaction if any exception occurs
            self.session.rollback()
            logger.error(f"Failed to schedule job and insert into Task table with exception: {str(e)}")
            raise Exception("Failed to schedule job and insert into Task table with exception")
        return {"message": "Job scheduled successfully", "job_id": job_id}

    def remove_job(self, job_id):
        job = self.scheduler.remove_job(str(job_id))
        delete_job(self.session, job_id)

    def update_job(self, job_id, **schedule_args):
        job = self.scheduler.reschedule_job(job_id, trigger='interval', **schedule_args)
        update_job(self.session, job_id, next_run_time=job.next_run_time, job_state=str(job.trigger))
        logger.info(f"Job {job_id} updated in the scheduler and the database.")

