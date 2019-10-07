#!/usr/bin/python3

import subprocess
import secrets
import string
import sys
import json
import random

machines = ["1uuidSender-tf", "2uuidSender-tf", "recieverWebServer-tf"]
senders = ["1uuidSender-tf", "2uuidSender-tf"]
recievers = ["recieverWebServer-tf"]
kbCluster = ["1uuidSender-kbClus-mast", "2uuidSender-kbClus", "3uuidSender-kbClus"]
kbMaster = ["1uuidSender-kbClus-mast"]
kbWorker = ["2uuidSender-kbClus", "3uuidSender-kbClus"]
azMachines = ["azureSenders-tf"]


def sm_initate_all():
    for machine in machines:
        event1 = ("terraform init ./{}".format(machine))
        sys.stderr = open('log.txt', 'a+')
        process1 = subprocess.call(event1.split(), stdout=subprocess.PIPE)
        
def sm_start_all():
    for machine in machines:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        sys.stderr = open('log.txt', 'w')
        jackBeNimble = "./" + machine + "/pass.txt"
        f = open(jackBeNimble, 'w')
        f.write("{}".format(password))
        f.close()
        field1 = "root_pass=" + password
        field2 = "./" + machine
        field3 = "-state=./" + machine + "/terraform.tfstate"
        event1 = ["terraform", "apply",  "-auto-approve", "-var"]
        event1.extend([field1, field3, field2])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE)

def sm_destroy_all():
    for machine in machines:
        sys.stderr = open('log.txt', 'w')
        jackBeNimble = "./" + machine + "/pass.txt"
        with open(jackBeNimble, 'r') as myfile:
            password=myfile.read().replace('\n', '')
        field1 = "root_pass=" + password
        field2 = "-lock=false"
        field3 = "-state=./" + machine + "/terraform.tfstate"
        field4 = "./" + machine
        event1 = ["terraform", "destroy", "-auto-approve", "-var"]
        event1.extend([field1, field2, field3, field4])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE)

def sm_build_reciever():
    for machine in recievers:
        field1 = "./" + machine + "/terraform.tfstate"
        field2 = "./" + machine + "/pass.txt"
        field3 = "./" + machine +"/ansibleData/deploy.yml"
        with open(field1) as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                ip_address = str(modules['resources']['linode_instance.recieverWebServer']['primary']['attributes']['ip_address'])
        ip_address = ip_address + ","
        with open(field2, 'r') as myfile:
            password=myfile.read().replace('\n', '')
            password = "ansible_user=root " + "ansible_password=" + password
        event1 = ["ansible-playbook", "-i"]
        event1.extend([ip_address, "--extra-vars", password, field3])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def sm_build_sender():
    for machine in senders:
        field1 = "./" + machine + "/terraform.tfstate"
        field2 = "./" + machine + "/pass.txt"
        field3 = "./" + machine +"/ansibleData/deploy.yml"
        skippy_do = machine[:-3]
        field4 = "linode_instance." + skippy_do
        with open(field1) as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                ip_address = str(modules['resources'][field4]['primary']['attributes']['ip_address'])
        ip_address = ip_address + ","
        with open(field2, 'r') as myfile:
            password=myfile.read().replace('\n', '')
            password = "ansible_user=root " + "ansible_password=" + password
        event1 = ["ansible-playbook", "-i"]
        event1.extend([ip_address, "--extra-vars", password, field3])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def sm_call_sender():
    for machine in senders:
        field1 = "./" + machine + "/terraform.tfstate"
        passLoc = "./" + machine + "/pass.txt" 
        skippy_do = machine[:-3]
        field4 = "linode_instance." + skippy_do
        list_1 = ["red", "green"]
        list_2 = ["1", "2", "3", "4", "5"]
        choice1 = random.choice(list_1)
        choice2 = random.choice(list_2)
        with open(field1) as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                internal_ip_address = str(modules['resources'][field4]['primary']['attributes']['ip_address'])
        with open("./recieverWebServer-tf/terraform.tfstate") as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                reciever_ip_address = str(modules['resources']['linode_instance.recieverWebServer']['primary']['attributes']['ip_address'])
        internal_ip_address = internal_ip_address + ","
        reciever_ip_address = "http://" + reciever_ip_address
        with open(passLoc, 'r') as myfile:
            password=myfile.read().replace('\n', '')
            password = "ansible_user=root " + "ansible_password=" + password
        event1 = ["ansible", "all", "-i"]
        command_call = "docker run -d -e DESTINATION=" + reciever_ip_address + "/reciever" + " -e WAITTIME=" + choice2 + " -e SOURCEVALUE=" + choice1 + " princelogan/webhook-generator:latest"
        event1.extend([internal_ip_address, "--extra-vars", password, "-a", command_call])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def start_all_kb_cluster():
    for machine in kbCluster:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(10))
        sys.stderr = open('log.txt', 'w')
        jackBeNimble = "./kbCluster-uuidSenders/" + machine + "/pass.txt"
        f = open(jackBeNimble, 'w')
        f.write("{}".format(password))
        f.close()
        field1 = "root_pass=" + password
        field2 = "./kbCluster-uuidSenders/" + machine
        field3 = "-state=./kbCluster-uuidSenders/" + machine + "/terraform.tfstate"
        event1 = ["terraform", "apply",  "-auto-approve", "-var"]
        print(event1)
        event1.extend([field1, field3, field2])
        process1 = subprocess.call(event1, stdout=subprocess.PIPE)

