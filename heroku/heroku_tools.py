import requests
from pydantic import BaseModel, Field
from composio_tools import Action, Tool
from typing import Optional
import requests
import base64
import json

# Actions of Heroku Apps
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

        app_info_response = requests.get(app_info_url, headers=headers)
        if app_info_response.status_code != 200:
            return HerokuAppInfoResponse(success=False, app_info=app_info_response.json())

        return HerokuAppInfoResponse(
            success=True,
            app_info=app_info_response.json()
        )
    
class CreateHerokuAppRequest(BaseModel):
    app_name: str = Field(..., description="The name of the Heroku app to be created.")
    region: str = Field(..., description="The region where the Heroku app will be deployed.")
    stack: str = Field(..., description="The stack to be used for the Heroku app.")
    organization: Optional[str] = Field(None, description="The organization to which the Heroku app will belong.")
    space: Optional[str] = Field(None, description="The space where the Heroku app will be deployed.")
    team: Optional[str] = Field(None, description="The team that will own the Heroku app.")
    personal: Optional[bool] = Field(None, description="Indicates whether the Heroku app is personal.")

class CreateHerokuAppResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the app creation was successful.")
    app_info: dict = Field(..., description="The full response data returned by the Heroku API.")

class CreateHerokuApp(Action):
    """
    Create Heroku App
    """
    @property
    def display_name(self) -> str:
        return "Create Heroku App"

    @property
    def request_schema(self) -> BaseModel:
        return CreateHerokuAppRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return CreateHerokuAppResponse
    
    def execute(self, authorisation_data: dict, request: CreateHerokuAppRequest) -> CreateHerokuAppResponse:
        headers = authorisation_data["headers"]
        create_app_url = "https://api.heroku.com/apps"
        app_data = {
            "name": request.app_name,
            "region": request.region,
            "stack": request.stack
        }

        if request.organization:
            app_data["organization"] = request.organization
        if request.space:
            app_data["space"] = request.space
        if request.team:
            app_data["team"] = request.team
        if request.personal:
            app_data["personal"] = request.personal

        create_app_response = requests.post(create_app_url, headers=headers, data=json.dumps(app_data))
        if create_app_response.status_code != 201:
            return CreateHerokuAppResponse(success=False, app_info=create_app_response.json())

        return CreateHerokuAppResponse(
            success=True,
            app_info=create_app_response.json()
        )

class GetHerokuAppListRequest(BaseModel):
    pass

class GetHerokuAppListResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the app list retrieval was successful.")
    app_list: list = Field(..., description="The full response data returned by the Heroku API.")

class GetHerokuAppList(Action):
    """
    Get Heroku App List
    """
    @property
    def display_name(self) -> str:
        return "Get Heroku App List"

    @property
    def request_schema(self) -> BaseModel:
        return GetHerokuAppListRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return GetHerokuAppListResponse
    
    def execute(self, authorisation_data: dict, request: GetHerokuAppListRequest) -> GetHerokuAppListResponse:
        headers = authorisation_data["headers"]
        app_list_url = "https://api.heroku.com/apps"

        app_list_response = requests.get(app_list_url, headers=headers)
        if app_list_response.status_code != 200:
            return GetHerokuAppListResponse(success=False, app_list=app_list_response.json())

        return GetHerokuAppListResponse(
            success=True,
            app_list=app_list_response.json()
        )

class DeleteHerokuAppRequest(BaseModel):
    app_id: str = Field(..., description="The unique identifier for the Heroku app to be deleted.")

class DeleteHerokuAppResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the app deletion was successful.")
    message: str = Field(..., description="The message returned by the Heroku API.")

class DeleteHerokuApp(Action):
    """
    Delete Heroku App
    """
    @property
    def display_name(self) -> str:
        return "Delete Heroku App"

    @property
    def request_schema(self) -> BaseModel:
        return DeleteHerokuAppRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return DeleteHerokuAppResponse
    
    def execute(self, authorisation_data: dict, request: DeleteHerokuAppRequest) -> DeleteHerokuAppResponse:
        headers = authorisation_data["headers"]
        app_id = request.app_id
        delete_app_url = f"https://api.heroku.com/apps/{app_id}"

        delete_app_response = requests.delete(delete_app_url, headers=headers)
        if delete_app_response.status_code != 200:
            return DeleteHerokuAppResponse(success=False, message=json.dumps(delete_app_response.json()))

        return DeleteHerokuAppResponse(
            success=True,
            message=delete_app_response.json()
        )

