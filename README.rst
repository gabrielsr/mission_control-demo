====================
mission_control_demo
====================
A exemplar project of how to use mission_control with pyDEEco to create simulation and generated mission plans.

Setup
-----

This project uses 'poetry' for mananing dependencies 

.. code:: bash

    # install
    ~$ pip install poetry
    # Or
    ~$ brew install poetry
    # then use poetry to install dependencies
    ~$ poetry install
    # and configure a virtual environment
    ~$ poetry shell


Run
---

./mission_control_demo/lab_samples

is an example of simulation. To run:

.. code:: bash
    
    ~$ python ./mission_control_demo/lab_samples/run.py
    ~$ python ./mutrose/lab_samples/run.py


The are already configured 'Launch' actions for vscode, which can be used for execution/debuging.

Result
------

After executing the demo, a folder will be generated in 'new'

/executions/exec_{}
|_logs/cf_request_x.log ->  a file for each coalition formation process for each received request
|_scenarios.json  ->  the initial configuration of the simulation
|_trial.json  ->  the end state of the simulation, with a plan assigned to a robot if the case a plan was found