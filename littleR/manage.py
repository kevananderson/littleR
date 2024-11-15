import os
import shutil

def cli():

    #setup functions that the user can call, see below for ***Actions*** defined locally
    selections = [
        { 'fn':goodbye,                 'text': "Exit"},
        { 'fn':new_project,             'text': "Create New Project"},
        { 'fn':littleR_project,         'text': "Use the requirements for the littleR Project"},
        { 'fn':remove_project,          'text': "Remove projects files"},
    ]

    while True:
        #prompt for the user input
        print_cli_options(selections)

        #make sure the user can leave as needed
        try:
            selection_index = input("Select Option: ")
        except KeyboardInterrupt:
            goodbye()
            break

        try:
            #verify the selected input
            index = int(selection_index) - 1
            if index < 0 or index >= len(selections):
                raise IndexError("Invalid user selected index.")
            print(f"Index [{index+1}] selected.")

            #run the selected function
            selections[index]['fn']()

            break
        
        except IndexError:
            print(f"Invalid option, please enter number from the list.")

def print_cli_options(selections):
    print("\nChoose an option from the list. Enter the desired number.")
    for index,selected in enumerate(selections):
        print(f"[{index+1}]: {selected['text']}")

def can_copy_template():
    if not os.path.exists('project') and \
       not os.path.exists('reports') and \
       not os.path.exists('config.yaml'):
        return True
    else:
        print("Cannot overwrite existing project. To remove the the project, select Remove option from main.")

    return False

def template_path(template_name):
    return os.path.join(os.path.dirname(__file__), 'templates', template_name)

#*** Actions ***

def goodbye():
    print( "\nGoodbye." )

def new_project():
    #we are putting the template in the working directory
    if can_copy_template():

        #copy the template from littleR_req to the working dir
        shutil.copytree(template_path('new_req'), os.getcwd(), dirs_exist_ok=True )

def littleR_project():
    #we are putting the template in the working directory
    if can_copy_template():

        #copy the template from littleR_req to the doc working dir
        shutil.copytree(template_path('littleR_req'), os.getcwd(), dirs_exist_ok=True )

def remove_project():
    #does the project exist?
    exists = os.path.exists('project') or os.path.exists('reports') or os.path.exists('config.yaml')

    if exists:
        #make sure the user can leave as needed
        try:
            print("!! Are you sure you want to delete the project? !!")
            confirmation = input("Type [confirm] to delete files: ")
        except KeyboardInterrupt:
            goodbye()
        
        if confirmation == 'confirm':
            if os.path.exists('project'):
                shutil.rmtree('project', ignore_errors=True)
            if os.path.exists('reports'):
                shutil.rmtree('reports', ignore_errors=True)
            if os.path.exists('config.yaml'):
                os.remove('config.yaml')
            print("Project files have been deleted.")
        else:
            print("Files NOT removed.")

if __name__ == "__main__":
    cli()