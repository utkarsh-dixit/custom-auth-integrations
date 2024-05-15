import requests
from pydantic import BaseModel, Field
from shared.composio_tools.lib import Action, Tool
from typing import Optional, Type

class SpecificAccountRequest(BaseModel):
    subdomain: str = Field(..., description="The subdomain of the account")

class SpecificAccountResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the request was successful")
    account_info: Optional[dict] = Field(..., description="The account information")

class GetSpecificAccountAction(Action):
    """
    Get Specific Account Action
    """
    @property
    def display_name(self) -> str:
        return "Get Specific Account"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return SpecificAccountRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return SpecificAccountResponse

    def execute(self, request: SpecificAccountRequest, authorisation_data: dict) -> SpecificAccountResponse:
        headers = authorisation_data["headers"]
        subdomain = request.subdomain
        url = f"https://www.workable.com/spi/v3/accounts/{subdomain}"
        account_response = requests.get(url, headers=headers)
        account = account_response.json()
        if account_response.status_code != 200:
            return SpecificAccountResponse (
                success=False,
                account_info=account
            )
        
        return SpecificAccountResponse (
            success=True,
            account_info=account
        )
    
class MembersListRequest(BaseModel):
    subdomain: str = Field(..., description="The subdomain of the account")
    limit: Optional[int] = Field(None, description="The number of members to return")
    since_id: Optional[int] = Field(None, description="Returns results with an ID greater than or equal to the specified ID.")
    max_id: Optional[int] = Field(None, description="Returns results with an ID less than or equal to the specified ID.")
    role: str = Field(None, description="Filters for members of the specified role. Can be simple, admin or reviewer.") 
    shortcode: str = Field(None, description="Filters for a specific job, only collaborators will be returned") 

class MembersListResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the request was successful")
    members: Optional[list] = Field(..., description="The members of the account")

class GetMembersListAction(Action):
    """
    Members List Action
    """
    @property
    def display_name(self) -> str:
        return "Members List"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return MembersListRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return MembersListResponse

    def execute(self, request: MembersListRequest, authorisation_data: dict) -> MembersListResponse:
        headers = authorisation_data["headers"]
        subdomain = request.subdomain
        limit = request.limit
        since_id = request.since_id
        max_id = request.max_id
        role = request.role
        shortcode = request.shortcode
        url = f"https://{subdomain}.workable.com/spi/v3/members"
        params = {
            "limit": limit,
            "since_id": since_id,
            "max_id": max_id,
            "role": role,
            "shortcode": shortcode
        }
        members_response = requests.get(url, headers=headers, params=params)
        if members_response.status_code != 200:
            return MembersListResponse (
                success=False,
                members=None
            )
        
        members = members_response.json()
        return MembersListResponse (
            success=True,
            members=members
        )
    
class ExternalRecruiterListRequest(BaseModel):
    subdomain: str = Field(..., description="The subdomain of the account")
    shortcode: str = Field(None, description="Filters for a specific job, only collaborators will be returned")

class ExternalRecruiterListResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the request was successful")
    external_recruiters: Optional[list] = Field(..., description="The external recruiters of the account")

class GetExternalRecruiterListAction(Action):
    """
    External Recruiter List Action
    """
    @property
    def display_name(self) -> str:
        return "External Recruiter List"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return ExternalRecruiterListRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return ExternalRecruiterListResponse

    def execute(self, request: ExternalRecruiterListRequest, authorisation_data: dict) -> ExternalRecruiterListResponse:
        headers = authorisation_data["headers"]
        subdomain = request.subdomain
        shortcode = request.shortcode
        url = f"https://{subdomain}.workable.com/spi/v3/recruiters"
        params = {
            "shortcode": shortcode
        }
        external_recruiters_response = requests.get(url, headers=headers, params=params)
        if external_recruiters_response.status_code != 200:
            return ExternalRecruiterListResponse (
                success=False,
                external_recruiters=None
            )
        
        external_recruiters = external_recruiters_response.json()
        return ExternalRecruiterListResponse (
            success=True,
            external_recruiters=external_recruiters
        )
    
class RequirementPipelineStageRequest(BaseModel):
    subdomain: str = Field(..., description="The subdomain of the account")
    
class RequirementPipelineStageResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the request was successful")
    pipeline_stages: dict = Field(..., description="The pipeline stages of the account")

