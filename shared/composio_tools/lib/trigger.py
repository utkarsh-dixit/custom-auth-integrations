from pydantic import BaseModel
from abc import ABC, abstractmethod

class AlreadyExistsError(Exception):
    pass

class Trigger(BaseModel, ABC):
    _display_name: str = ""  # Add an internal variable to hold the display name
    _payload_schema: BaseModel = None  # Placeholder for payload schema
    _trigger_config_schema: BaseModel = None  # Placeholder for trigger config
    _trigger_instructions: str = ""  # Placeholder for trigger instructions

    @property
    def display_name(self) -> str:
        return self._display_name

    @display_name.setter
    def display_name(self, value: str):
        self._display_name = value  # Set the internal variable

    @property
    def payload_schema(self) -> BaseModel:
        return self._payload_schema

    @payload_schema.setter
    def payload_schema(self, value: BaseModel):
        self._payload_schema = value  # Set the internal variable

    @property
    def trigger_config_schema(self) -> BaseModel:
        return self._trigger_config_schema
    
    @trigger_config_schema.setter
    def trigger_config_schema(self, value: BaseModel):
        self._trigger_config_schema = value  # Set the internal variable

    @property
    def trigger_instructions(self) -> str:
        return self._trigger_instructions
    
    @trigger_instructions.setter
    def trigger_instructions(self, value: str):
        self._trigger_instructions = value  # Set the internal variable

    @abstractmethod
    def check_and_convert_to_identifier_payload_schema(self, data: dict) -> (bool, str, _payload_schema):
        pass
    
    @abstractmethod
    def set_webhook_url(self, authorisation_data: dict, webhook_url_to_set: str, req: _trigger_config_schema) -> str:
        pass
