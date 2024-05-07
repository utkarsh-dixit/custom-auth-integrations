# from pydantic import BaseModel, Field
# from composio_tools import Action, Tool
# import base64
# import json
# import requests

# from typing import Optional, List, Dict

# class Get

# class HerokuTool(Tool):
#     """
#     Tool for interacting with the Heroku API.
#     """
#     def actions(self) -> list:
#         return [
#             self.list_apps,
#             self.create_app,
#             self.delete_app,
#             self.list_builds,
#             self.create_build,
#             self.get_build,
#             self.get_build_log,
#             self.list_releases,
#             self.create_release,
#             self.rollback_release,
#             self.list_dynos,
#             self.restart_dyno,
#             self.list_config_vars,
#             self.set_config_vars,
#             self.get_config_var,
#             self.delete_config_var,
#             self.list_addons,
#             self.create_addon,
#             self.get_addon,
#             self.delete_addon,
#             self.list_addon_attachments,
#             self.create_addon_attachment,
#             self.get_addon_attachment,
#             self.delete_addon_attachment,
#             self.list_collaborators,
#             self.add_collaborator,
#             self.get_collaborator,
#             self.remove_collaborator,
#             self.list_domains,
#             self.create_domain,
#             self.get_domain,
#             self.delete_domain,
#             self.list_features,
#             self.get_feature,
#             self.update_feature,
#             self.list_keys,
#             self.create_key,
#             self.get_key,
#             self.delete_key,
#             self.list_regions,
#             self.get_region,
#             self.list_stack,
#             self.get_stack,
#             self.list_account_features,
#             self.get_account_feature,
#             self.update_account_feature,
#             self.list_account_keys,
#             self.create_account_key,
#             self.get_account_key,
#             self.delete_account_key,
#             self.list_account_regions,
#             self.get_account_region,
#             self.list_account_stack,
#             self.get_account_stack,
#             self.list_account_apps,
#             self.get_account_app,
#             self.update_account_app,
#             self.delete_account_app,
#             self.list_account_builds,
#             self.get_account_build,
#             self.list_account_features,
#             self.get_account_feature,
#             self.update_account_feature,
#             self.list_account_keys,
#             self.create_account_key,
#             self.get_account_key,
#             self.delete_account_key,
#             self.list_account_regions,
#             self.get_account_region,
#             self.list_account_stack,
#         ]
#     def triggers(self) -> list:
#         return []
    
