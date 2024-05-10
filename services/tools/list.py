from fastapi import HTTPException
from typing import Optional
from loguru import logger
from services.tools.register_tools import ALL_TOOLS, ALL_TOOLS_JSON_SCHEMA
import yaml
import json
import os
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

async def list_tools(
    client_id: str,
    tool_name: Optional[str] = None,
    use_case: Optional[str] = None,
    limit: int = 10,
):
    logger.info(f"Listing tools for client_id: {client_id}, tool_name: {tool_name}, use_case: {use_case}")
    
    if not client_id:
        logger.error("Client ID is missing in the request")
        raise HTTPException(status_code=400, detail="Client ID is required")

    tools = []
    if tool_name:
        tool_name = tool_name.lower()
        default_tool_identifier = f"{tool_name}_default"
        client_tool_identifier = f"{tool_name}_{client_id}"

        tool = ALL_TOOLS.get(client_id, {}).get(client_tool_identifier) or ALL_TOOLS.get("default", {}).get(default_tool_identifier)
        if not tool:
            logger.error(f"Tool not found: {tool_name} for client_id: {client_id} for identifiers: {client_tool_identifier} and {default_tool_identifier}, all_tools_keys: {ALL_TOOLS.keys()}, all_tools_default_keys: {ALL_TOOLS.get('default', {}).keys()}")
            raise HTTPException(status_code=404, detail="Tool not found")

        if use_case:
            schema = tool.json_schema(use_case=use_case, limit=limit)
            if not schema:
                logger.error(f"No schema found for use_case: {use_case}")
                raise HTTPException(status_code=404, detail="Schema for specified use case not found")
            tools.append(schema)
        else:
            tools.append(ALL_TOOLS_JSON_SCHEMA[tool.identifier_name()])
    else:
        for toolset in (ALL_TOOLS.get("default", {}), ALL_TOOLS.get(client_id, {})):
            for tool in toolset.values():
                  try:
                        ALL_TOOLS_JSON_SCHEMA[tool.identifier_name()]
                        tools.append(ALL_TOOLS_JSON_SCHEMA[tool.identifier_name()])                   
                  except Exception as e:
                        print(e)
              

    return {"tools": tools}

async def list_tool_w_basic_info(
    client_id: str,
    tool_name: Optional[str] = None,
):
    logger.info(f"Listing basic tool info for client_id: {client_id}, tool_name: {tool_name}")
    
    if not client_id:
        logger.error("Client ID is missing in the request")
        raise HTTPException(status_code=400, detail="Client ID is required")

    tools =  {}

    combine_toolset = list(ALL_TOOLS.get("default", {}).values()) +  list(ALL_TOOLS.get(client_id, {}).values())
    for tool in combine_toolset:
        try: 
            integration_yaml = ""
            root_dir = get_project_root()

            try:
                with open(os.path.join(root_dir, tool.integration_yaml_path), 'r') as file:
                    yaml_content = yaml.safe_load(file)

                    is_custom_category = tool.custom_id != "default"
                    if is_custom_category:
                       yaml_content["categories"] = yaml_content.get("categories", []) + ["custom"]


                    tools[tool.tool_name] = {
                        "name": tool.tool_name,
                        "data": yaml_content,
                        "integration_yaml_path": tool.integration_yaml_path
                    }
            except FileNotFoundError:
                logger.error(f"Integration YAML not found at {tool.integration_yaml_path}")
                continue
               
            except yaml.YAMLError as exc:
                logger.error(f"Error parsing YAML file at {integration_yaml}: {exc}")
                continue
        except Exception as e:
            logger.error(f"{e}")
            continue
           

    if tool_name:
        try:
            tools = [tool for tool in tools if tool["name"].lower() == tool_name.lower()]
        except Exception as e:
            logger.error(f"Error filtering tools by name: {tool_name}. Error: {e}")
            tools = []
        return {"tools": tools}

    return {"tools": tools}
