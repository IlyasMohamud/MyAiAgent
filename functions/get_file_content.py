import os


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path_working_dir = os.path.abspath(working_directory)
        target_dir =  os.path.normpath(os.path.join(abs_path_working_dir,file_path))

        valid_target_dir = os.path.commonpath([abs_path_working_dir,target_dir]) == abs_path_working_dir
        if not valid_target_dir:
            return f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory'

        is_file =  os.path.isfile(target_dir)

        if not is_file:
            return f'Error: File not found or is not a regular file: "{target_dir}"'

        with open(target_dir, "r", encoding="utf-8") as file:
            contents = file.read(10000)
            if file.read(1):
                    contents += f'[...File "{target_dir}" truncated at 10000 characters]'


    except Exception as e:
        return f"Error: {e}"



    return contents

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Gets the content of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file we will get content of",
                },
            },
            "required":["file_path"]
        },
    },
}
