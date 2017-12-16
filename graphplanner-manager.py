#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import os.path 
import pyparsing
import re
import collections
from subprocess import Popen, PIPE


# returns ops-file contents. If there is a previous tmp ops-file, gets that instead
def read_file():
    if(os.path.isfile("ops_test.tmp")):
        f = open("ops_test.tmp", "r")
    else:
        f = open("ops_test.txt", "r")
    
    content = f.read()
    start = content.find('(')
    return content[start:]

    
# returns a key:value structure, having the op name as the key, and the raw op as the value
def get_tasks():
    f_content = read_file()
    tasks_array = f_content.split("\n\n")
    
    tasks = {}

    thecontent = pyparsing.Word(pyparsing.alphanums) | '<' | '>' | '-'
    parens = pyparsing.nestedExpr('(', ')', content=thecontent)

    for task in tasks_array:
        try:
            task_raw_struct = parens.parseString(task)
            task_name = task_raw_struct[0][1]
            
            tasks[task_name] = task
            
        except pyparsing.ParseException:
            print("Ops file syntax error. Check the following OP:")
            print
            print(task)
            exit(1)
    
    return collections.OrderedDict(sorted(tasks.items()))
    
    
# creates tmp ops-file (if not exists)
def tmp_task_file():

    if(not os.path.isfile("ops_test.tmp")):
        f_content = ""
        
        tasks = get_tasks()
        
        for task_name,task_raw in tasks.items():
            f_content += task_raw + "\n\n"
        
        f = open("ops_test.tmp", "w")
        f.write(f_content[:-2]) # removes extra \n\n

        
# set task_name as a failed task and then returns the raw ops-structure without it
def failed_task(failedtask_name):
    f_content = ""
    
    tasks = collections.OrderedDict(sorted(get_tasks().items()))
    
    for task_name,task_raw in tasks.items():
        if(task_name != failedtask_name):
            f_content += task_raw + "\n\n"
    
    f = open("ops_test.tmp", "w")
    f.write(f_content[:-2]) # removes extra \n\n


# returns the task list that can be done at each step
def parse_plan(rawPlan):
    plan = rawPlan.split("\n")    
    plan_regex = re.compile('^([0-9]+) ([^_]+)_.*$')
    
    plan_steps = {}
    
    for step in plan:
        m = plan_regex.match(step)
        
        if(m.group(1) in plan_steps):
            plan_steps[m.group(1)] += [m.group(2)]
        else:
            plan_steps[m.group(1)] = [m.group(2)]
    
    return collections.OrderedDict(sorted(plan_steps.items()))
    
    
# call graphplan planner and get output
def call_planner():
    tmp_task_file()
    #failed_task("t7")
    
    process = Popen(["cmu-graphplan/graphplan", "-o", "ops_test.tmp", "-f", "tasks_facts.txt", "-d"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    
    if(output.find("Problem not solvable") > 0):
        print("NO SOLUTION")
        
    elif(output.find("goals at time") > 0):
        print("GOAL")
        indexStart = output.find("goals at time")
        indexStart = output.find("\n\n", indexStart)
        indexEnd = output.find("entries in hash table", indexStart)
        
        plan = parse_plan(output[indexStart+2:indexEnd-3])
        
        for step,task_list in plan.items():
            print(task_list)
           
    else:
        print("CALL_PLANNER ERROR")

    
call_planner()