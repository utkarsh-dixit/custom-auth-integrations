from fastapi import HTTPException
from loguru import logger
from services.tools.register_tools import ALL_TOOLS

async def transform_trigger_payload(trigger_payload: dict) -> dict:
    tool_name = trigger_payload["tool_name"].lower()
    client_id = trigger_payload["client_id"]
    client_tool_identifier = f"{tool_name}_{client_id}"
    default_tool_identifier = f"{tool_name}_default"

    logger.info(f"Transforming trigger payload for Tool: {tool_name}")

    if default_tool_identifier not in ALL_TOOLS.get("default", {}) and client_tool_identifier not in ALL_TOOLS.get(client_id, {}):
        tools = [
            tool.identifier_name()
            for toolset in (ALL_TOOLS["default"], ALL_TOOLS.get(client_id, {}))
            for tool in toolset.values()
        ]
        logger.info("Only supported tools are: ", tools)
        raise HTTPException(status_code=404, detail="Tool not found")

    tool = ALL_TOOLS.get(client_id, {}).get(client_tool_identifier, ALL_TOOLS["default"].get(default_tool_identifier))
    transformed_payload = tool.transform_trigger_payload(payload=trigger_payload["request"])
    return transformed_payload

async def set_webhook_url(set_webhook_url_payload: dict) -> dict:
    tool_name = set_webhook_url_payload["tool_name"].lower()
    client_id = set_webhook_url_payload["client_id"]
    default_tool_identifier = f"{tool_name}_default"
    client_tool_identifier = f"{tool_name}_{client_id}"

    logger.info("Received request to set webhook URL", set_webhook_url_payload)

    if default_tool_identifier not in ALL_TOOLS.get("default", {}) and client_tool_identifier not in ALL_TOOLS.get(client_id, {}):
        tools = [
            tool.json_schema()
            for toolset in (ALL_TOOLS["default"], ALL_TOOLS.get(client_id, {}))
            for tool in toolset.values()
        ]
        logger.info("Only supported tools are: ", tools)
        raise HTTPException(status_code=404, detail="Tool not found")

    tool = ALL_TOOLS.get(client_id, {}).get(client_tool_identifier, ALL_TOOLS["default"].get(default_tool_identifier))
    response = tool.set_webhook_url(
        set_webhook_url_payload["trigger_name"],
        set_webhook_url_payload["authorization_data"],
        set_webhook_url_payload["trigger_config"],
    )
    return response
