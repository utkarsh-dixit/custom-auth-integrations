from abc import ABC, abstractmethod
import requests
from requests.exceptions import HTTPError, RequestException
from time import sleep
from loguru import logger


KEY_WEBHOOK_URL = "webhook_url"
KEY_PAYLOAD = "payload"
KEY_RETRY = "retry"
KEY_BACKOFF = "backoff"

class SchedulerTask(ABC):
    @abstractmethod
    def job_func(self, args, **kwargs):
        pass

class CallWebHook(SchedulerTask):
    def job_func(self, args, **kwargs):
        if not kwargs.get(KEY_WEBHOOK_URL):
            raise Exception("webhook url not given")
        try:
            url = kwargs.get(KEY_WEBHOOK_URL)
            payload = kwargs.get(KEY_PAYLOAD, {})
            retries = kwargs.get(KEY_RETRY, 3)
            backoff = kwargs.get(KEY_BACKOFF, 2)
            response = self.call_webhook_with_retries(url, payload, retries, backoff)
        except Exception as e:
            raise Exception(e)

    def call_webhook_with_retries(self, url, payload, retries=3, backoff_factor=2):
        attempt = 0
        while attempt < retries:
            try:
                logger.info(f"Attempt {attempt + 1} of {retries}")
                response = requests.post(url, json=payload)
                response.raise_for_status()
                return response.json()
            except HTTPError as http_err:
                logger.info(f"HTTP error occurred: {http_err}")  # Specific HTTP related errors
                if response.status_code < 500:
                    # Do not retry for client-side errors
                    break
            except RequestException as req_err:
                logger.info(f"Other request error occurred: {req_err}")  # Other request issues like network failures
            attempt += 1
            sleep(backoff_factor ** attempt)  # Exponential backoff
        return None
