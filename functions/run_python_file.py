import os
import subprocess
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_path_working_dir = os.path.abspath(working_directory)
        target_dir =  os.path.normpath(os.path.join(abs_path_working_dir,file_path))

        valid_target_dir = os.path.commonpath([abs_path_working_dir,target_dir]) == abs_path_working_dir
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        is_file =  os.path.isfile(target_dir)

        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args:
            command.extend(args)
        result = subprocess.run(command,timeout=30,text=True,capture_output=True,cwd=working_directory)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    output_string = ""
    if result.returncode != 0:
        output_string+= f"Process exited with code {result.returncode}"
    if  not result.stderr and not result.stdout:
        output_string+= "No output produced"
    if result.stdout:
        output_string+=f"STDOUT: {result.stdout}"
    if result.stderr:
        output_string+= f"STDERR: {result.stderr}"


    return output_string

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file we will execute",
                },
                "args":{
                    "type": "array",
                    "description": "Optional command-line arguments to pass to the Python file when executing",
                    "items": {
                            "type": "string"
                        },
                },

            },
            "required":["file_path"],
        },
    },
}
