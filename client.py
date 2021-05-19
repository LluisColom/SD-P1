# -------------------------------------- #										 #
# Programador: David Nada Fernandez		 #
# Programador: Lluís Oriol Colom Nichols #
# -------------------------------------- #
#from master import add_worker, submit_task
import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8005',verbose=True)

def show_menu():
    print ("* Which action do you want to perform?   *")
    print ("*  1 - Submit a task to the cluster.     *")
    print ("*  2 - Add worker.                       *")
    print ("******************************************")

def choose_task():
    print ("\n*************** Submit task **************")
    function_name = input("Type the function to be executed: (WordCount) (CountWords) ")
    function_args = input("Enter the task arguments separated by a ';' :")
    print ("Submitting task, please wait...")
    job_id = s.submit_task(function_name,function_args)
    print("Your task is being processed by the cluster. Use its job_id: ",job_id," to get the result once finished.")

def get_cluster_workers():
    pass

def invalid_option():
    print ("Please, select a valid option.\n")

switch_options = {
    '1': choose_task,
    '2': s.add_worker
}

print ("*********** Welcome to Cluster ***********")
print ("*                                        *")
kill_program = 0
while (kill_program == 0):
    
    show_menu()
    choice = input('Your choice: ')

    switch_options.get(choice, invalid_option)()