class GetRequirementPipelineStageAction(Action):
    """
    Requirement Pipeline Stage Action
    """
    @property
    def display_name(self) -> str:
        return "Requirement Pipeline Stage"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return RequirementPipelineStageRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return RequirementPipelineStageResponse

    def execute(self, request: RequirementPipelineStageRequest, authorisation_data: dict) -> RequirementPipelineStageResponse:
        headers = authorisation_data["headers"]
        subdomain = request.subdomain
        url = f"https://{subdomain}.workable.com/spi/v3/stages"
        pipeline_stages_response = requests.get(url, headers=headers)
        pipeline_stages = pipeline_stages_response.json()
        if pipeline_stages_response.status_code != 200:
            return RequirementPipelineStageResponse (
                success=False,
                pipeline_stages=pipeline_stages
            )
        
        return RequirementPipelineStageResponse (
            success=True,
            pipeline_stages=pipeline_stages
        )
    
class AccountDepartmentRequest(BaseModel):
    subdomain: str = Field(..., description="The subdomain of the account")

class AccountDepartmentResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the request was successful")
    departments: Optional[list] = Field(..., description="The departments of the account")

class GetAccountDepartmentAction(Action):
    """
    Collection of your account departments
    """
    @property
    def display_name(self) -> str:
        return "Collection of your account departments"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return AccountDepartmentRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return AccountDepartmentResponse

    def execute(self, request: AccountDepartmentRequest, authorisation_data: dict) -> AccountDepartmentResponse:
        headers = authorisation_data["headers"]
        subdomain = request.subdomain
        url = f"https://{subdomain}.workable.com/spi/v3/departments"
        departments_response = requests.get(url, headers=headers)
        if departments_response.status_code != 200:
            return AccountDepartmentResponse (
                success=False,
                departments=None
            )
        
        departments = departments_response.json()
        return AccountDepartmentResponse (
            success=True,
            departments=departments
        )
    
class LegalEntitiesRequest(BaseModel):
    subdomain: str = Field(..., description="The subdomain of the account")

class LegalEntitiesResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the request was successful")
    legal_entities: Optional[list] = Field(..., description="The legal entities of the account")

class GetLegalEntitiesAction(Action):
    """
    Collection of your account legal entities
    """
    @property
    def display_name(self) -> str:
        return "Collection of your account legal entities"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return LegalEntitiesRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return LegalEntitiesResponse

    def execute(self, request: LegalEntitiesRequest, authorisation_data: dict) -> LegalEntitiesResponse:
        headers = authorisation_data["headers"]
        subdomain = request.subdomain
        url = f"https://{subdomain}.workable.com/spi/v3/legal_entities"
        legal_entities_response = requests.get(url, headers=headers)
        if legal_entities_response.status_code != 200:
            return LegalEntitiesResponse (
                success=False,
                legal_entities=None
            )
        
        legal_entities = legal_entities_response.json()
        return LegalEntitiesResponse (
            success=True,
            legal_entities=legal_entities
        )
    


class WorkableAccountAccessRequest(BaseModel):
    pass

class WorkableAccountAccessResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the request was successful")
    account_data: Optional[dict] = Field(..., description="The account data")

class WorkableAccountAccessAction(Action):
    """
    Workable Account Access Action
    """
    @property
    def display_name(self) -> str:
        return "Workable Account Access"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return WorkableAccountAccessRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return WorkableAccountAccessResponse

    def execute(self, request: WorkableAccountAccessRequest, authorisation_data: dict) -> WorkableAccountAccessResponse:
        headers = authorisation_data["headers"]
        url = "https://www.workable.com/spi/v3/accounts"
        account_response = requests.get(url, headers=headers)
        if account_response.status_code != 200:
            return WorkableAccountAccessResponse (
                success=False,
                account_data=None
            )
        
        account = account_response.json()
        return WorkableAccountAccessResponse (
            success=True,
            account_data=account
        )
        

class Workable(Tool):
    def actions(self) -> list:
        return [
            WorkableAccountAccessAction,
            GetSpecificAccountAction,
            GetMembersListAction,
            GetExternalRecruiterListAction,
            GetRequirementPipelineStageAction,
            GetAccountDepartmentAction,
            GetLegalEntitiesAction
        ]
    
    def triggers(self) -> list:
        return []
    
__all__ = ["Workable"]