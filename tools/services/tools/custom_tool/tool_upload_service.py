from typing import TypedDict
import shutil
import os
from pydantic import BaseModel
from openapi_spec.openapi_codegen_class import OpenAPICodegenTool
from services.tools.register_tools import register_custom_tools, storage, SYSTEM_DATA_DIR

class IndividualComponentStatusLogs(BaseModel):
    is_success: bool
    logs: list[dict]

class ToolUploadStatusLogs(BaseModel):
    is_success: bool
    openapi_spec: IndividualComponentStatusLogs

class ToolUploadService:
    def __init__(self) -> None:
        pass

    def create_tool_dir_from_openapi_spec(self, client_id: str, open_api_spec_yaml: str, name: str, integration_yaml: str) -> IndividualComponentStatusLogs:
        logs = []
        is_success = True
        openapi_codegen_tool = OpenAPICodegenTool(tool_name=name, tool_dir="../apps", output_dir=f"{SYSTEM_DATA_DIR}/generate_tool/{client_id}", spec=open_api_spec_yaml, integration_yaml=integration_yaml)
        
        try:
            openapi_codegen_tool.write_spec_files()
        except Exception as e:
            print(repr(e))
            logs.append({
                "type": "error",
                "message": repr(e),
                "data": {
                    "type": "OPENAPI_SPEC",
                    "details": "Error in generating open api tools"
                }
            })
            is_success = False

      
        for log_entry in openapi_codegen_tool.logger:
            logs.append(log_entry)
      

        if is_success:
            logs.append({
                "type": "log",
                "message": "Created tool directory"
            })
            self.move_tool_dir_to_custom_apps(client_id, name)
            
            logs.append({
                "type": "log",
                "message": "Moved tool directory to custom apps"
            })

            is_valid_tool_dir = self.validate_tool_dir(client_id, name)

            print(is_valid_tool_dir)
            if is_valid_tool_dir.get("is_success"):
                logs.append({
                    "type": "log",
                    "message": "Tool directory is valid"
                })
                self.upload_tool_to_s3(client_id)
                logs.append({
                    "type": "log",
                    "message": "Upload to S3 successful"
                })
            else:
                is_success = False
                for log in is_valid_tool_dir["logs"]:
                    logs.append({
                        "type": "registering",
                        "message": log
                    })
         

        print(logs)
        return IndividualComponentStatusLogs(
            is_success=is_success,
            logs = logs
        )

    def validate_tool_dir(self, client_id: str, name: str) -> dict:
        errors = register_custom_tools(client_id=client_id,path=f"/{name}")
        if len(errors) == 0:
            return {
                "is_success": True,
                "logs": ["Directory creation successful", "Tool directory is valid", "Upload to S3 successful"]
            }
        else:
            ## Delete the tool directory
           
                #  shutil.rmtree(f"{SYSTEM_DATA_DIR}/generate_tool/{client_id}")
                # shutil.rmtree(f"{SYSTEM_DATA_DIR}/custom_apps/{client_id}/{name}")
              
            return {
                "is_success": False,
                "logs": [
                    {
                        "type": "error",
                        "details": error
                    } for error in errors
                ]
            }

    def move_tool_dir_to_custom_apps(self, client_id: str, name: str) -> bool:
        tool_directory = f"{SYSTEM_DATA_DIR}/generate_tool/{client_id}"
        target_dir = f"{SYSTEM_DATA_DIR}/custom_apps/{client_id}/{client_id}"

        if os.path.exists(target_dir):
            for item in os.listdir(tool_directory):
                s = os.path.join(tool_directory, item)
                d = os.path.join(target_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
        else: 
            shutil.move(tool_directory, target_dir)

        return True
    
    def upload_tool_to_s3(self, client_id: str):
        tool_directory = f"{SYSTEM_DATA_DIR}/custom_apps/{client_id}"
        zip_path = shutil.make_archive(tool_directory, 'zip', tool_directory)
        custom_client_repo_rel = f"custom_apps/{client_id}.zip"
        storage.upload(zip_path, custom_client_repo_rel, False)

    def generate_tool_zip_from_openapi_spec(self, client_id: str, name: str, specYML: str, integration_yaml: str) -> ToolUploadStatusLogs:
        openapi_spec_status = self.create_tool_dir_from_openapi_spec(client_id, specYML, name, integration_yaml)

        return ToolUploadStatusLogs(
            is_success=openapi_spec_status.is_success,
            openapi_spec=openapi_spec_status,
        )
    
    def delete_tool(self, client_id: str, name: str):
        shutil.rmtree(f"{SYSTEM_DATA_DIR}/custom_apps/{client_id}/{name}")
        self.upload_tool_to_s3(client_id)
        register_custom_tools(client_id=client_id)

    def get_tools_for_client(self, client_id: str):
        dir_name = f"{SYSTEM_DATA_DIR}/custom_apps/{client_id}"
        
        #list top folder in dirName
        top_folders = []
        if os.path.exists(dir_name):
            top_folders = [item for item in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name, item))]
        return top_folders
