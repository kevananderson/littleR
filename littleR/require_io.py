import os
import ruamel.yaml
from requirement import Requirement

class RequireIO:
    def __init__(self, path):
        self.path = path

    def read(self):
        #get all requirement files in the path
        req_files = self._get_requirement_files()
        
        #get the raw requirements from the files
        requirements = self._get_raw_requirements(req_files)
        
        #find all the new requirements
        
        #make sure all the requirements are valid

        #link the requirements together





    def write(self, data):
        with open(self.path, 'w') as f:
            f.write(data)
    
    def _get_requirement_files(self):
        req_files = []
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith('.yaml') and file != 'config.yaml':
                    req_files.append(os.path.join(root, file))
        return req_files
    
    def _get_raw_requirements(self, req_files):
        #initialize yaml parser
        yaml = ruamel.yaml.YAML()
        
        #initialize list to hold the requirements
        requirements = []

        #for each file, read it and parse it into requirements, storing them in the list
        for req_file in req_files:
            data = None
            with open(req_file, 'r') as file:
                data = yaml.load(file)

            if data is not None:
                for key, value in data.items():
                    value['index'] = key
                    requirement = Requirement(value, req_file)
                    
                    if requirement is not None:
                        requirements.append(requirement)

    def _get_config(self):
        '''returns a dictionary of the config file
        
        Returns:
            dict: the config file as a dictionary

        Raises:
            FileNotFoundError: if the config file does not exist
        '''
        config_path = os.path.join(self.path, 'config.yaml')
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(f'LittleR config file not found at {config_path}')
        
        yaml = ruamel.yaml.YAML()
        with open(config_path, 'r') as file:
            config = yaml.load(file)
        
        return config
            
    def __str__(self):
        return f'RequireIO({self.path})'
    
    def __repr__(self):
        return f'RequireIO({self.path})'