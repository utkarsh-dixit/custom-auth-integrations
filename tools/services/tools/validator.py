import os

import requests

from shared.composio_tools.lib.tool import Tool

from loguru import logger

from utils.validator import validate_folder_name, validate_integrations_yaml

def validate_tools(path: str, is_default: bool = False):
    try:
        folders = os.listdir(path)
        failed_apps = []
        for folder in folders:
            try:
                print(
                    f"Folder: {folder}",
                    validate_folder_name(folder),
                    validate_integrations_yaml(
                        os.path.join(path, folder, "integrations.yaml")
                    ),
                )
            except Exception as e:
                failed_apps.append((folder, e))

        if is_default and len(failed_apps) > 0:
            proper_message = f"There are {len(failed_apps)} errors in the default apps:"
            i = 0
            for app, error in failed_apps:
                proper_message += f"\n{i+1}. {app}: {error}"
                i += 1
            requests.post(
                "https://hooks.slack.com/triggers/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",
                json={"text": proper_message},
            )
            return {
                "status": "success",
                "message": f"Default apps validated successfully",
                "failed_apps": failed_apps,
            }
    except Exception as e:
        return {"status": "error", "message": f"{str(e)}"}


def modify_tool_file(tool_file, client_id):
    with open(tool_file, "r") as file:
        lines = file.readlines()
        # Find the line where class that extends Tool is defined and insert _custom_id after the docstring
        class_found = False
        print(lines)
        for i, line in enumerate(lines):
            if "class" in line and "(Tool)" in line:
                class_found = True
                logger.info(f"Found class definition at line {i}")
                # Find the correct indentation level
                indentation = len(line) - len(line.lstrip())
                docstring_end_found = False
                # Find the end of the docstring
                for j in range(i + 1, len(lines)):
                    if '"""' in lines[j] and not docstring_end_found:
                        docstring_end_found = True
                    elif '"""' in lines[j] and docstring_end_found:
                        # Insert _custom_id after the end of the docstring, respecting the original indentation
                        lines.insert(
                            j + 1,
                            " " * indentation + f"    _custom_id = '{client_id}'\n",
                        )
                        break
                break

        if not class_found:
            logger.error(f"No Tool class found in {tool_file}")
            raise Exception("Tool class definition not found")

            # Write the modified content back to the file
        with open(tool_file, "w") as file:
            file.writelines(lines)
