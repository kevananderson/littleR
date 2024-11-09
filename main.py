import littleR
import littleR.helloworld

def main():


    #setup functions that the user can call, see below for ***Actions*** defined locally
    selections = [
        { 'fn':goodbye,                 'text': "Exit"},
        { 'fn':initialize_littleR,      'text': "Create file structure for littleR requirements."},
    ]

    while True:
        #prompt for the user input
        print_options(selections)

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
        except:
            print(f"Invalid option, please enter number from the list.")


def print_options(selections):
    print("\nChoose an option from the list. Enter the desired number.")
    for index,selected in enumerate(selections):
        print(f"[{index+1}]: {selected['text']}")

#*** Actions ***

def goodbye():
    print( "\nGoodbye." )

def initialize_littleR():
    littleR.helloworld.say_hello()
    print( "INIT" )


if __name__ == "__main__":
    main()