# Actions related to account information

class GetAccountInfoRequest(BaseModel): 
    pass

class GetAccountInfoResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the account information retrieval was successful.")
    account_info: dict = Field(..., description="The full response data returned by the Heroku API.")

class GetAccountInfo(Action):
    """
    Get Heroku Account Information
    """
    @property
    def display_name(self) -> str:
        return "Get Heroku Account Information"

    @property
    def request_schema(self) -> BaseModel:
        return GetAccountInfoRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return GetAccountInfoResponse
    
    def execute(self, authorisation_data: dict, request: GetAccountInfoRequest) -> GetAccountInfoResponse:
        headers = authorisation_data["headers"]
        account_info_url = "https://api.heroku.com/account"

        account_info_response = requests.get(account_info_url, headers=headers)
        if account_info_response.status_code != 200:
            return GetAccountInfoResponse(success=False, account_info=account_info_response.json())

        return GetAccountInfoResponse(
            success=True,
            account_info=account_info_response.json()
        )

class UpdateAccountInfoRequest(BaseModel):
    allow_tracking: Optional[bool] = Field(None, description="Indicates whether tracking is allowed.")
    beta: Optional[bool] = Field(None, description="Indicates whether beta features are enabled.")
    name: Optional[str] = Field(None, description="The name of the account.")

class UpdateAccountInfoResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the account information update was successful.")
    account_info: dict = Field(..., description="The full response data returned by the Heroku API.")

class UpdateAccountInfo(Action):
    """
    Update Heroku Account Information
    """
    @property
    def display_name(self) -> str:
        return "Update Heroku Account Information"

    @property
    def request_schema(self) -> BaseModel:
        return UpdateAccountInfoRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return UpdateAccountInfoResponse
    
    def execute(self, authorisation_data: dict, request: UpdateAccountInfoRequest) -> UpdateAccountInfoResponse:
        headers = authorisation_data["headers"]
        update_account_info_url = "https://api.heroku.com/account"

        account_data = {}
        if request.allow_tracking:
            account_data["allow_tracking"] = request.allow_tracking
        if request.beta:
            account_data["beta"] = request.beta
        if request.name:
            account_data["name"] = request.name

        update_account_info_response = requests.patch(update_account_info_url, headers=headers, data=json.dumps(account_data))
        if update_account_info_response.status_code != 200:
            return UpdateAccountInfoResponse(success=False, account_info=update_account_info_response.json())

        return UpdateAccountInfoResponse(
            success=True,
            account_info=update_account_info_response.json()
        )
    
class AccountDelinquencyInfoRequest(BaseModel):
    pass

class AccountDelinquencyInfoResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the account delinquency information retrieval was successful.")
    delinquency_info: dict = Field(..., description="The full response data returned by the Heroku API.")

class GetAccountDelinquencyInfo(Action):
    """
    Get Heroku Account Delinquency Information
    """
    @property
    def display_name(self) -> str:
        return "Get Heroku Account Delinquency Information"

    @property
    def request_schema(self) -> BaseModel:
        return AccountDelinquencyInfoRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return AccountDelinquencyInfoResponse
    
    def execute(self, authorisation_data: dict, request: AccountDelinquencyInfoRequest) -> AccountDelinquencyInfoResponse:
        headers = authorisation_data["headers"]
        delinquency_info_url = "https://api.heroku.com/account/delinquency"

        delinquency_info_response = requests.get(delinquency_info_url, headers=headers)
        if delinquency_info_response.status_code != 200:
            return AccountDelinquencyInfoResponse(success=False, delinquency_info=delinquency_info_response.json())

        return AccountDelinquencyInfoResponse(
            success=True,
            delinquency_info=delinquency_info_response.json()
        )

# GET /account/features/{account_feature_id_or_name}
class AccountFeatureInfoRequest(BaseModel):
    account_feature_id_or_name: str = Field(..., description="The unique identifier or name of the account feature.")

class AccountFeatureInfoResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the account feature information retrieval was successful.")
    feature_info: dict = Field(..., description="The full response data returned by the Heroku API.")

class GetAccountFeatureInfo(Action):
    """
    Get Heroku Account Feature Information
    """
    @property
    def display_name(self) -> str:
        return "Get Heroku Account Feature Information"

    @property
    def request_schema(self) -> BaseModel:
        return AccountFeatureInfoRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return AccountFeatureInfoResponse
    
    def execute(self, authorisation_data: dict, request: AccountFeatureInfoRequest) -> AccountFeatureInfoResponse:
        headers = authorisation_data["headers"]
        feature_id_or_name = request.account_feature_id_or_name
        feature_info_url = f"https://api.heroku.com/account/features/{feature_id_or_name}"

        feature_info_response = requests.get(feature_info_url, headers=headers)
        if feature_info_response.status_code != 200:
            return AccountFeatureInfoResponse(success=False, feature_info=feature_info_response.json())

        return AccountFeatureInfoResponse(
            success=True,
            feature_info=feature_info_response.json()
        )
    
class AccountFeatureListRequest(BaseModel):
    pass

class AccountFeatureListResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the account feature list retrieval was successful.")
    feature_list: list = Field(..., description="The full response data returned by the Heroku API.")

class GetAccountFeatureList(Action):
    """
    Get Heroku Account Feature List
    """
    @property
    def display_name(self) -> str:
        return "Get Heroku Account Feature List"

    @property
    def request_schema(self) -> BaseModel:
        return AccountFeatureListRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return AccountFeatureListResponse
    
    def execute(self, authorisation_data: dict, request: AccountFeatureListRequest) -> AccountFeatureListResponse:
        headers = authorisation_data["headers"]
        feature_list_url = "https://api.heroku.com/account/features"

        feature_list_response = requests.get(feature_list_url, headers=headers)
        if feature_list_response.status_code != 200:
            return AccountFeatureListResponse(success=False, feature_list=feature_list_response.json())

        return AccountFeatureListResponse(
            success=True,
            feature_list=feature_list_response.json()
        )
    
class AccountFeatureUpdateRequest(BaseModel):
    account_feature_id_or_name: str = Field(..., description="The unique identifier or name of the account feature.")
    enabled: bool = Field(..., description="Indicates whether the account feature is enabled.")

class AccountFeatureUpdateResponse(BaseModel):
    success: bool = Field(..., description="Indicates whether the account feature update was successful.")
    feature_info: dict = Field(..., description="The full response data returned by the Heroku API.")

class UpdateAccountFeature(Action):
    """
    Update Heroku Account Feature
    """
    @property
    def display_name(self) -> str:
        return "Update Heroku Account Feature"

    @property
    def request_schema(self) -> BaseModel:
        return AccountFeatureUpdateRequest
    
    @property
    def response_schema(self) -> BaseModel:
        return AccountFeatureUpdateResponse
    
    def execute(self, authorisation_data: dict, request: AccountFeatureUpdateRequest) -> AccountFeatureUpdateResponse:
        headers = authorisation_data["headers"]
        feature_id_or_name = request.account_feature_id_or_name
        update_feature_url = f"https://api.heroku.com/account/features/{feature_id_or_name}"

        feature_data = {
            "enabled": request.enabled
        }

        update_feature_response = requests.patch(update_feature_url, headers=headers, data=json.dumps(feature_data))
        if update_feature_response.status_code != 200:
            return AccountFeatureUpdateResponse(success=False, feature_info=update_feature_response.json())

        return AccountFeatureUpdateResponse(
            success=True,
            feature_info=update_feature_response.json()
        )

# Heroku Tools
class HerokuTool(Tool):
    """
    Connect to Heroku
    """
    def actions(self) -> list:
        return [
            GetHerokuAppInfo,
            GetAccountInfo,
            GetHerokuAppList,
            CreateHerokuApp,
            DeleteHerokuApp,
            UpdateAccountInfo,
            GetAccountDelinquencyInfo,
            GetAccountFeatureInfo,
            GetAccountFeatureList,
            UpdateAccountFeature
        ]

    def triggers(self) -> list:
        return []

__all__ = ["HerokuTool"]