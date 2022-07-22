====================
mission_control_demo
====================
A exemplar project of how to use mission_control with pyDEEco to create simulation and generated mission plans.

Setup
=====

This project uses 'poetry' for mananing dependencies 

.. code:: bash

    # install poetry [https://python-poetry.org/]
    # then use poetry to install dependencies
    ~$ poetry install
    # and configure a virtual environment in your shell
    ~$ poetry shell

Importing hmrs_mission_control by code
-----------------------------------

Run side by side with 'hmrs_mission_control' code for fixing bugs in it and debuging.

.. code:: bash

    # path considering both projects are in the same folder
    ~$ pip install -e ./hmrs_mission_control


Run
===

./mission_control_demo/lab_samples

is an example of simulation. To run:

.. code:: bash
    # within poetry shell
    ~$ python ./mission_control_demo/lab_samples/run.py
    ~$ python ./mutrose/lab_samples/run.py
    ~$ python ./mutrose/food_logistics/run_fld.py
    ~$ python ./mutrose/food_logistics/run_flp.py


The are already configured 'Launch' actions for vscode, which can be used for execution/debuging.

Result
------

After executing the demo, a folder will be generated in */executions*:

.. code:: bash
    
    /executions/exec_{}
    |_logs/cf_request_x.log # a file for each coalition formation process for each received request
    |_scenarios.json        # the initial configuration of the simulation
    |_trial.json            # the end state of the simulation, with a plan assigned to a robot if the case a plan was found
