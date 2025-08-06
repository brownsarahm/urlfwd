from typing import Dict
import yaml

def find_duplicate_keys(source_yaml):
    '''
    find any duplicated keys in the source yaml

    Parameters
    ----------
    source_yaml : string or file buffer
        file to parse

    Returns
    -------
    duplicates: list
        list of repeated keys; empty if none
    '''
    #yaml reading drops duplicates, keeps only the last one. 
    with open(source_yaml,'r') as f:
        yaml_dict = yaml.safe_load(f)

    with open(source_yaml,'r') as f:
        yaml_list = f.readlines()

    # lengths will match if well formated and no repeats
    if len(yaml_dict) ==len(yaml_list):
        return []
    else:
        key_list = [key_val.split(':')[0] for key_val in yaml_list]
        # cast to set removes duplicates
        duplicate_candidates = set([key for key in key_list if key_list.count(key) >1])
        # ignore any keys that start with a tab, these are subkeys
        duplicates = [dc for dc in list(duplicate_candidates) if not(dc.startswith((' ', '\t')))]
        return duplicates
    

def parse_yml(source_yaml, target_type='basic'):
    '''
    determine yaml formalt type and return a usable object

    Parameters
    ----------
    source_yaml : string or file buffer
        file to parse
    target_type : string
        'basic' for simple key: value pairs, 'informational' for key: {url: url, description: 'description'}
        if not specified, will return the type basic

    Returns
    -------
    duplicates: list
        list of repeated keys; empty if none
    '''
    #yaml reading drops duplicates, keeps only the last one. 
    with open(source_yaml,'r') as f:
        yaml_dict = yaml.safe_load(f)

    # check structure
    # acceptable is shortname: url
    # or shortname: {url: url, description: 'description'}
    
    # check if it has the right structure
    required_keys = ['url', 'description']
    for key, value in yaml_dict.items():
        if isinstance(value, str):

            continue
        elif isinstance(value, dict):
            # check that all requred keys are present
            if not all(req_key in value for req_key in required_keys):
                raise ValueError(f"Value for key '{key}' is a dict but does not contain " +
                                 f"all required keys: {required_keys}." +
                                 f" Found keys: {list(value.keys())}.")
            # check that url is present
        else:
            raise ValueError(f"Value for key '{key}' is not valid. Expected URL "+
                             f"for dict with key: {required_keys}, got {type(value)}.")
        
    types = {key: type(value) for key, value in yaml_dict.items()}
    if all(isinstance(value, str) for value in yaml_dict.values()) or target_type == 'basic':
        format = 'basic'
        parsed_dict = LinkListing(yaml_dict)
    elif all(isinstance(value, dict) and 'url' in value for value in yaml_dict.values()):
        format = 'informational'
        parsed_dict = FlyerListing(yaml_dict)
    else:
        format = 'mixed'
        parsed_dict = LinkListing({key: value['url'] if isinstance(value, dict) and 'url' in value else value 
                for key, value in yaml_dict.items()})
    
    
    return parsed_dict
    
    
# TODO: make this work to parse the tyeps and makethe flyer generation more smooth
class LinkListing(Dict):
    '''
    a dictionary that can be used to store links by short name
    names as keys, urls as values
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
    
class FlyerListing(Dict):
    '''
    a dictionary that can be used to store links and their descriptions
    names keys, value a dictionary with keys 'url' and 'description'
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

def add_link(new_url,new_name,yaml_file, force=False,return_dict =False):
    '''
    add a new key to the yaml file

    Parameters:
    -----------
    new_url : string
        URL to forward to, value in yaml file
    new_name: string
        short url to create, key in yaml file
    yaml_file : string or file buffer
        file to add to
    force: boolean
        if true change a value for an existing key
    '''


    with open(yaml_file,'r') as f:
        link_dict = yaml.safe_load(f)

    if  new_name in link_dict.keys():
        if not(force):
            message = new_name + ' exists, not creating'
            write = False
        else:
            message = new_name + ' exists, overwriting'
            write = True
    else:
        write = True
        message = ''

    if write: 
        link_dict[new_name] = new_url

        text_out = yaml.dump(link_dict)
        with open(yaml_file,'w') as f:
             f.write(text_out)

    if return_dict:
        return message, link_dict
    else:
        return message