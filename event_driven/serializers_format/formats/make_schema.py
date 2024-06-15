import inspect
import os
import subprocess
import textwrap

BLUE = "\033[94m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


def _print(text, color_code):
    print(f"{color_code}{text}{RESET}")


class ExecuteTerminalCommand:
    def __init__(self, command, path=os.getcwd()) -> None:
        self.execute_command(command, path)

    def add_tab_in_lines(self, output):
        wrapped_output = textwrap.indent(
            textwrap.fill(output, width=80), "   ")
        return f"{wrapped_output}"

    def execute_command(self, command, path):
        current = os.getcwd()
        os.chdir(path)
        try:

            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=path
            )
            _print(self.add_tab_in_lines(result.stdout), GREEN)
        except subprocess.CalledProcessError as e:
            _print(self.add_tab_in_lines(e.stderr), RED)
        os.chdir(current)


def make_schema():
    ExecuteTerminalCommand("flatc --python event.fbs", path=os.path.join(
        os.getcwd(), "event_driven/serializers/formats/flatbuffer"))
    ExecuteTerminalCommand(f"protoc -I . event.proto --python_out=.",
                           path=os.path.join(os.getcwd(), "event_driven/serializers/formats/protobuf"))


if __name__ == '__main__':
    make_schema()
