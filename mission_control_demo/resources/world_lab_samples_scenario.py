from mission_control.deeco_integration.simulation.scenario import Scenario
from mission_control.data_model.restrictions import Request
from .world_lab_samples import pickup_ihtn, poi


robot_facotrs = [{
    'id': 0, 
    'skills': ['approach_person', 'approach_robot', 'authenticate_person', 'deposit', 'navigation', 'operate_drawer', 'pick_up'], 
    'location': poi.pc_room_6.value,
    'battery_charge': 0.37,
    'battery_discharge_rate': 0.0011,
    'avg_speed': 0.15
    }, {
    'id': 1, 
    'skills': ['approach_person', 'approach_robot', 'authenticate_person', 'deposit', 'navigation', 'operate_drawer', 'pick_up'], 
    'location': poi.ic_room_5.value,
    'battery_charge': 0.04,
    'battery_discharge_rate':  0.0019,
    'avg_speed': 0.15
    }]

pickup_sample, _ =  pickup_ihtn(poi.pc_room_3.value)

fetch_sample_trial = Scenario(
    id=0,
    code='',
    nurses=[],
    factors=[],
    robots=robot_facotrs,
    requests= [
        Request(
            task=pickup_sample,
            timestamp=0)
        ]
    )
