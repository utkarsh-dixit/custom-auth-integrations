import asyncio
import os
import shutil
import glob
import importlib.util
from typing import Dict
from loguru import logger
from os import getenv

import re

from apps.serpapi import Serpapi
from apps.github import Github
from apps.linear import Linear
from apps.linearsandbox import Linearsandbox
from apps.asana import Asana
from apps.trello import Trello
from apps.notion import Notion
from apps.zendesk import Zendesk
from apps.typeform import Typeform
from apps.dropbox import Dropbox
from apps.slack import Slack
from apps.slackbot import SlackBot
from apps.apify import Apify
from apps.gcalendar import Googlecalendar
from apps.gmail import Gmail
from apps.exa import Exa
from apps.filemanager import Filemanager
from apps.scheduler.scheduler_tool import Scheduler


from apps.codeinterpreter import CodeInterpreter

from shared.composio_tools.lib.tool import Tool
from system.storage import Storage
from apps.githublargebeta import Githublargebeta
from apps.trellolargebeta import Trellolargebeta
from apps.slacklargebeta import Slacklargebeta
from apps.listennotes import Listennotes
from apps.elevenlabs import Elevenlabs
from apps.zoom import Zoom
from apps.snowflake import Snowflake
from apps.notionbeta import Notionbeta
from shared.composio_tools.lib.tool import Tool
from system.storage import Storage
from .validator import validate_tools

from apps.brevo import Brevo
from apps.attio import Attio
from apps.okta import Okta

import yaml

SYSTEM_DATA_DIR = getenv("CUSTOM_VOLUME_PATH", "./system_data")
APP_DIR = getenv("CUSTOM_VOLUME_PATH", 
                 "./apps",
                 )
ALL_TOOLS: Dict[str, Dict[str, Tool]] = {}
ALL_TOOLS_JSON_SCHEMA: Dict[str, Dict[str, Tool]] = {}

class ToolToRegister():
    def __init__(self):
        self.tool_class_to_register = [Github, Linear, Asana, Trello, Notion, Zendesk, Typeform,
                                        Dropbox, Slack, Apify, Googlecalendar, Githublargebeta,
                                        Trellolargebeta, Slacklargebeta, Gmail, SlackBot, CodeInterpreter,
                                        Serpapi, Snowflake, Exa, Filemanager, Notionbeta, Scheduler, Zoom,
                                       Listennotes, Elevenlabs, Brevo, Attio, Okta]
        self.tools_to_register = []

    def initialize_tools(self, scheduler):
        if os.getenv("IN_SANDBOX") == "true":
            self.tools_to_register = [Linearsandbox()]
        else:
            self.tools_to_register = [tool_class(scheduler) if tool_class.require_scheduler else tool_class()
                                      for tool_class in self.tool_class_to_register]
        return self.tools_to_register

storage = Storage(
    os.getenv("AWS_ACCESS_KEY_ID", "972bf213575a9a6ad16f18d4ad9a675d"),
    os.getenv(
        "AWS_SECRET_ACCESS_KEY",
        "8fd79a4126710c9c722c909abd5ac4ced270495f4cf2645ee826d7250c618e6c",
    ),
    os.getenv(
        "ENDPOINT_URL",
        "https://4d4f16c61d89ec64e760039c4ec50717.r2.cloudflarestorage.com/",
    ),
    os.getenv("BUCKET_NAME", "tools-staging"),
)