def build_kb_master():
    for machine in kbMaster:
        field1 = "./kbCluster-uuidSenders/" + machine + "/terraform.tfstate"
        field2 = "./kbCluster-uuidSenders/" + machine + "/pass.txt"
        field3 = "./kbCluster-uuidSenders/" + machine +"/ansibleData/deploy.yml"
        field4 = "linode_instance." + machine
        with open(field1) as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                ip_address = str(modules['resources'][field4]['primary']['attributes']['ip_address'])
        ip_address = ip_address + ","
        with open(field2, 'r') as myfile:
            password=myfile.read().replace('\n', '')
            password = "ansible_user=root " + "ansible_password=" + password
        event1 = ["ansible-playbook", "-i"]
        event1.extend([ip_address, "--extra-vars", password, field3])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def build_kb_worker():
    for machine in kbWorker:
        field1 = "./kbCluster-uuidSenders/" + machine + "/terraform.tfstate"
        field2 = "./kbCluster-uuidSenders/" + machine + "/pass.txt"
        field3 = "./kbCluster-uuidSenders/" + machine +"/ansibleData/deploy.yml"
        field4 = "linode_instance." + machine
        with open(field1) as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                ip_address = str(modules['resources'][field4]['primary']['attributes']['ip_address'])
        ip_address = ip_address + ","
        with open(field2, 'r') as myfile:
            password=myfile.read().replace('\n', '')
            password = "ansible_user=root " + "ansible_password=" + password
        event1 = ["ansible-playbook", "-i"]
        event1.extend([ip_address, "--extra-vars", password, field3])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def join_kb():
    for machine in kbWorker:
        joinStuff = "./kbCluster-uuidSenders/joinData"
        field1 = "./kbCluster-uuidSenders/" + machine + "/terraform.tfstate"
        passLoc = "./kbCluster-uuidSenders/" + machine + "/pass.txt"
        field4 = "linode_instance." + machine
        with open(joinStuff) as json_file:
            data = json.load(json_file)
            for modules in data['stdout_lines']:
                commandString = str(modules)
        with open(field1) as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                internal_ip_address = str(modules['resources'][field4]['primary']['attributes']['ip_address'])
        internal_ip_address = internal_ip_address + ","
        with open(passLoc, 'r') as myfile:
            password=myfile.read().replace('\n', '')
            password = "ansible_user=root " + "ansible_password=" + password
        event1 = ["ansible", "all", "-i"]
        event1.extend([internal_ip_address, "--extra-vars", password, "-a", commandString])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def kb_start_process():
    for machine in kbMaster:
        field1 = "./kbCluster-uuidSenders/" + machine + "/terraform.tfstate"
        passLoc = "./kbCluster-uuidSenders/" + machine + "/pass.txt"
        field4 = "linode_instance." + machine
        with open(field1) as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                internal_ip_address = str(modules['resources'][field4]['primary']['attributes']['ip_address'])
        internal_ip_address = internal_ip_address + ","
        with open("./recieverWebServer-tf/terraform.tfstate") as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                reciever_ip_address = str(modules['resources']['linode_instance.recieverWebServer']['primary']['attributes']['ip_address'])
                reciever_ip_address = "http://" + reciever_ip_address
        with open(passLoc, 'r') as myfile:
            password=myfile.read().replace('\n', '')
            password = "ansible_user=root " + "ansible_password=" + password
        x = 0
        for x in range(0, 100):
            list_1 = ["red", "green"]
            list_2 = ["1", "2", "3", "4", "5"]
            choice1 = random.choice(list_1)
            choice2 = random.choice(list_2)
            event1 = ["ansible", "all", "-i"]
            x +=1
            y = str(x)
            command_call = "kubectl run --generator=run-pod/v1" + " uuidsenderxyz" + y + " --overrides='{\"kind\":\"Pod\", \"apiVersion\":\"v1\", \"spec\": {\"hostNetwork\": true}}' --image=princelogan/webhook-generator --env=\"DESTINATION=\"" + reciever_ip_address + "/reciever" + "  --env=\"WAITTIME=\"" + choice2 + " --env=\"SOURCEVALUE=\"" + choice1
            event1.extend([internal_ip_address, "--extra-vars", password, "-a", command_call])
            print(event1)
            process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def destroy_cluster():
    for machine in kbCluster:
        sys.stderr = open('log.txt', 'w')
        jackBeNimble = "./kbCluster-uuidSenders/" + machine + "/pass.txt"
        with open(jackBeNimble, 'r') as myfile:
            password=myfile.read().replace('\n', '')
        field1 = "root_pass=" + password
        field2 = "-lock=false"
        field3 = "-state=./kbCluster-uuidSenders/" + machine + "/terraform.tfstate"
        field4 = "./kbCluster-uuidSenders/" + machine
        event1 = ["terraform", "destroy", "-auto-approve", "-var"]
        event1.extend([field1, field2, field3, field4])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE)

