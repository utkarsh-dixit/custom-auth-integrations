import requests
from pydantic import BaseModel, Field
from composio_tools import Action, Tool
from typing import Optional
import requests
import base64
import json


class HerokuAppInfoRequest(BaseModel):
    app_id: str = Field(..., description="The unique identifier for the Heroku app.")

class HerokuAppInfoResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the app information retrieval was successful.")
    app_info: dict = Field(..., description="The full response data returned by the Heroku API.")


class GetHerokuAppInfo(Action):
    """
    Get Heroku App Information
    """
    @property
    def display_name(self) -> str:
        return "Get Heroku App Information"

    @property
    def request_schema(self) -> BaseModel:
        return HerokuAppInfoRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return HerokuAppInfoResponse
    
    def execute(self, authorisation_data: dict, request: HerokuAppInfoRequest) -> HerokuAppInfoResponse:
        headers = authorisation_data["headers"]
        app_id = request.app_id
        app_info_url = f"https://api.heroku.com/apps/{app_id}"

        # Get app information
        app_info_response = requests.get(app_info_url, headers=headers)
        if app_info_response.status_code != 200:
            return HerokuAppInfoResponse(success=False, app_info=app_info_response.json())

        return HerokuAppInfoResponse(
            success=True,
            app_info=app_info_response.json()
        )


class HerokuTool(Tool):
    """
    Connect to Heroku
    """
    def actions(self) -> list:
        return [
            GetHerokuAppInfo,
        ]

    def triggers(self) -> list:
        return []

__all__ = ["HerokuTool"]