def load_and_register_tool(module_path):
    try:
        module_content = ''
        with open(module_path, 'r') as file:
            module_content = file.read()
        
        class_name_search = re.search(r'class\s+(\w+)\(Tool\):', module_content)
    
        module_path = module_path.replace('./', '').replace('/', '.').rstrip('.py').replace('.Users.himanshu.Desktop.composio.hermes.tools.','')

        imported_module = importlib.import_module(module_path)
        tool_class = imported_module.__getattribute__(class_name_search.group(1))
        instance = tool_class()

        if instance.custom_id not in ALL_TOOLS:
            ALL_TOOLS[instance.custom_id] = {}
  
        identifier = instance.identifier_name()
        ALL_TOOLS[instance.custom_id][identifier] = instance
        ALL_TOOLS_JSON_SCHEMA[identifier] = instance.json_schema()

     
        logger.info(f"Successfully imported module: {module_path} {instance.custom_id} ",)
    except ImportError as e:
        logger.error(f"Failed to import module {module_path}: {str(e)}")


def register_default_tools():
   file_pattern = f"{APP_DIR}/**/*.yaml"

   files = glob.glob(file_pattern, recursive=True)
   for integration_yml in files: 

        is_any_python_file_in_same_dir = len(glob.glob(os.path.join(os.path.dirname(integration_yml), '*.py'))) > 1

        if(is_any_python_file_in_same_dir):
            continue

        name = ""
        description = ""
        with open(integration_yml, 'r') as file:
            try:
                integration_data = yaml.safe_load(file)
            except Exception as e:
                print(e)
                continue

            name = integration_data.get('name', 'Unnamed Tool')
            description = integration_data.get('description', None)

        custom_tool_instance = Tool()
        custom_tool_instance.set_custom_integration_yaml_and_name(integration_yml, name, description)

        identifier = custom_tool_instance.identifier_name()

        if(custom_tool_instance.custom_id not in ALL_TOOLS):
            ALL_TOOLS[custom_tool_instance.custom_id] = {}

        ALL_TOOLS[custom_tool_instance.custom_id][identifier] = custom_tool_instance
        ALL_TOOLS_JSON_SCHEMA[identifier] = custom_tool_instance.json_schema()

        logger.info(f"Successfully registered tool: {custom_tool_instance.custom_id} with identifier: {identifier}")
           


def register_custom_tools(client_id=None,path=''):
    file_pattern = f"{SYSTEM_DATA_DIR}/**/*.py" if not client_id else f"{SYSTEM_DATA_DIR}/**/{client_id}/**/*.py"

    files = glob.glob(file_pattern, recursive=True)
    files = [f for f in files if not (f.endswith("__init__.py") or "actions" in f)]
    
    errors = []
    for tool_path in files:  
       
        module_content = ''
        with open(tool_path, 'r') as file:
            module_content = file.read()
        
        class_name = re.search(r'class\s+(\w+)\(Tool\):', module_content)
    
        if class_name is not None:
            try:
        
                load_and_register_tool(tool_path)
            except Exception as e:
                error_message = f"Error loading tool {tool_path}: {e}"
                logger.error(error_message)
                errors.append(error_message)
    return errors

async def on_mount_download_from_s3() -> dict:
    storage.download("custom_apps", os.path.join(SYSTEM_DATA_DIR, "custom_apps"), True)
    return {"status": "ok"}

async def register_tools(scheduler):
    #storage.delete("custom_apps",True)
    if not os.path.exists(SYSTEM_DATA_DIR):
        await on_mount_download_from_s3()

    tool_register = ToolToRegister()
    tools_to_register = tool_register.initialize_tools(scheduler)

    async def register_tool(tool):
        logger.info(f"⚙️ Registering tool: {tool.__class__.__name__}")
        default_tools = ALL_TOOLS.setdefault("default", {})
        # try:
        default_tools[tool.identifier_name()] = tool
        # except Exception as e:
        # logger.error(f"tool: {tool.__class__.__name__} exception: " + str(e))
        tool_json_schema = tool.json_schema()
        if tool_json_schema:
            ALL_TOOLS_JSON_SCHEMA[tool.identifier_name()] = tool_json_schema

    register_default_tools()
    await asyncio.gather(*(register_tool(tool) for tool in tools_to_register))
    validate_tools(path=os.path.join(__file__, "apps"), is_default=True)
    register_custom_tools()
