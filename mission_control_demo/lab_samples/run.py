
import json
from pathlib import Path

from typing import List
from __init__ import *
from datetime import datetime


from mission_control.data_model.restrictions import Request
from mission_control.deeco_integration.simulation.sim_exec import SimExec
from mission_control.deeco_integration.simulation.scenario import Scenario
from mission_control.utils.logger import LogDir

from resources.world_lab_samples import all_skills, near_ic_pc_rooms, pickup_ihtn, get_position_of_poi, container

def gen_requests(times, locations):
    for time, location in zip(times, locations):
        task, _ = pickup_ihtn(location)
        yield location, Request(task=task, timestamp=time)
    return

def simp_factors_map(map):
    return map


def exp_gen_id():
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%H_%M_%S")
    print("Current Time =", current_time)
    return current_time

def main():
    ################
    # Initializations
    ####

    exp_id = exp_gen_id()
    new_experiment_path = f'executions/exec_{exp_id}'
    path = Path(f'{new_experiment_path}/tmp')
    path.mkdir(parents=True, exist_ok=True)
    LogDir.default_path = f'{new_experiment_path}/logs'


    ################
    # Configure scenario
    ####
    number_of_robots = 6
    number_of_users = 1

    # times in which a new request will appear in the trial
    request_times = [ 4000 ] # single request

    # set of requests
    requests = None
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

        # trailing positions are the position of nurses
        nurse_locations = near_ic_pc_rooms[number_of_robots: number_of_robots + number_of_users]

        # generate a request for each time
        requests = []
        nurses = []
        nurses_locations = []
        for location, request in gen_requests(request_times, nurse_locations):
            requests.append(request)
            nurses.append({ 'position': get_position_of_poi(location), 'location': location.label})
            nurses_locations.append(location)


    ################
    # create the scenario
    ##
    scenario = Scenario(id=1, code='scenario_1', factors='--',
        robots=set_of_robot_factors, 
        nurses= nurses,
        requests=requests)

    dump_scenarios([scenario], f'{new_experiment_path}/scenarios.json')
    ################
    # Prepare execution
    ####

    # create deeco sim env 
    sim_exec = get_sim_exec()
    # fire the sim!
    final_state = sim_exec.run(scenario, limit_ms=10000)
    # inspect end state
    print(final_state['missions'][0].occurances)
    for robot in scenario.robots:
        robot['position'] = get_position_of_poi(robot['location'])
        robot['location'] = robot['location'].label
        robot['skills'].sort()

    # delete non dict before writing to json
    delattr(scenario, 'requests')

    if any(final_state['local_plans']):
        print('the mission was planned for the request.')
    else:
        print('no plan was found!')

    # dump no planned trials for debug (ideally it is empty)
    with open(f'{new_experiment_path}/trial.json', 'w') as outfile:
        json.dump(scenario.__dict__, outfile, indent=4, sort_keys=True)

def get_sim_exec():
    return SimExec(container)


def repack(objiter, repacking_tupels):
    new = {}
    for key, value in objiter:
        _, fnc = next(filter(lambda item: item[0] == key, repacking_tupels), (None, None))
        new[key] = fnc(value) if fnc else value
    return new

def dump_scenarios(scenarios, path):    
    def repack_robots(robot):
        return repack(robot.items(),
            [('location', lambda location: location.label )])

    def scenrio_to_dump(scenario: Scenario):
        return repack(scenario.__dict__.items(),[ 
            ('nurse', lambda nurses: list(map( lambda nurse: nurse.location))),
            ('requests', 
                lambda requests: list(map( 
                        lambda request: { 
                            'timestamp': request.timestamp, 
                            'task': request.task.name }, requests            ) 
            )),
            ('robots', lambda robots: list(map(repack_robots, robots )))
        ])

    sceratios_to_dump = list(map(scenrio_to_dump, scenarios))
    with open(path, 'w') as outfile:
        json.dump(sceratios_to_dump, outfile, indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
