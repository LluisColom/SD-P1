# -------------------------------------- #										 
# Programador: David Nada Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #

import xmlrpc.client
import os

# ---------------------------- Connex Establishment ----------------------------- #
s = xmlrpc.client.ServerProxy('http://localhost:8005')

TASKS_ID = []

#---------------------------------- SWITCH OPTIONS ------------------------------ #

def choose_task():
    #check num workers.
    print ("******************************************")
    print ("*                                        *")
    print ("*               Submit task              *")
    print ("*                                        *")
    print ("******************************************\n")

    function_name = input("Type the function to be executed: (wordCount) (countWords) ")
    function_args = input("Enter the task arguments separated by a ' ': ")
    print ("Submitting task, please wait...")
    job_id = s.submit_task(function_name,function_args)
    print("Your task is being processed by the cluster. Use its job_id: ",job_id," to get the result once finished.")
    if job_id is not None:
        TASKS_ID.append(job_id)

def read_result():
    print ("\n*************** Read result **************")
    print ("Created tasks (shown by ID):")
    for tsk in TASKS_ID:
        print(tsk)
    
    selected = input ("\nChoose the task ID which you want to know the result: ")
    ret_val = s.check_result(selected)
    if ret_val is not None:
        print("\nThe result of task with id ",selected," is:\n",ret_val)
    else:
        print("\nError: no found job in the DB with id: ",selected,". It is possible that the task has not finished yet.")

def invalid_option():
    print ("******************************************")
    print ("*                                        *")
    print ("*            Invalid Option              *")
    print ("*                                        *")
    print ("******************************************\n")
    print("Please, select a valid option.\n")

def add_worker():
    print ("******************************************")
    print ("*                                        *")
    print ("*               Add Worker               *")
    print ("*                                        *")
    print ("******************************************\n")
    print(s.add_worker())

def rem_worker():
    print ("******************************************")
    print ("*                                        *")
    print ("*             Remove Worker              *")
    print ("*                                        *")
    print ("******************************************\n")

    print ("Active worker IDs:")
    print(s.list_worker())
    print("\nWrite the IDs of the target workers (separated by space):")
    target = input()

    print(s.remove_worker(target))    #Falta argument.

def print_workers():
    print ("******************************************")
    print ("*                                        *")
    print ("*              List Worker               *")
    print ("*                                        *")
    print ("******************************************\n")
    print(s.list_worker())

switch_options = {
    '1': choose_task,
    '2': add_worker,
    '3': print_workers,
    '4': rem_worker,
    '5': read_result
}

def wipe_screen():
    os.system('clear')

#---------------------------------------- MAIN -----------------------------------#

def show_menu():
    print ("******************************************")
    print ("*                                        *")
    print ("*           Welcome to Cluster           *")
    print ("*                                        *")
    print ("******************************************")
    print ("*                                        *")
    print ("* Which action do you want to perform?   *")
    print ("*  0 - Exit.                             *")
    print ("*  1 - Submit a task.                    *")
    print ("*  2 - Add worker.                       *")
    print ("*  3 - List workers.                     *")
    print ("*  4 - Remove worker.                    *")
    print ("*  5 - Read task result.                 *")
    print ("*                                        *")
    print ("******************************************")

choice = -1
while (choice != 0):
    
    show_menu()
    choice = input('Your choice: ')
    wipe_screen()

    switch_options.get(choice, invalid_option)()
    input('\nPress any key to continue...')
    wipe_screen()

print("Shutting down...")