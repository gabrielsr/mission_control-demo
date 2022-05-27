from functools import reduce
import operator

from typing import List
from mission_control.data_model import Method, ElementaryTask, AbstractTask
from mission_control.data_model import POI, Role
from enum import Enum

from mission_control.data_model import WorldModelDomain

import json

def ihtn_from_json(json_file_path):
    file = open(json_file_path,)
    data = json.load(file)
    root = recursive_ihtn_gen(data, "0")
    return root

def init_role_map(data: dict):
    role_labels_lists = map(lambda n: set(n["agents"]), data.values()) # get agents of each node
    role_labels = reduce(operator.or_, role_labels_lists)
    
    def get_role(a):
        return Role(a) if a.startswith('r') else Role(a, Role.Type.NOT_MANAGED)

    return dict(zip(role_labels, map(get_role, role_labels))) # instantiate

def filter_node_by_type(nodes, *types):
    for k, n in nodes.items():
        if n["type"] in types:
            yield k, n
            
def create_map_of_parsed_nodes(filtered_nodes, parse_fnc):
    filtered_dict = dict(filtered_nodes)
    return dict(zip(
        filtered_dict.keys(),
        map(parse_fnc, filtered_dict.values())))
        
class MultroseJson:
    def __init__(self, path, world_model: WorldModelDomain):
        self.file_path = path
        self.world_model = world_model

    def parse_data(self):
        # initial setup        
        return self.parse_root()

    def get_role(self, agent_label):
        return self.role_map[agent_label]

    def parse_root(self):
        return self.parse_task(self.data.get('0'))

    def parse_action(self, node):
        # TODO improve parse
        action_name = node["name"]
        pos = action_name.find("-")

        action_task_type = ""
        action_action = ""
        if pos != -1:
            action_task_type = action_name[:pos]
            action_action = action_name[pos+1:]
        else:
            action_task_type = action_name

        destination = None

        task_type = self.world_model.get(action_task_type, "task_type")

        if node["locations"]:
            destination = self.world_model.get(node["locations"][0], "location")

        assign_to = list(map(lambda a: self.role_map.get(a), node["agents"]))

        if action_action == "":
            a = ElementaryTask(type=task_type, destination=destination, assign_to=assign_to, name=action_name)
        else:
            a = ElementaryTask(type=task_type, destination=destination, action=action_action, assign_to=assign_to, name=action_name)

        return a

    def parse_method(self, node):
        def acc_child(acc_list: List, child_id):
            if self.elementary_tasks_map.get(child_id):
                acc_list.append(self.elementary_tasks_map.get(child_id))
            else:
                acc_list.append(self.parse_task(self.data.get(child_id)))
            return acc_list

        method_subtasks = reduce(acc_child, node["children"], [])
        m = Method(subtasks = method_subtasks)
        m.name = node["name"]
        return m
    
    def parse_task(self, node):
        def acc_child(acc_list: List, child_id):
            acc_list.append(self.parse_method(self.data.get(child_id)))
            return acc_list
        
        methods = reduce(acc_child, node["children"], [])
        return AbstractTask(methods = methods, name=node['name'])
    
    def _load_json(self):
        self.file = open(self.file_path, 'r')
        self.data: dict = json.load(self.file)
        self.file.close()

        # instantiate Roles
        self.role_map:List[Role] = init_role_map(self.data)

        # instantiate leaf tasks
        self.elementary_tasks_map = create_map_of_parsed_nodes(
            filter_node_by_type(self.data, 'action'),
            self.parse_action)

    def __enter__(self):
        self._load_json()
        return self.parse_data()
        
    def __exit__(self, exc_type, exc_value, traceback):
        print(exc_type)



def recursive_ihtn_gen(data, key):
    """ 
    mutrose json is a set of key: nodes,
    in which each key is an integer.
    and each node is either an task (abstract), method or action
    """
    node = data[key]
    node_type = data[key]["type"]



    # match node_type:
    #     case "task":
    #     return parse_task_node
    # elif data[key]["type"] == "method":
    #     method_subtasks = []

    #     for child in data[key]["children"]:
    #         subtask = recursive_ihtn_gen(data, child)
    #         method_subtasks.append(subtask)
        
    #     m = Method(subtasks = method_subtasks)
    #     return m
    # elif data[key]["type"] == "action":
    #     action_name = data[key]["name"]

    #     pos = action_name.find("-")

    #     action_task_type = ""
    #     action_action = ""
    #     if pos != -1:
    #         action_task_type = action_name[:pos]
    #         action_action = action_name[pos+1:]
    #     else:
    #         action_task_type = action_name
        
    #     destination = data[key]["locations"]
        
    #     if len(destination) > 0:
    #         destination = destination[0]

    #     agents = data[key]["agents"]

    #     assignees = []
    #     for a in agents:
    #         if a.startswith('r'):
    #             assignees.append(Role(a))
    #         else:
    #             assignees.append(Role(a, Role.Type.NOT_MANAGED))

    #     if action_action == "":
    #         a = ElementaryTask(type=action_task_type, destination=POI(destination), assign_to=[a for a in assignees], name=data[key]['name'])
    #     else:
    #         a = ElementaryTask(type=action_task_type, destination=POI(destination), action=action_action, assign_to=[a for a in assignees], name=data[key]['name'])

    #     return a