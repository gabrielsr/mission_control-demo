from datetime import datetime
import json
from pathlib import Path
from hospital_world.bindings import get_position_of_poi
from mission_control_demo.sim_exec import SimExec
from mission_control.deeco_integration.simulation.scenario import Scenario
from mission_control.utils.logger import LogDir
from mission_control_demo.sim_exec import SimExec

# def get_sim_exec():
#     return SimExec(container)


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



def exp_gen_id():
    now = datetime.now()
    current_time = now.strftime("%Y_%m_%d_%H_%M_%S")
    print("Current Time =", current_time)
    return current_time

def setup_scenario_and_run(scenario: Scenario, container):
    ################
    # Initializations
    ####

    # folder
    exp_id = exp_gen_id()
    new_experiment_path = f'executions/exe_{scenario.experiment_code}_{exp_id}'
    path = Path(f'{new_experiment_path}/tmp')
    path.mkdir(parents=True, exist_ok=True)
    LogDir.default_path = f'{new_experiment_path}/logs'

    # dump scenario (i.e., setup parameters)
    dump_scenarios([scenario], f'{new_experiment_path}/scenarios.json')
    ################
    # Prepare execution
    ####

    # create deeco sim env 
    sim_exec = SimExec(container)
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
