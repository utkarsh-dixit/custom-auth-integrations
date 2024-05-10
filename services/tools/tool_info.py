from loguru import logger

def get_tool_info(meta_data: dict):
    # to avoid circular dependency
    from services.tools.register_tools import ALL_TOOLS
    tool_name = meta_data["tool_name"]
    client_id = meta_data["client_id"]
    
    default_tool_identifier = f"{tool_name}_default"
    client_tool_identifier = f"{tool_name}_{client_id}"
    
    tool = ALL_TOOLS.get(client_id, {}).get(client_tool_identifier) or ALL_TOOLS.get("default", {}).get(default_tool_identifier)
    if not tool:
        logger.error(f"Tool not found: {tool_name} for client_id: {client_id}")
        return None
    
    return tool.json_schema()