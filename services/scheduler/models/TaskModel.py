from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Session
from uuid import uuid4
from enum import Enum
from datetime import datetime


Base = declarative_base()

'''
These models and migrations are handled by app/hermes/prisma/migration 
'''

class TaskStatus(Enum):
    new = 'new'
    pending = 'pending'
    running = 'running'
    completed = 'completed'
    failed = 'failed'
    disabled = 'disabled'

def get_job_status(job_status:str)-> TaskStatus:
    job_status = job_status.lower()
    if job_status == "new":
        return TaskStatus.new
    if job_status == "pending":
        return TaskStatus.pending
    if job_status == "running":
        return TaskStatus.running
    if job_status == "completed":
        return TaskStatus.completed
    if job_status == "failed":
        return TaskStatus.failed
    if job_status == "disabled":
        return TaskStatus.disabled

class Client(Base):
    __tablename__ = 'Client'
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    api_key = Column(String, unique=True)
    webhook_url = Column(String)


class TaskModel(Base):
    __tablename__ = 'Task'
    TaskId = Column(String, primary_key=True, default=lambda: str(uuid4()), name="taskId")
    Schedule = Column(String(255), nullable=False, name="schedule")
    status = Column(SQLEnum(TaskStatus))
    NextRunTime = Column(DateTime, nullable=True, name="nextRunTime")
    LastRunTime = Column(DateTime, name="lastRunTime")
    IsActive = Column(Boolean, nullable=False, name="isActive", default=True)
    WebHookUrl = Column(String(255), nullable=False, name="webHookUrl")
    ClientId = Column(String, ForeignKey('Client.id'), name="clientId")

def insert_job(session: Session, client_id:str, job_id: str, next_run_time: DateTime, webhook_url:str, job_status: str, interval_in_sec:str):
    status = get_job_status(job_status)
    very_old_time = datetime(2000, 1, 1)
    new_job = TaskModel(TaskId=job_id, ClientId=client_id,
                        NextRunTime=next_run_time, status=status,
                        WebHookUrl=webhook_url, Schedule=interval_in_sec, LastRunTime=very_old_time)
    session.add(new_job)

def update_job(session: Session, job_id: str, **kwargs):
    job = session.query(TaskModel).filter(TaskModel.id == job_id).one()
    for key, value in kwargs.items():
        setattr(job, key, value)
    session.commit()

def delete_job(session: Session, job_id: str):
    '''
    marks the job is_active field as false --> soft delete
    '''
    update_job(session, job_id, {"isActive":False})