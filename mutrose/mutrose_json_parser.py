from mission_control.data_model import Method, ElementaryTask, AbstractTask
from mission_control.data_model import POI, Role
from enum import Enum
import json

def ihtn_from_json(json_file_path):
    file = open(json_file_path,)
    data = json.load(file)
    root = recursive_ihtn_gen(data, "0")
    return root

def recursive_ihtn_gen(data, key):
    if data[key]["type"] == "task":
        task_methods = []

        for child in data[key]["children"]:
            child_method = recursive_ihtn_gen(data, child)
            task_methods.append(child_method)

        t = AbstractTask(methods = task_methods, name=data[key]['name'])
        return t
    elif data[key]["type"] == "method":
        method_subtasks = []

        for child in data[key]["children"]:
            subtask = recursive_ihtn_gen(data, child)
            method_subtasks.append(subtask)
        
        m = Method(subtasks = method_subtasks)
        return m
    elif data[key]["type"] == "action":
        action_name = data[key]["name"]

        pos = action_name.find("-")

        action_task_type = ""
        action_action = ""
        if pos != -1:
            action_task_type = action_name[:pos]
            action_action = action_name[pos+1:]
        else:
            action_task_type = action_name
        
        destination = data[key]["locations"]
        
        if len(destination) > 0:
            destination = destination[0]

        agents = data[key]["agents"]

        assignees = []
        for a in agents:
            if a.startswith('r'):
                assignees.append(Role(a))
            else:
                assignees.append(Role(a, Role.Type.NOT_MANAGED))

        if action_action == "":
            a = ElementaryTask(type=action_task_type, destination=POI(destination), assign_to=[a for a in assignees], name=data[key]['name'])
        else:
            a = ElementaryTask(type=action_task_type, destination=POI(destination), action=action_action, assign_to=[a for a in assignees], name=data[key]['name'])

        return a