#     # def __init__(self, name: str, token: str):
#     #     self.name = name
#     #     self.token = token
#     #     self.headers = {
#     #         'Accept': 'application/vnd.heroku+json; version=3',
#     #         'Authorization': f'Bearer {self.token}'
#     #     }
#     #     self.url = 'https://api.heroku.com'
#     #     self.actions = {
#     #         'list_apps': Action('GET', '/apps', self.list_apps),
#     #         'create_app': Action('POST', '/apps', self.create_app),
#     #         'delete_app': Action('DELETE', '/apps/{app_id}', self.delete_app),
#     #         'list_builds': Action('GET', '/apps/{app_id}/builds', self.list_builds),
#     #         'create_build': Action('POST', '/apps/{app_id}/builds', self.create_build),
#     #         'get_build': Action('GET', '/apps/{app_id}/builds/{build_id}', self.get_build),
#     #         'get_build_log': Action('GET', '/apps/{app_id}/builds/{build_id}/log', self.get_build_log),
#     #         'list_releases': Action('GET', '/apps/{app_id}/releases', self.list_releases),
#     #         'create_release': Action('POST', '/apps/{app_id}/releases', self.create_release),
#     #         'get_release': Action('GET', '/apps/{app_id}/releases/{release_id}', self.get_release),
#     #         'rollback_release': Action('POST', '/apps/{app_id}/releases/{release_id}/rollback', self.rollback_release),
#     #         'list_dynos': Action('GET', '/apps/{app_id}/dynos', self.list_dynos),
#     #         'restart_dyno': Action('DELETE', '/apps/{app_id}/dynos/{dyno_id}', self.restart_dyno),
#     #         'list_config_vars': Action('GET', '/apps/{app_id}/config-vars', self.list_config_vars),
#     #         'set_config_vars': Action('PATCH', '/apps/{app_id}/config-vars', self.set_config_vars),
#     #         'get_config_var': Action('GET', '/apps/{app_id}/config-vars/{key}', self.get_config_var),
#     #         'delete_config_var': Action('DELETE', '/apps/{app_id}/config-vars/{key}', self.delete_config_var),
#     #         'list_addons': Action('GET', '/apps/{app_id}/addons', self.list_addons),
#     #         'create_addon': Action('POST', '/apps/{app_id}/addons', self.create_addon),
#     #         'get_addon': Action('GET', '/apps/{app_id}/addons/{addon_id}', self.get_addon),
#     #         'delete_addon': Action('DELETE', '/apps/{app_id}/addons/{addon_id}', self.delete_addon),
#     #         'list_addon_attachments': Action('GET', '/apps/{app_id}/addon-attachments', self.list_addon_attachments),
#     #         'create_addon_attachment': Action('POST', '/apps/{app_id}/addon-attachments', self.create_addon_attachment),
#     #         'get_addon_attachment': Action('GET', '/apps/{app_id}/addon-attachments/{addon_attachment_id}', self.get_addon_attachment),
#     #         'delete_addon_attachment': Action('DELETE', '/apps/{app_id}/addon-attachments/{addon_attachment_id}', self.delete_addon_attachment),
#     #         'list_collaborators': Action('GET', '/apps/{app_id}/collaborators', self.list_collaborators),
#     #         'add_collaborator': Action('POST', '/apps/{app_id}/collaborators', self.add_collaborator),
#     #         'get_collaborator': Action('GET', '/apps/{app_id}/collaborators/{collaborator_id}', self.get_collaborator),
#     #         'remove_collaborator': Action('DELETE', '/apps/{app_id}/collaborators/{collaborator_id}', self.remove_collaborator),
#     #         'list_domains': Action('GET', '/apps/{app_id}/domains', self.list_domains),
#     #         'create_domain': Action('POST', '/apps/{app_id}/domains', self.create_domain),
#     #         'get_domain': Action('GET', '/apps/{app_id}/domains/{domain_id}', self.get_domain),
#     #         'delete_domain': Action('DELETE', '/apps/{app_id}/domains/{domain_id}', self.delete_domain),
#     #         'list_features': Action('GET', '/account/features', self.list_features),
#     #         'get_feature': Action('GET', '/account/features/{feature_id}', self.get_feature),
#     #         'update_feature': Action('PATCH', '/account/features/{feature_id}', self.update_feature),
#     #         'list_keys': Action('GET', '/account/keys', self.list_keys),
#     #         'create_key': Action('POST', '/account/keys', self.create_key),
#     #         'get_key': Action('GET', '/account/keys/{key_id}', self.get_key),
#     #         'delete_key': Action('DELETE', '/account/keys/{key_id}', self.delete_key),
#     #         'list_regions': Action('GET', '/regions', self.list_regions),
#     #         'get_region': Action('GET', '/regions/{region_id}', self.get_region),
#     #         'list_stack': Action('GET', '/stacks', self.list_stack),
#     #         'get_stack': Action('GET', '/stacks/{stack_id}', self.get_stack),
#     #         'list_account_features': Action('GET', '/account/features', self.list_account_features),
#     #         'get_account_feature': Action('GET', '/account/features/{feature_id}', self.get_account_feature),
#     #         'update_account_feature': Action('PATCH', '/account/features/{feature_id}', self.update_account_feature),
#     #         'list_account_keys': Action('GET', '/account/keys', self.list_account_keys),
#     #         'create_account_key': Action('POST', '/account/keys', self.create_account_key),
#     #         'get_account_key': Action('GET', '/account/keys/{key_id}', self.get_account_key),
#     #         'delete_account_key': Action('DELETE', '/account/keys/{key_id}', self.delete_account_key),
#     #         'list_account_regions': Action('GET', '/account/regions', self.list_account_regions),
#     #         'get_account_region': Action('GET', '/account/regions/{region_id}', self.get_account_region),
#     #         'list_account_stack': Action('GET', '/account/stacks', self.list_account_stack),
#     #         'get_account_stack': Action('GET', '/account/stacks/{stack_id}', self.get_account_stack),
#     #         'list_account_apps': Action('GET', '/account/apps', self.list_account_apps),
#     #         'get_account_app': Action('GET', '/account/apps/{app_id}', self.get_account_app),
#     #         'update_account_app': Action('PATCH', '/account/apps/{app_id}', self.update_account_app),
#     #         'delete_account_app': Action('DELETE', '/account/apps/{app_id}', self.delete_account_app),
#     #         'list_account_builds': Action('GET', '/account/builds', self.list_account_builds),
#     #         'get_account_build': Action('GET', '/account/builds/{build_id}', self.get_account_build),
#     #         'list_account_features': Action('GET', '/account/features', self.list_account_features),
#     #         'get_account_feature': Action('GET', '/account/features/{feature_id}', self.get_account_feature),
#     #         'update_account_feature': Action('PATCH', '/account/features/{feature_id}', self.update_account_feature),
#     #         'list_account_keys': Action('GET', '/account/keys', self.list_account_keys),
#     #         'create_account_key': Action('POST', '/account/keys', self.create_account_key),
#     #         'get_account_key': Action('GET', '/account/keys/{key_id}', self.get_account_key),
#     #         'delete_account_key': Action('DELETE', '/account/keys/{key_id}', self.delete_account_key),
#     #         'list_account_regions': Action('GET', '/account/regions', self.list_account_regions),
#     #         'get_account_region': Action('GET', '/account/regions/{region_id}', self.get_account_region),
#     #         'list_account_stack': Action('GET', '/account/stacks', self.list_account_stack),

#     #     }   

# __all__ = ["HerokuTool"]

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

def test_heroku_actions():
    # Heroku API token
    heroku_api_token = "3bc29419-837a-4cd6-901c-e39f798f4ee6"
    
    # Mock authorization data
    authorization_data = {
        "headers": {
            "Accept": "application/vnd.heroku+json; version=3",
            "Authorization": f"Bearer {heroku_api_token}"
            # Add other headers as needed
        }
    }

    # Create an instance of the HerokuTool
    heroku_tool = HerokuTool()

    # Instantiate GetHerokuAppInfo action
    get_app_info_action = GetHerokuAppInfo()

    # Test GetHerokuAppInfo action
    app_id = "composio"
    get_app_info_request = HerokuAppInfoRequest(app_id=app_id)
    app_info_response = get_app_info_action.execute(authorization_data, get_app_info_request)

    if app_info_response.success:
        print("Heroku App Information:")
        print(app_info_response.app_info)
    else:
        print("Failed to retrieve Heroku App information.")
        print("Response:", app_info_response.app_info)

    # Add more tests for other actions as needed


# Call the function to test Heroku actions
test_heroku_actions()