
import json
import os
from pathlib import Path
from datetime import datetime


from mission_control.data_model import Request
from mission_control.deeco_integration.simulation.scenario import Scenario
from mission_control_demo.setup_scenario_and_dump import setup_scenario_and_run
from mutrose.mutrose_json_parser import MultroseJson

from hospital_world.bindings import all_skills, near_ic_pc_rooms, get_position_of_poi, hospital_map, world_model_domain, container
from hospital_world.lab_samples_mission import pickup_ihtn

def gen_requests(times, locations):
    for time, location in zip(times, locations):
        task, _ = pickup_ihtn(location)
        yield Request(task=task, timestamp=time)
    return

if __name__ == '__main__':
    ################
    # Configure scenario
    ####
    number_of_robots = 1
    number_of_users = 1

    # robots
    set_of_robot_factors = []
    for robot_index in range(number_of_robots):
        #each robot
        robot_facotrs = {
            'id': (robot_index + 1), 'name': f'r{(robot_index + 1)}',
            'location':near_ic_pc_rooms[ robot_index ], # select the first positions, improve according experimental goals
            'skills': all_skills, # every robot have every skill
            'battery_charge':  1,
            'battery_discharge_rate': 0.0002,
            'avg_speed': 0.15
        }
        set_of_robot_factors.append(robot_facotrs)

    # nurses
    # trailing positions are the position of nurses
    nurse_locations = near_ic_pc_rooms[number_of_robots: number_of_robots + number_of_users]
    request_times = [ 4000 + t * 1000 for t in range(number_of_users) ] # request start at 4000 and is 1000 apart
    # generate a request for each time
    requests = list(gen_requests(request_times, nurse_locations))

    # generate a request for each time
    nurses = [{'label': 'nurse', 'position': get_position_of_poi(location), 'location': location.label } for location in nurse_locations]

    ################
    # create the scenario
    ##
    scenario = Scenario(id=1, 
        experiment_code='mc_lab_samples',
        code='scenario_1', factors='--',
        robots=set_of_robot_factors, 
        persons= nurses,
        requests=requests)

    setup_scenario_and_run(scenario, container)
