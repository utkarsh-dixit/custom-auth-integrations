import datetime
import json
import jsonref
import inflection
from typing import List
from loguru import logger
import traceback
import pg8000
import openai
import os
import inspect
from urllib.parse import urlparse
import time
import sys
from .action import Action
from services.action.global_action import get_global_actions, is_global_action,get_integration_yaml_path

from .trigger import AlreadyExistsError, Trigger
from concurrent.futures import ThreadPoolExecutor



SCHEDULE_ACTION_NAME = "ScheduleJobAction"
ACTION_EXECUTE_WITH_META_DATA = {SCHEDULE_ACTION_NAME: True}

def add_tool_name(tool_name: str, action_name: str) -> str:
    return f"{tool_name.lower()}_{inflection.underscore(action_name)}"

def get_name_of_dir_with_integration_yaml(tool_name: str) -> str: 
    return os.path.basename(os.path.dirname(get_integration_yaml_path(tool_name)))

def meta_data_required_action(action_name):
    if ACTION_EXECUTE_WITH_META_DATA.get(action_name):
        return True
    return False

def get_class_description(action_cls, action_instance):
    if hasattr(action_instance, 'get_description') and callable(getattr(action_instance, 'get_description')):
        return action_instance.get_description()
    return action_cls.__doc__.strip() if action_cls.__doc__ else None


def actions_for_usecase(tool_name, usecase, limit):
    get_task_function = [
                {
                    "name": "get_tasks",
                    "description": "Breaks down a use case into a list of tasks",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tasks": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "description": "Description of a task"
                                }
                            }
                        },
                        "required": ["tasks"]
                    }
                }
            ]
    subtasksystem = """ you will be provided with a big ass usecase for a specific api your job is to break down the usecase into a set of actions use simplify and explain the actions if you can use the function calling
        and only reply in this particular format and nothing else if you think there is some action that is not of the same api do not mention it but only reply in the given json format
    """
    prompts = [{"role": "system", "content": subtasksystem}, {"role": "user", "content": f"here is the total task return the tasks and only in the json format {usecase}"}]
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    def ai(prompts, func_name):
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=prompts,
            functions = func_name,
            function_call = 'auto'
        )
        if response.choices[0].message.function_call is None:
            raise Exception("Function call not found in response")
        return response.choices[0].message.function_call.arguments
    start_time = time.time()
    response = ai(prompts, get_task_function)
    end_time = time.time()
    logger.info(f"AI function call 1 duration: {end_time - start_time} seconds")
    tasks = json.loads(response)["tasks"]

    usecase_action = []
    def process_task(task_description):
        parsed_url = urlparse(os.environ.get("VECTORDB_URL"))
        conn = pg8000.connect(
            host=parsed_url.hostname, #type: ignore
            port=parsed_url.port, #type: ignore
            user=parsed_url.username, 
            password=parsed_url.password, 
            database=parsed_url.path[1:]
        )
        do = []
        start_embedding_time = time.time()
        response = client.embeddings.create(
                input=task_description,
                model="text-embedding-3-large"
            )
        do.append(response.data[0].embedding)
        end_embedding_time = time.time()
        logger.info(f"Embedding generation time: {end_embedding_time - start_embedding_time} seconds")
        query_vector = do[0]
        try:
            query_start_time = time.time()
            query = f"SELECT vector_id, vector FROM {tool_name} ORDER BY vector <=> :vec LIMIT {limit}"
            results = conn.run(query, vec=str(query_vector))
            query_end_time = time.time()
            logger.info(f"Database query duration: {query_end_time - query_start_time} seconds")
            return [result[0] for result in results]
        except pg8000.Error as e:
            logger.error(f"Database error occurred: {e}")
            return ["no"]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_task, tasks))
    for result in results:
        if "no" not in result:
            usecase_action.extend(result)
    if "no" not in usecase_action:
        get_api_function = [
                {
                    "name": "get_apis",
                    "description": "Selects the top APIs for a given action",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "apis": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "description": "Name of an API"
                                        },
                                    },
                                    "required": ["name"]
                                }
                            }
                        },
                        "required": ["apis"]
                    }
                }
            ]
        choose_final_action = f"""
            you will be provided with an action and all possible apis you can call to perform those actions choose the top {limit} no. of actions ONLY GIVE THIS EXACT NUMBER OF ACTIONS OKAY and give me the response
            the response should only be in a structured format use the function call if you need anything
            and so do not reply with anything other than that this has to be strictly in that format
            give the output actions in a sorted format that is by there importance the most important ones should be the first and  the least should be that last
        """
        prompts = [{"role": "system", "content": choose_final_action}, {"role": "user", "content": f"here is the action {usecase} and here are the probable apis you can call {usecase_action} return top {limit} no. of apis that are most probable also only reply in the given format. AGAIN ONLY GIVE THE NUMBER OF ACTIONS I HAVE TOLD YOU ABOUT"}]
        ai_start_time = time.time()
        final_answer = ai(prompts, get_api_function)
        ai_end_time = time.time()
        logger.info(f"AI processing 2 time: {ai_end_time - ai_start_time} seconds")
        final_action = json.loads(final_answer)["apis"]
        final_action = list({api['name']: api for api in final_action}.values())
        top_limit_actions = final_action[:limit]
        return [action['name'] for action in top_limit_actions]
    else:
        return None

