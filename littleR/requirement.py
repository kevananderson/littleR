
class Requirement:

    def __init__(self,requirement_dictionary=None, file=None):
        #set default values for all fields
        self.file = file

        self.enabled = True

        self.index = ""
        self.type = ""
        self.title = ""
        self.requirement = ""
        self.description = ""
        self.assumptions = ""

        self.component = ""
        self.label = []
        
        #lists of indexes
        self.parent_idx = []
        self.child_idx = []
        self.related_idx = []
        
        #lists of requirements, linked later
        self.parent = []
        self.child = []
        self.related = []
        
        #we are done if no dictionary is provided
        if requirement_dictionary is None:
            return
        
        #fill in values from the dictionary
        
        #index
        if 'index' in requirement_dictionary:
            self.index = requirement_dictionary['index']

        #type
        if 'type' in requirement_dictionary:
            self.type = requirement_dictionary['type']
        
        #title
        if 'title' in requirement_dictionary:
            self.title = requirement_dictionary['title']

        #requirement
        if 'requirement' in requirement_dictionary:
            self.requirement = requirement_dictionary['requirement']

        #description
        if 'description' in requirement_dictionary:
            self.description = requirement_dictionary['description']
        
        #assumptions
        if 'assumptions' in requirement_dictionary:
            self.assumptions = requirement_dictionary['assumptions']

        #component
        if 'component' in requirement_dictionary:
            self.component = requirement_dictionary['component']

        #label
        if 'label' in requirement_dictionary:
            for label in requirement_dictionary['label']:
                if label not in self.label:
                    self.label.append(label)

        #parent_idx
        if 'parent_idx' in requirement_dictionary:
            for parent_idx in requirement_dictionary['parent_idx']:
                if parent_idx not in self.parent_idx:
                    self.parent_idx.append(parent_idx)
        
        #child_idx
        if 'child_idx' in requirement_dictionary:
            for child_idx in requirement_dictionary['child_idx']:
                if child_idx not in self.child_idx:
                    self.child_idx.append(child_idx)

        #related_idx
        if 'related_idx' in requirement_dictionary:
            for related_idx in requirement_dictionary['related_idx']:
                if related_idx not in self.related_idx:
                    self.related_idx.append(related_idx)


    def valid_index(index):
        '''checks if the index is valid

        Args:
            index (str): the index to check
                         index is a string in the format r00000000

        Returns:
            bool: True if the index is valid, False otherwise
        '''
        if len(index) != 9:
            return False
        if index[0] != 'r':
            return False
        if not index[1:].isdigit():
            return False
        idx = Requirement.int_index(index)
        if idx is None:
            return False
        return True

    def int_index(index):
        '''converts the index to an integer value

        Args:
            index (str): the index to convert to an integer
                         index is a string in the format r00000000

        Returns:
            int: the integer value of the index
            None: if the index is not valid
        '''
        try:
            return int(index[1:])
        except:
            return None
        
        



    def __str__(self):

        return f"Requirement({self.index})"