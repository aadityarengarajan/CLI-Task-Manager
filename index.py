#!/usr/bin/env python

"""
                                                                                                                                                     
   _|_|_|  _|        _|_|_|      _|_|_|_|_|                    _|            _|      _|                                                              
 _|        _|          _|            _|      _|_|_|    _|_|_|  _|  _|        _|_|  _|_|    _|_|_|  _|_|_|      _|_|_|    _|_|_|    _|_|    _|  _|_|  
 _|        _|          _|            _|    _|    _|  _|_|      _|_|          _|  _|  _|  _|    _|  _|    _|  _|    _|  _|    _|  _|_|_|_|  _|_|      
 _|        _|          _|            _|    _|    _|      _|_|  _|  _|        _|      _|  _|    _|  _|    _|  _|    _|  _|    _|  _|        _|        
   _|_|_|  _|_|_|_|  _|_|_|          _|      _|_|_|  _|_|_|    _|    _|      _|      _|    _|_|_|  _|    _|    _|_|_|    _|_|_|    _|_|_|  _|        
                                                                                                                             _|                      
                                                                                                                         _|_|                        
CLI Based Task Management Solution
BY AADITYA RENGARAJAN
CREATION TIMESTAMP : 22:38 12/21/21 21 12 2021
[TO-DO]
"""
#==============IMPORTING MODULES======================================================
import sys, os
#==============DEFINING BASIC FUNCTIONS===============================================
def helpme():
  '''
  HelpMe function to print usage and help
  '''
  print("""
$ ./task help
Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics""")
def getIndexed():
    with open("task.txt") as taskfile:
      tasks = taskfile.read().split("\n")
    taskss = []
    for i in tasks:
      if i.strip()!="":
        taskss.append(i.strip())
    tasks = taskss
    the_tasks = []
    for i in tasks:
      the_tasks.append({"priority":int(i.split(" ")[0]),"description":" ".join(i.split(" ")[1:])})
    tasks = sorted(the_tasks, key = lambda i: i['priority'])
    index=0
    indexed = []
    for i in tasks:
      index+=1
      indexed.append({"index":index,'description':i['description'],"priority":i['priority']})
    return indexed
def getCompleted():
    with open("completed.txt") as taskfile:
      tasks = taskfile.read().split("\n")
    taskss = []
    for i in tasks:
      if i.strip()!="":
        taskss.append(i.strip())
    tasks = taskss
    return tasks
#==============ERROR HANDLING======================================================
if "task.txt" not in os.listdir():
  with open("task.txt","w"):
    pass
if "completed.txt" not in os.listdir():
  with open("completed.txt","w"):
    pass
#==============MAIN SCRIPT======================================================
arg_lst = list(sys.argv)[1:]
if len(arg_lst) == 0:
  helpme()
if (len(arg_lst) == 1):
  if (arg_lst[0] == "help"):
    helpme()
  if (arg_lst[0] == "ls"):
    for i in getIndexed():
      print(f"{i['index']} {i['description']} [{i['priority']}]")
  if (arg_lst[0] == "report"):
    print("Pending :",len(getCompleted()))
    index = 0
    for i in getCompleted():
      index+=1
      print(f"{index}. {i}")
    print("\nCompleted :",len(getIndexed()))
    for i in getIndexed():
      print(f"{i['index']}. {i['description']}")
if "add" in arg_lst:
  priority = arg_lst[-2]
  task = arg_lst[-1]
  with open("task.txt","a+") as file:
    file.write(str("\n"+f"{priority} {task}"))
    file.seek(0)
    filecontent = file.read()
  with open("task.txt","w") as file:
    file.write(filecontent.replace("\n\n","\n"))
  print(f"Added task: \"{task}\" with priority {priority}")
if "del" in arg_lst:
    delindex = int(arg_lst[-1])
    indexed = getIndexed()
    finaltasks = []
    deleted = False
    for i in indexed:
      if i["index"]!=delindex:
        finaltasks.append({"priority":i["priority"],"description":i["description"]})
      else:
        deleted = True
    if deleted==False:
      print(f"Error: item with index {delindex} does not exist. Nothing deleted.")
    else:
      with open("task.txt","w") as file:
        file.write("\n".join(list(f"{i['priority']} {i['description']}" for i in finaltasks)))
      print(f"Deleted item with index {delindex}")
if "done" in arg_lst:
    doneindex = int(arg_lst[-1])
    indexed = getIndexed()
    done = False
    for i in indexed:
      if i["index"] == doneindex:
        with open("completed.txt","a+") as file:
          file.write(str("\n"+i["description"]))
          file.seek(0)
          filecontent = file.read()
        with open("completed.txt","w") as file:
          file.write(filecontent.replace("\n\n","\n"))
        done = True
    if done==False:
      print(f"Error: no incomplete item with index {doneindex} exists.")
    else:
      finaltasks = []
      for i in indexed:
        if i["index"]!=doneindex:
          finaltasks.append({"priority":i["priority"],"description":i["description"]})
      else:
        with open("task.txt","w") as file:
          file.write("\n".join(list(f"{i['priority']} {i['description']}" for i in finaltasks)))
#==============END OF SCRIPT======================================================
#/- COMPLETION TIMESTAMP : 11:10 01/16/22 16 01 2022 -/#