class Tool():
    custom_tool_path = None
    dynamic_tool_name = None
    dynamic_description = None
    dynamic_integration_yaml_path = None

    ## this should be dynamic tool
    is_integration_yml_only_tool = False

    def __init__(self, scheduler=None):
        self.scheduler = scheduler
    @property
    def custom_id(self) -> str:
        return self.get_metadata()["unique_id"]

    def set_custom_integration_yaml_and_name(self, path: str, name: str, description: str):
        self.is_integration_yml_only_tool = True
        self.dynamic_integration_yaml_path = path
        self.dynamic_tool_name = name
        self.dynamic_description = description
    
    @property
    def require_scheduler(self):
        if "scheduler" in self.identifier_name():
            return True
        return False
    @property
    def integration_yaml_path(self) -> str:
        return self.get_metadata()["integration_yaml_path"]

    @property
    def tool_name(self) -> str:
        return self.dynamic_tool_name.lower() if self.dynamic_tool_name else self.__class__.__name__.lower()

    def set_custom_tool_path(self, value: str):
        self.custom_tool_path = value
        
    def get_metadata(self) -> dict:
        tool_file_path = self.custom_tool_path if self.custom_tool_path else sys.modules[self.__class__.__module__].__file__
        integration_yaml_path = None
        if tool_file_path:
            integration_yaml_path = tool_file_path.rsplit('/', 1)[0] + '/integrations.yaml'

        unique_id = ""

        if tool_file_path and "apps/" in tool_file_path:
            unique_id = 'default'
            ## Default id
            unique_id = 'default'
        if tool_file_path and "system_data/custom_apps/" in tool_file_path:
            ## Client id
            unique_id = tool_file_path.split("custom_apps/")[1].split("/")[0] if len(tool_file_path.split("custom_apps/")) > 1 else ""

        if tool_file_path and "tool.py" in tool_file_path:
            unique_id = "default"

        return {
            "integration_yaml_path": self.dynamic_integration_yaml_path or integration_yaml_path,
            "unique_id": unique_id,
            "tool_name": self.tool_name
        }
    

    def identifier_name(self) -> str:
        return self.get_metadata()["tool_name"] + "_" + self.custom_id

    def actions(self) -> List[Action]:
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def triggers(self) -> List[Trigger]:
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_action_instance(self, action:Action):
        if action.__name__ == SCHEDULE_ACTION_NAME:
            return action(self.scheduler)
        return action()

    def execute_action(self, action_name: str, request_data: dict, authorisation_data: dict, meta_data) -> dict:
        tool_name = self.__class__.__name__

        self_actions = []
        try:
            self_actions = self.actions()
        except NotImplementedError:
            pass
        tool_actions = self_actions + get_global_actions(tool_name.lower())
        for action in tool_actions:
            action_name_shared = add_tool_name(tool_name, action.__name__)
            if action_name_shared == action_name:
                action_instance = self.get_action_instance(action)
                logger.info(f"Executing {action.__name__} on Tool: {tool_name} with request data {request_data} and authorisation data {authorisation_data}")
                try:
                    request_schema = action_instance.request_schema # type: ignore
                    req = request_schema.model_validate_json(json_data=json.dumps(request_data))
                    if is_global_action(action_name.replace(f"{tool_name.lower()}_", "")):
                        return action_instance.execute_global(meta_data) # type: ignore
                    elif meta_data_required_action(action.__name__):
                        # need to send client_id in scheduler action, sending it from meta data
                        return action_instance.execute_with_meta_data(req, authorisation_data, meta_data)
                    else:
                        return action_instance.execute(req, authorisation_data) # type: ignore
                except Exception as e:
                    logger.error(f"Error executing {action.__name__} on Tool: {tool_name}: {e}\n{traceback.format_exc()}")
                    return {"status": "failure", "details": "Error executing action with error: " + str(e)}
        return {"status": "failure", "details": "Action not found"}
    
    def set_webhook_url(self, trigger_name: str, authorisation_data: dict, trigger_config: dict) -> dict: 
        tool_name = self.__class__.__name__
        for trigger in self.triggers():
            trigger_name_shared = add_tool_name(tool_name, trigger.__name__)
            if trigger_name_shared == trigger_name:
                logger.info(f"Setting webhook URL for Trigger: {trigger_name} on Tool: {tool_name} with URL {trigger_config['webhook_url']} and authorisation data {authorisation_data}")
                try:
                    webhook_url = trigger_config["webhook_url"]
                    del trigger_config["webhook_url"]
                    trigger_config_schema = trigger().trigger_config_schema # type: ignore
                    tc = trigger_config_schema.model_validate_json(json_data=json.dumps(trigger_config))
                    conn_data = trigger().set_webhook_url(authorisation_data, webhook_url, tc) # type: ignore
                    return {"status": "success", "connection_data": conn_data}
                except AlreadyExistsError as e:
                    logger.error(f"Webhook URL already exists for Trigger: {trigger_name} on Tool: {tool_name}: {e}")
                    return {"status": "failure", "details": "Webhook URL already exists"}
                except Exception as e:
                    logger.info(f"Error setting webhook URL for Trigger: {trigger_name} on Tool: {tool_name}: {e}")
                    return {"status": "failure", "details": str(e)}
        return {"status": "failure", "details": "Trigger not found"}
    
    def transform_trigger_payload(self, payload: dict) -> dict:
        tool_name = self.__class__.__name__
        for trigger in self.triggers():
            try:
                logger.info(f"Transforming trigger payload for Tool: {tool_name}")
                (match, connection_data, converted_payload) = trigger().check_and_convert_to_identifier_payload_schema(payload) # type: ignore
                logger.info(f"Match: {match}, Connection Data: {connection_data}, Converted Payload: {converted_payload}")
                if match:
                    return {
                        "trigger_name": add_tool_name(tool_name, trigger.__name__),
                        "connection_data": connection_data,
                        "payload": converted_payload
                    }
            except Exception as e:
                logger.error(f"Error transforming trigger payload for Tool: {tool_name}: {str(e)}")
                return {"status": "failure", "details": "Error transforming trigger payload with error: " + str(e)}
        return {"status": "failure", "details": "Trigger not found"}

    def json_schema(self,  use_case=None, limit: int = 10):
        usecase_actions = []
        tool_name = self.tool_name
        if use_case:
            tool_name = self.__class__.__name__.lower()
            usecase_actions = actions_for_usecase(tool_name, use_case, limit)
            logger.info(f"use_case_actions - {usecase_actions}")

        module_parts = self.__module__.split('.')
        package_name = module_parts[-2] if len(module_parts) > 1 else None
        if not package_name:
            return None
        self_actions = []
        try:
            self_actions = self.actions()
        except NotImplementedError:
            pass

        self_triggers = []
        try:
            self_triggers = self.triggers()
        except NotImplementedError:
            pass
                    
        tool_actions = self_actions + get_global_actions(tool_name.lower())
        action_meta = []
        for action in tool_actions:
            if not use_case or (usecase_actions and add_tool_name(tool_name, action.__name__) in usecase_actions):
                action_instance = self.get_action_instance(action)
                action_description = get_class_description(action, action_instance)
                action_meta.append({
                    "name": add_tool_name(tool_name, action.__name__),
                    "display_name": action_instance.display_name, # type: ignore
                    "tags": action_instance.tags, # type: ignore
                    "description": action_description, # type: ignore
                    "parameters": sort_params_on_default(json_schema_enum_processor(jsonref.loads(json.dumps(action_instance.request_schema.model_json_schema(by_alias=False))))), # type: ignore
                    "response": jsonref.loads(json.dumps(action_instance.response_schema.model_json_schema())) # type: ignore
                })
        return {
            "Name": tool_name,
            "UniqueKey": self.tool_name.replace(" ", "_") if self.is_integration_yml_only_tool else package_name,
            "Description": self.dynamic_description if self.is_integration_yml_only_tool else self.__doc__.strip() if self.__doc__ else None,
            "CustomID": self.custom_id,
            "Actions": action_meta,
            "Triggers": [
                {
                    "name": add_tool_name(tool_name, trigger.__name__),
                    "display_name": trigger().display_name, # type: ignore
                    "description": trigger.__doc__.strip() if trigger.__doc__ else None,
                    "payload": jsonref.loads(json.dumps(trigger().payload_schema.model_json_schema())), # type: ignore
                    "config": jsonref.loads(json.dumps(trigger().trigger_config_schema.model_json_schema())), # type: ignore
                    "instructions": trigger().trigger_instructions # type: ignore
                } for trigger in self_triggers
            ],
        }

