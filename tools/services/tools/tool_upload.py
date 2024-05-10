import os
import shutil
import zipfile
import base64
from fastapi import HTTPException
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from loguru import logger
from pathlib import Path
from services.tools.register_tools import register_custom_tools, storage, SYSTEM_DATA_DIR
from services.tools.validator import modify_tool_file


async def sync_apps(req: dict):
    try:
        client_id = req.get("client_id")
        if not client_id:
            logger.error("Client ID is missing in the request")
            raise HTTPException(status_code=400, detail="Client ID is required")

        custom_client_repo_rel = f"custom_apps/{client_id}"
        logger.info(f"Processing sync for client: {client_id} with repo: {custom_client_repo_rel}")
        client_apps_abs = os.path.join(SYSTEM_DATA_DIR, custom_client_repo_rel)

        # Ensure the directory is clean before use
        shutil.rmtree(client_apps_abs, ignore_errors=True)
        os.makedirs(client_apps_abs)

        zip_path = os.path.join(client_apps_abs, "apps.zip")
        try:
            with open(zip_path, "wb") as zip_file:
                zip_file.write(base64.b64decode(req.get("custom_apps_zip", "")))
        except Exception as e:
            logger.error(f"Failed to decode and write zip file: {str(e)}")
            return {"status": "error", "message": "Invalid zip file"}

        # Extract and clean up the zip file
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(client_apps_abs)
        os.remove(zip_path)

        # Process each Python tool file
        tool_files = [os.path.join(root, name) for root, dirs, files in os.walk(client_apps_abs) for name in files if name.endswith(".py") and not name == "__init__.py"]
        for tool_file in tool_files:
            modify_tool_file(tool_file, client_id)

        # Register tools and handle errors
        errors = register_custom_tools(client_id=client_id)
        if errors:
            logger.error(f"Errors occurred during tool registration: {errors}")
            return {"status": "error", "message": f"Error syncing apps: {errors}"}

        # Archive and upload the synced apps
        app_path = Path(client_apps_abs).resolve()
        zip_path = app_path.parent / f"{app_path}"
        shutil.make_archive(base_name=str(zip_path), format="zip", root_dir=str(app_path))
        storage.upload(f"{zip_path}.zip", f"{custom_client_repo_rel}.zip", False)

        return {"status": "success", "message": f"Apps synced successfully for client {client_id}"}
    except Exception as e:
        logger.error(f"Unhandled exception in sync_apps: {str(e)}")
        return {"status": "error", "message": f"Error syncing apps: {str(e)}"}
