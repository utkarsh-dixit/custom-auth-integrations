from pydantic import BaseModel, Field
from shared.composio_tools.lib.tool import Action
import yaml
import os
from services.tools.tool_info import get_tool_info

class GetToolInfoRequest(BaseModel):
    """
    Request schema for getting tool info.
    """
class GetToolDescriptionResponse(BaseModel):
    tool_description: str = Field(..., description="The description of the tool")

class GetActionsResponse(BaseModel):
    actions: list[object] = Field(..., description="The actions of the tool")
    
class GetToolDescription(Action):
    """
    Get the description of the tool.
    """
    _display_name = "Get Tool Description"
    _request_schema = GetToolInfoRequest
    _response_schema = GetToolDescriptionResponse

    def execute(self, req: GetToolInfoRequest, authorisation_data: dict):
         pass
     
    def execute_global(self, meta_data: dict):
        
        tool_info = get_tool_info(meta_data)
        if tool_info:
            return {
                    "execution_details": {"executed": True},
                    "response_data": tool_info["Description"]
                }
        else:
            return {
                "execution_details": {"executed": False},
                "response_data": "Failed to get the tool description"
            }
            
class ListAllActions(Action):
    """
    Get the tool actions.
    """
    _display_name = "Get Tool Actions"
    _request_schema = GetToolInfoRequest
    _response_schema = GetActionsResponse

    def execute(self, req: GetToolInfoRequest, authorisation_data: dict):
        pass
    
    def execute_global(self, meta_data: dict):
        tool_info = get_tool_info(meta_data)
        if tool_info:
            return {
                    "execution_details": {"executed": True},
                    "response_data": [action["display_name"] for action in tool_info["Actions"]] 
                }  
        else:
            return {
                "execution_details": {"executed": False},
                "response_data": "Failed to list the tool actions"
            }
            
AVAILABLE_ACTIONS = {
    'get_tool_description': GetToolDescription,
    'list_all_actions': ListAllActions
}   

def is_global_action(action_name)-> bool:
    return action_name in AVAILABLE_ACTIONS

def get_integration_yaml_path(tool_name: str) -> str:
    return f"apps/{tool_name}/integrations.yaml"

def get_global_actions(tool_name: str) -> list:
    
    integrations_path = f"apps/{tool_name}/integrations.yaml"
    global_actions = []
    
    if os.path.exists(integrations_path):
                
        with open(integrations_path, 'r') as stream:
            try:
                integrations = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                raise e

        if "global_actions" in integrations:
            for action in integrations["global_actions"]:
                action_name, is_enabled = list(action.items())[0]
                if is_enabled and action_name in AVAILABLE_ACTIONS:
                    global_actions.append(AVAILABLE_ACTIONS.get(action_name))

    return global_actions
