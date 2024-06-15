import os
import subprocess
import sys
import textwrap
from subprocess import call

BLUE = "\033[94m"
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


def print_(text, color_code):
    print(f"{color_code}{text}{RESET}")


def add_tab_in_lines(output):
    wrapped_output = textwrap.indent(textwrap.fill(output, width=80), "   ")
    return f"{wrapped_output}"


def execute_command(command, path=os.getcwd()):
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
        print_(add_tab_in_lines(result.stdout), GREEN)
    except subprocess.CalledProcessError as e:
        print_(add_tab_in_lines(e.stderr), RED)


def add_init_files(directory="."):
    for root, dirs, files in os.walk(directory):
        if root.startswith(os.path.join(directory, "venv")):
            continue

        if root.startswith(os.path.join(directory, "locale")):
            continue

        python_files = [file for file in files if file.endswith(".py")]
        if not python_files:
            continue

        if "__init__.py" not in files:
            init_path = os.path.join(root, "__init__.py")
            with open(init_path, "w"):
                pass
            print_(f"   Added __init__.py to {root}", GREEN)


def pre_commit():
    done = ('   done \n', GREEN)
    print_("\u25CF Open all python pakages and check for init file...", BLUE)
    for entry in os.scandir("."):
        if entry.is_dir() and not entry.name.startswith("venv"):
            add_init_files(entry.path)
    print_('\n' + done[0], done[1])

    print_("\u25CF Fix pep8 and other stuff...", BLUE)
    execute_command("autopep8 --in-place --recursive . --exclude venv,docs")
    execute_command("isort .")
    print_(done[0], done[1])

    print_('\u25CF Working on sphinx docs...', BLUE)
    # call(['sphinx-apidoc', '-o', 'docs/source/',
    #      '.', './*venv*', './*migrations*'])
    # execute_command('.\make.bat html *> $null',
    #                 os.path.join(os.getcwd(), 'docs'))
    print_('\n   still working on it', GREEN)
    # print_(done[0], done[1])

    return True


if __name__ == "__main__":
    pre_commit()