def az_launch_machine():
    for machine in azMachines:
        alphabet1 = string.ascii_letters + string.digits
        alphabet2 = string.digits
        password = ''.join(secrets.choice(alphabet1) for i in range(10))
        run = ''.join(secrets.choice(alphabet2) for i in range(4))
        sys.stderr = open('log.txt', 'w')
        jackBeNimble = "./" + machine + "/pass.txt"
        jackBeNimble2 = "./" + machine + "/run.txt"
        f = open(jackBeNimble, 'w')
        f.write("{}".format(password))
        f.close()
        f = open(jackBeNimble2, 'w')
        f.write("{}".format(run))
        f.close()
        field1 = "root_pass=" + password
        field2 = "./" + machine
        field3 = "-state-out=./" + machine + "/" 
        field3 = "-state=./" + machine + "/terraform.tfstate"
        field4 = "-var"
        field4b = "run_id=" + run
        field5 = "-lock=false"
        event1 = ["terraform", "apply",  "-auto-approve", "-var"]
        event1.extend([field1, field4, field4b, field5, field3, field2])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE)

def az_initate_all():
    for machine in azMachines:
        event1 = ("terraform init ./{}".format(machine))
        sys.stderr = open('log.txt', 'a+')
        process1 = subprocess.call(event1.split(), stdout=subprocess.PIPE)

def az_kill_machine():
    for machine in azMachines:
        sys.stderr = open('log.txt', 'w')
        jackBeNimble = "./" + machine + "/pass.txt"
        jackBeNimble2 = "./" + machine + "/pass.txt"
        with open(jackBeNimble, 'r') as myfile:
            password=myfile.read().replace('\n', '')
        with open(jackBeNimble2, 'r') as myfile:
            run=myfile.read().replace('\n', '')
        field1 = "root_pass=" + password
        field2 = "-lock=false"
        field3 = "-state=./" + machine + "/terraform.tfstate"
        field4 = "./" + machine
        field5 = "-var"
        field6 = "run_id=" + run
        event1 = ["terraform", "destroy", "-auto-approve", "-var"]
        event1.extend([field1, field5, field6, field2, field3, field4])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE)

