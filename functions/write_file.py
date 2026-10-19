import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path_working_dir = os.path.abspath(working_directory)
        target_dir =  os.path.normpath(os.path.join(abs_path_working_dir,file_path))

        valid_target_dir = os.path.commonpath([abs_path_working_dir,target_dir]) == abs_path_working_dir
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        target_is_dir = os.path.isdir(target_dir)
        if target_is_dir:
            return  f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_dir),exist_ok=True)

        with open(target_dir, "w", encoding="utf-8") as file:
            file.write(content)
    except Exception as e:
        return f'Error: {e}'



    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write or overwrite files",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file we will write in",
                },
                "content":{
                    "type": "string",
                    "description": "What will be written in the file"
                },
            },
            "required":["file_path","content"],
        },
    },
}
