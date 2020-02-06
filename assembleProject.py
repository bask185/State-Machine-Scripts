#!/usr/bin/python

import os
import shutil, errno

def getStateMachines(type) : # function tested!
    Files = []
    if type == "main":
        type = ".\mainStateMachines"
    else:
        type = ".\\nestedStateMachines"

    for root, dirs, fileList in os.walk(".", topdown=False):
        if root == type :
            Files = fileList
            
    string = []
    for file in Files:
        string.append(file[:-8])
    return string


def moveStateMachines(_src, _dest):
    src = _src
    dest = _dest
    for src_dir, dirs, files in os.walk(src):
        #print(dst_dir)
        dst_dir = src_dir.replace(src, dest, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            if "graphml" in src_file:
                shutil.copy(src_file, "yEd_stateMachines_repo")
                shutil.move(src_file, dst_dir + "/stateDiagrams") # make me move
            else:
                shutil.move(src_file, dst_dir) # make me move

def assembleTimersTab():
    stateMachineList = []

    with open("timers.tab", "w") as timers:
        for machine in stateMachines:
                timers.write(machine + "T\t10\n")
        # if errorHandler == 1:
        #     timers.write("errorT\t2\n")
        # if lightHandler == 1:
        #     timers.write("lightHandlerT\t100\n")
        timers.close()

def copyAllFiles():
    shutil.copy("updateTimers.py"   , folder)
    shutil.move("timers.tab"        , folder)
    shutil.copy("updateIO.py"       , folder)
    shutil.copy("io.tab"            , folder)

def assembleMain():
    folder2 = folder[2:]
    with open(folder + "/" + folder2 + ".ino", "w") as main:             #main.c
        main.write('#include "src/basics/timers.h"\n')
        main.write('#include "roundRobinTasks.h"\n')
        #main.write('#include " .h"\n') #fill in custom libraries
        #main.write('#include " .h"\n')    
        
        for machine in stateMachines:
            main.write('#include "' + machine + '.h"\n\n\n')
            
        main.write("void setup() {\n")
        main.write("\tinitTimers();\n")
        for machine in stateMachines:
            main.write("\t" + machine + "SetState(" + machine + "IDLE);\n")
        main.write("}\n\n")

        main.write("void loop() {\n")
        main.write("\tprocessRoundRobinTasks();\n\n")
        
        for machine in stateMachines:
            main.write("\t" + machine + "();\n")
        main.write("}")
        main.close()

def assembleRoundRobinTasks():
    with open(folder + "/roundRobinTasks.cpp", "w") as rr:
        rr.write("""
#include "roundRobinTasks.h"
#include "src/basics/io.h"

extern void processRoundRobinTasks(void) {
	static unsigned char taskCounter = 0;

// HIGH PRIORITY ROUND ROBIN TASKS
	//readSerialBus();
	//updateIO();

// LOW PRIORITY ROUND ROBIN TASKS
	taskCounter ++;
	switch(taskCounter) {
		default: taskCounter = 0;

		case 0:
		/* fill in a task */
		break;

		case 1:
		/* fill in a task */
		break;""")

        rr.write(" } }")
        rr.close()


    with open(folder + "/roundRobinTasks.h", "w") as rr:
        rr.write("void processRoundRobinTasks();\n")
        rr.write("#define updateIO(); updateOutputs(); \\\n")
        rr.write("updateInputs();")
        rr.close()

def createFolders():
    folder = "../" +input("Type name of new project\n")
    try:
        os.makedirs(folder)
        os.makedirs(folder + "/src")
        os.makedirs(folder + "/src/modules")
        os.makedirs(folder + "/src/basics")
        os.makedirs(folder + "/stateDiagrams")
        return folder
    except OSError:
        print("ERROR FOLDER EXISTS")
        pass


### BEGIN SCRIPT ###

folder = createFolders()

stateMachines = getStateMachines("nested") #GENERATE ALL NESTED STATE MACHINES
for machine in stateMachines:
    os.system("python.exe stateMachineGenerator.py " + machine + ".graphml" + " nested")

stateMachines = getStateMachines("main")   #GENERATE ALL MAIN STATE MACHINES
for machine in stateMachines:
    os.system("python.exe stateMachineGenerator.py " + machine + ".graphml" + " main")

moveStateMachines("nestedStateMachines", folder)

moveStateMachines("mainStateMachines", folder)

assembleTimersTab()

copyAllFiles()

assembleMain()

assembleRoundRobinTasks()

os.chdir(folder)
os.system("python.exe updateTimers.py")
os.system("python.exe updateIO.py")

### END SCRIPT ###
