import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path_working_dir = os.path.abspath(working_directory)
        target_dir =  os.path.normpath(os.path.join(abs_path_working_dir,directory))

        valid_target_dir = os.path.commonpath([abs_path_working_dir,target_dir]) == abs_path_working_dir
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        target_is_dir = os.path.isdir(target_dir)
        if not target_is_dir:
            return f'Error: "{directory}" is not a directory'
        items = os.listdir(target_dir)
        for item in items:
            item_path = os.path.join(target_dir,item)
            item_info = os.stat(item_path)
            print(f"- {item}: file_size={item_info.st_size} bytes, is_dir={os.path.isdir(item_path)}")
    except Exception as e:
        return f"Error: {e}"

    return f'Success: "{directory}" is within the working directory'


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
