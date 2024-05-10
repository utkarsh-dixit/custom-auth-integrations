from pydantic import BaseModel
from typing import List
from abc import ABC, abstractmethod

class Action(ABC):
    _display_name: str = ""  # Add an internal variable to hold the display name
    _request_schema: BaseModel = None  # Placeholder for request schema
    _response_schema: BaseModel = None  # Placeholder for response schema
    _tags: List[str] = None
    
    @property
    def display_name(self) -> str:
        return self._display_name

    @display_name.setter
    def display_name(self, value: str):
        self._display_name = value  # Set the internal variable
        
    @property
    def tags(self) -> List[str]:
        return self._tags

    @tags.setter
    def tags(self, value: List[str]):
        self._tags = value  # Set the internal variable
        
    @property
    def request_schema(self) -> BaseModel:
        return self._request_schema

    @request_schema.setter
    def request_schema(self, value: BaseModel):
        self._request_schema = value

    @property
    def response_schema(self) -> BaseModel:
        return self._response_schema
    
    @response_schema.setter
    def response_schema(self, value: BaseModel):
        self._response_schema = value

    @abstractmethod
    def execute(self, request_data: _request_schema, authorisation_data: dict) -> dict:
        pass
    
    @property
    def required_scopes(self) -> List[str]:
        return []
