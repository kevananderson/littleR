import os
import shutil

def cli():

    #setup functions that the user can call, see below for ***Actions*** defined locally
    selections = [
        { 'fn':goodbye,                 'text': "Exit"},
        { 'fn':new_project,             'text': "Create New Project"},
        { 'fn':littleR_project,         'text': "Use the requirements for the littleR Project"},
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

def make_doc_folder():
    if not os.path.exists('doc'):
        os.makedirs('doc')

def template_path(template_name):
    return os.path.join(os.path.dirname(__file__), 'templates', template_name)

def find_name_for_copy():
    #TODO: we may want to have the project copied in the root directory
    #our first choice is to call it littleR
    path = 'doc/littleR'
    if not os.path.exists('doc/littleR'):
        return path
    
    #we need to append a number at the end
    number = 1
    while True:
        path = f"doc/littleR_{number:02}"
        if not os.path.exists(path):
            return path
        number += 1
        if number >= 100:
            raise ValueError("Tried 100 times but unable to find a valid dirctory name. Please check in the doc folder for too many littleRs.")
            

#*** Actions ***

def goodbye():
    print( "\nGoodbye." )

def new_project():
    #all setup is done in the doc folder
    make_doc_folder()

    #copy the template from littleR_req to the doc folder
    shutil.copytree(template_path('new_req'), find_name_for_copy() )

def littleR_project():
    #all setup is done in the doc folder
    make_doc_folder()

    #copy the template from littleR_req to the doc folder
    shutil.copytree(template_path('littleR_req'), find_name_for_copy() )

if __name__ == "__main__":
    cli()