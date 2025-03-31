"""Command line interface for the littleR project."""

import os
import shutil
import subprocess
import webbrowser

from context import littleR
from littleR.standard import Standard

def main():
    """Main function to run command line for installed project.
    
    This has two functions:
        * Run the command line interface for the littleR project.
        * Start the gui and open the default web browser to local host.
    """
    # check if the user wants to run the command line interface or the GUI
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "gui":
        _start_gui()
    else:
        cli()


def cli():
    """Command line interface for the littleR project.

    This function provides a simple command line interface for the user to
    interact with the littleR project. The options available are a list 
    of functions and text. The user can select an option by entering the number
    associated with the option. The selected function is then called.
    """
    #still not sure if this should be provided as a parameter or not
    selections = [
        {"fn": _goodbye, "text": "Exit."},
        {"fn": _new_project, "text": "Create New Project."},
        {
            "fn": _littleR_project,
            "text": "Populate Example Project (littleR Requirements).",
        },
        {"fn": _remove_project, "text": "Remove projects files."},
        {"fn": _validate_project, "text": "Validate project requirements."},
        {"fn": _start_gui, "text": "Start the GUI."},
    ]

    #verify input
    if selections is None:
        raise ValueError("Selections must not be None.")
    for selection in selections:
        if not isinstance(selection, dict):
            raise TypeError("Selection items must be dicts.")
        if "fn" not in selection or "text" not in selection:
            raise ValueError("Selection items (dict) must contain 'fn' and 'text' keys.")
        if not callable(selection["fn"]):
            raise TypeError("Selection item 'fn' must be callable.")
        if not isinstance(selection["text"], str):
            raise TypeError("Selection item 'text' must be a string.")

    #have the user make a selection
    while True:
        # prompt for the user input
        _print_cli_options(selections)

        # make sure the user can leave as needed
        try:
            selection_index = input("Select Option: ")
        except KeyboardInterrupt:
            _goodbye()
            break

        try:
            # verify the selected input
            index = int(selection_index) - 1
            if index < 0 or index >= len(selections):
                raise IndexError("Invalid user selected index.")
            print(f"Option [{index+1}] selected.")

            # run the selected function
            selections[index]["fn"]()

            break

        except IndexError:
            print("Invalid option, please enter number from the list.")


def _print_cli_options(selections):
    print("\nChoose an option from the list. Enter the desired number.")
    for index, selected in enumerate(selections):
        print(f"[{index+1}]: {selected['text']}")


def _can_copy_template():
    if (
        not os.path.exists("project")
        and not os.path.exists("reports")
        and not os.path.exists("config.yaml")
    ):
        return True

    print(
        "Cannot overwrite existing project. To remove the the project, "
        + "select Remove option from main."
    )

    return False


def _template_path(template_name):
    return os.path.join(os.path.dirname(__file__), "templates", template_name)


# *** Actions ***


def _goodbye():
    print("\nGoodbye.")


def _new_project():
    # we are putting the template in the working directory
    if _can_copy_template():

        # copy the template from littleR_req to the working dir
        shutil.copytree(_template_path("new_req"), os.getcwd(), dirs_exist_ok=True)


def _littleR_project():  # pylint: disable=invalid-name
    # we are putting the template in the working directory
    if _can_copy_template():

        # copy the template from littleR_req to the doc working dir
        shutil.copytree(_template_path("littleR_req"), os.getcwd(), dirs_exist_ok=True)


def _remove_project():
    # does the project exist?
    exists = (
        os.path.exists("project")
        or os.path.exists("reports")
        or os.path.exists("config.yaml")
    )

    if exists:
        # make sure the user can leave as needed
        try:
            print("!! Are you sure you want to delete the project? !!")
            confirmation = input("Type [confirm] to delete files: ")
        except KeyboardInterrupt:
            _goodbye()

        if confirmation == "confirm":
            if os.path.exists("project"):
                shutil.rmtree("project", ignore_errors=True)
            if os.path.exists("reports"):
                shutil.rmtree("reports", ignore_errors=True)
            if os.path.exists("config.yaml"):
                os.remove("config.yaml")
            print("Project files have been deleted.")
        else:
            print("Files NOT removed.")


def _validate_project():
    standard = Standard().read()
    standard.write()
    print("Project requirements validated.")
    print(f"Problems found: {standard.validator().problem_count()}")
    if standard.validator().problem_count() > 0:
        print("Please review the problems and correct as needed.")
        print(
            f"The report is located: {standard.validator().report_path().replace("\\", "/")}"
        )

def _start_gui():
    """Run administrative tasks."""
    abs_path = os.path.abspath("./src/littleR/interface/manage.py")
    process = subprocess.Popen(["./.venv/Scripts/python", abs_path, "runserver"])
    webbrowser.open("http://localhost:8000/viewR")
    try:
        process.wait()
    except KeyboardInterrupt as e:
        process.terminate()
        print("User stopped the server.")



if __name__ == "__main__":
    main()