def az_create_sender():
    for machine in azMachines:
        field1 = "./" + machine + "/terraform.tfstate"
        field2 = "./" + machine + "/pass.txt"
        field3 = "./" + machine +"/ansibleData/deploy.yml"
        with open(field1) as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                ip_address1 = str(modules['resources']['azurerm_public_ip.publicIP']['primary']['attributes']['ip_address'])
                ip_address2 = str(modules['resources']['azurerm_public_ip.publicIPOne']['primary']['attributes']['ip_address'])
                ip_address3 = str(modules['resources']['azurerm_public_ip.publicIPThree']['primary']['attributes']['ip_address'])
        ip_address1 = ip_address1 + ","
        ip_address2 = ip_address2 + ","
        ip_address3 = ip_address3 + ","
        with open(field2, 'r') as myfile:
            password=myfile.read().replace('\n', '')
            password = "ansible_user=lojoho " + "ansible_password=" + password
        event1 = ["ansible-playbook", "-i"]
        event1.extend([ip_address1, "--extra-vars", password, field3])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        event2 = ["ansible-playbook", "-i"]
        event2.extend([ip_address2, "--extra-vars", password, field3])
        print(event2)
        process2 = subprocess.call(event2, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        event3 = ["ansible-playbook", "-i"]
        event3.extend([ip_address3, "--extra-vars", password, field3])
        print(event3)
        process3 = subprocess.call(event2, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def az_call_sender():
    for machine in azMachines:
        field1 = "./" + machine + "/terraform.tfstate"
        field2 = "./" + machine + "/pass.txt"
        passLoc = "./" + machine + "/pass.txt"
        list_1 = ["red", "green"]
        list_2 = ["1", "2", "3", "4", "5"]
        choice1 = random.choice(list_1)
        choice2 = random.choice(list_2)
        with open(field1) as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                ip_address1 = str(modules['resources']['azurerm_public_ip.publicIP']['primary']['attributes']['ip_address'])
                ip_address2 = str(modules['resources']['azurerm_public_ip.publicIPOne']['primary']['attributes']['ip_address'])
                ip_address3 = str(modules['resources']['azurerm_public_ip.publicIPThree']['primary']['attributes']['ip_address'])
        ip_address1 = ip_address1 + ","
        ip_address2 = ip_address2 + ","
        ip_address3 = ip_address3 + ","
        with open("./recieverWebServer-tf/terraform.tfstate") as json_file:
            data = json.load(json_file)
            for modules in data['modules']:
                reciever_ip_address = str(modules['resources']['linode_instance.recieverWebServer']['primary']['attributes']['ip_address'])
        reciever_ip_address = "http://" + reciever_ip_address
        with open(field2, 'r') as myfile:
            password=myfile.read().replace('\n', '')
            password = "ansible_user=lojoho " + "ansible_password=" + password
        event1 = ["ansible", "all", "-i"]
        command_call = "sudo docker run -d -e DESTINATION=" + reciever_ip_address + "/reciever" + " -e WAITTIME=" + choice2 + " -e SOURCEVALUE=" + choice1 + " princelogan/webhook-generator:latest"
        event1.extend([ip_address1, "--extra-vars", password, "-a", command_call])
        print(event1)
        process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        event2 = ["ansible", "all", "-i"]
        command_call = "sudo docker run -d -e DESTINATION=" + reciever_ip_address + "/reciever" + " -e WAITTIME=" + choice2 + " -e SOURCEVALUE=" + choice1 + " princelogan/webhook-generator:latest"
        event2.extend([ip_address2, "--extra-vars", password, "-a", command_call])
        print(event2)
        process2 = subprocess.call(event2, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        event3 = ["ansible", "all", "-i"]
        command_call = "sudo docker run -d -e DESTINATION=" + reciever_ip_address + "/reciever" + " -e WAITTIME=" + choice2 + " -e SOURCEVALUE=" + choice1 + " princelogan/webhook-generator:latest"
        event3.extend([ip_address3, "--extra-vars", password, "-a", command_call])
        print(event3)
        process3 = subprocess.call(event3, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

if __name__ == "__main__":
    sm_initate_all()
    sm_start_all()
    sm_destroy_all()
    sm_build_reciever()
    sm_build_sender()
    sm_call_sender()
    start_all_kb_cluster()
    build_kb_master()
    build_kb_worker()
    join_kb()
    kb_start_process()
    destroy_cluster()
    az_launch_machine()
    az_initate_iall()
    az_kill_machine()
    az_create_sender()
    az_call_sender()







#kubectl run --generator=run-pod/v1 uuidsenderyyyxx100 --overrides='{"kind":"Pod", "apiVersion":"v1", "spec": {"hostNetwork": true}}' --image=princelogan/webhook-generator --env="DESTINATION=https://en8ebcj8ftmb9.x.pipedream.net" --env="WAITTIME=2" --env="SOURCEVALUE=blue"
#kubectl run --generator=run-pod/v1 uuidsenderyyyxx100 --overrides='{"kind":"Pod", "apiVersion":"v1", "spec": {"hostNetwork": true}}' --image=princelogan/webhook-generator --env="DESTINATION=https://en8ebcj8ftmb9.x.pipedream.net" --env="WAITTIME=2" --env="SOURCEVALUE=blue"
#ansible all -i '198.58.110.204,' --extra-vars "ansible_user=root ansible_password=qWhzvfbOpG" -a "docker run -d -e SOURCEVALUE="green" -e DESTINATION="http://45.79.0.57/reciever" -e WAITTIME="1" princelogan/webhook-generator:latest"
#process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
#ansible all -i '45.79.24.147,' --extra-vars "ansible_user=root ansible_password=5Bx8ySFcAu" -a "docker run -e SOURCEVALUE="red" -e DESTINATION="https://enz9yjah5e6hn.x.pipedream.net" -e WAITTIME="1" princelogan/webhook-generator:latest"
#ansible-playbook -i '45.79.24.147,' --extra-vars "ansible_user=root ansible_password=5Bx8ySFcAu" deploy.yml
#ansible all -i '45.79.24.147,' --extra-vars "ansible_user=root ansible_password=5Bx8ySFcAu" -a "docker run -e SOURCEVALUE="red" -e DESTINATION="https://enz9yjah5e6hn.x.pipedream.net" -e WAITTIME="1" princelogan/webhook-generator:latest"

