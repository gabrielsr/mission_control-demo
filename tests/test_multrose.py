
import os
import json 

from mutrose.mutrose_json_parser import MultroseJson, filter_node_by_type, init_role_map
from hospital_world.bindings import world_model_domain

script_dir = os.path.dirname(__file__)



def resources_path(path):
    return os.path.join(script_dir, 'multrose_json', path)

def test_init_role_map():
    path = resources_path('ihtn_lsl.json')
    data = json.load(open(path))
    role_map = init_role_map(data)
    assert role_map['r1'].label == 'r1'

def test_parse_simple_action():
    parser = MultroseJson(resources_path('operate_drawer-close.json'), world_model_domain)
    parser._load_json()
    action = parser.parse_action(parser.data.get('0'))
    assert action

def test_parse_method():
    parser = MultroseJson(resources_path('sample-unload-method.json'), world_model_domain)
    parser._load_json()
    node = parser.data.get('17')
    method = parser.parse_method(node)
    assert len(method.subtasks) == 3
    
def test_create_action_dict():
    path = resources_path('ihtn_lsl.json')
    data = json.load(open(path))
    actions = dict(filter_node_by_type(data, 'action'))
    assert len(actions) == 11

def test_multrose():
    with MultroseJson(resources_path('ihtn_lsl.json'), world_model_domain) as ihtn:
        assert ihtn.name == 'ROOT'

