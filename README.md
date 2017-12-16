# GraphPlan Manager

The GraphPlan Manager is a dynamic ops manager (listed in ops file).

It gets the ops file as is, and generates a new one removing the failing ops (if there). When the new status is saved, the manager runs the planner in order to get a new -alternative- plan (if there is one)

## Previous considerations

In order to get this to work, you must first compile your own graphplan binary. Check the [cmu-graphplan](https://github.com/juan-vg/cmu-graphplan) project to do so. Once done, copy the executable to the _cmu-graphplan_ directory in this repository

## Exec example (on Linux)

    ~/plan-manager$ python graphplanner-manager.py
