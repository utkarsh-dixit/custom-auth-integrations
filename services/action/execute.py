import asyncio

from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse
from typing import Dict
import requests

from e2b import Sandbox


from loguru import logger
import asyncio
from services.tools.register_tools import ALL_TOOLS, ALL_TOOLS_JSON_SCHEMA


async def execution_action_in_sandbox(action_request: dict) -> dict:
    sandbox = Sandbox(template="tools-sandbox-new")
    try:
        host = sandbox.get_hostname(8000)
        sandbox.process.start(
            "/app/venv/bin/python main.py",
            on_stdout=lambda x: logger.info(x),
            on_stderr=lambda x: logger.error(x),
            cwd="/app",
            env_vars={"IN_SANDBOX": "true"},
        )
        logger.info(f"Host: {host}")
        # Check if the sandbox is ready by pinging its root URL until it returns {"status": "ok"}
        sandbox_ready = False
        while not sandbox_ready:
            try:
                response = requests.get(f"https://{host}")
                if (
                    response.status_code == 200
                    and response.json().get("status") == "ok"
                ):
                    sandbox_ready = True
                    logger.info("Sandbox is ready.")
                else:
                    logger.info("Waiting for sandbox to be ready...")
                    await asyncio.sleep(2)  # Wait for 2 seconds before retrying
            except Exception as e:
                logger.error(f"Error checking sandbox readiness: {e}")
                await asyncio.sleep(2)  # Wait for 2 seconds before retrying
        url = f"https://{host}/execute_action"

        response = requests.post(url, json=action_request, timeout=30)
    finally:
        sandbox.close()

    try:
        return JSONResponse(status_code=response.status_code, content=response.json())  # type: ignore
    except ValueError:
        return Response(status_code=response.status_code, content=response.text)  # type: ignore


async def execute_action(action_request: dict) -> dict:
    logger.info(f"Received action execution request: {action_request}")
    tool_name = action_request.get("tool_name")
    if not tool_name:
        logger.error("Tool name is missing in the action request")
        raise HTTPException(status_code=400, detail="Tool name is required")
    tool_name = tool_name.lower()
    action_name = action_request.get("action_name")
    if not action_name:
        logger.error("Action name is missing in the action request")
        raise HTTPException(status_code=400, detail="Action name is required")
    authorisation_data = action_request.get("authorisation_data", {})
    request_data = action_request.get("request_data", {})
    logger.info(
        f"Executing {action_name} on Tool: {tool_name} with request data {request_data} and authorisation data {authorisation_data}"
    )
    if action_request.get("run_in_sandbox", False):
        action_request_modified = {
            key: value
            for key, value in action_request.items()
            if key != "run_in_sandbox"
        }
        return await execution_action_in_sandbox(action_request=action_request_modified)

    default_tool_identifier = f"{tool_name}_default"
    client_tool_identifier = f"{tool_name}_{action_request['client_id']}"
    client_id = action_request.get("client_id", "default")
    if default_tool_identifier not in ALL_TOOLS.get(
        "default", {}
    ) and client_tool_identifier not in ALL_TOOLS.get(client_id, {}):
        tools = [
            tool.identifier_name()
            for toolset in (ALL_TOOLS["default"], ALL_TOOLS.get(client_id, {}))
            for tool in toolset.values()
        ]
        logger.info("Only supported tools are: ", tools)
        raise HTTPException(status_code=404, detail="Tool not found")

    tool = ALL_TOOLS.get(client_id, {}).get(client_tool_identifier) or ALL_TOOLS.get(
        "default", {}
    ).get(default_tool_identifier)
    if not tool:
        logger.error(f"Tool not found: {tool_name} for client_id: {client_id}")
        raise HTTPException(status_code=404, detail="Tool not found")
    
    meta_data = {
        "client_id": client_id,
        "tool_name": tool_name
    }
    
    action_response = await asyncio.to_thread(
        tool.execute_action,
        action_name=action_name,
        request_data=request_data,
        authorisation_data=authorisation_data,
        meta_data=meta_data
    )

    return action_response