def json_schema_enum_processor(param_schema):
    for prop_name, prop_details in param_schema["properties"].items():
        if 'allOf' in prop_details :
            if len(prop_details['allOf'])==1:
                enum_schema = param_schema["properties"][prop_name].pop("allOf")[0]
                param_schema["properties"][prop_name].update(enum_schema)
            else:
                raise ValueError("Case of No/Multiple allOf elements in parameters schema not yet handeled.")
            
        if 'const' in param_schema["properties"][prop_name]:
            if "type" not in param_schema["properties"][prop_name]:
                type_map = {
                    str: "string",
                    int: "integer",
                    float: "number",
                    bool: "boolean"
                }
                param_schema["properties"][prop_name]['type'] = type_map[type(param_schema["properties"][prop_name]['const'])]
            param_schema["properties"][prop_name]["enum"] = [param_schema["properties"][prop_name].pop("const")]
                
                
    if "$defs" in param_schema:
        param_schema.pop("$defs")
    return param_schema

def sort_params_on_default(param_schema):
    # Function to determine the sort key
    def sort_key(item):
        key, value = item
        # Priority 1: No 'default' key
        if 'default' not in value:
            return 0
        # Priority 2: 'default' is None
        elif value['default'] is None:
            return 1
        # Priority 3: 'default' has some value
        else:
            return 2
        
    # Sorting the dictionary based on our custom sort key
    param_schema["properties"] = dict(sorted(param_schema["properties"].items(), key=sort_key))
    return param_schema
    
