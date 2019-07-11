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

command1 = sys.argv[1]

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

if 'sm_destroy_all'in command1:
    sm_destroy_all()
elif 'sm_start_all' in command1:
    sm_initate_all()
    sm_start_all()
elif 'sm_build_reciever' in command1:
    sm_build_reciever()
elif 'sm_build_sender' in command1:
    sm_build_sender()
elif 'sm_call_sender' in command1:
    sm_call_sender()
elif 'start_all_kb_clusteer' in command1:
    start_all_kb_cluster()
elif 'build_kb_master' in command1:
    build_kb_master()
elif 'build_kb_worker' in command1:
    build_kb_worker()
elif 'join_kb' in command1:
    join_kb()
elif 'kb_start_process' in command1:
    kb_start_process()
elif 'destroy_cluster' in command1:
    destroy_cluster()
elif 'kb_restart_everything' in command1:
    sm_start_all()
    sm_build_reciever()
    start_all_kb_cluster()
    build_kb_master()
    build_kb_worker()
    join_kb()
elif 'sm_restart_everything' in command1:
    sm_destroy_all()
    sm_initate_all()
    sm_start_all()
    sm_build_reciever()
    sm_build_sender()
    sm_call_sender()
    sm_call_sender()
    sm_call_sender()
elif 'destroy_all' in command1:
    destroy_cluster()
    sm_destroy_all()
else:
    none

#kubectl run --generator=run-pod/v1 uuidsenderyyyxx100 --overrides='{"kind":"Pod", "apiVersion":"v1", "spec": {"hostNetwork": true}}' --image=princelogan/webhook-generator --env="DESTINATION=https://en8ebcj8ftmb9.x.pipedream.net" --env="WAITTIME=2" --env="SOURCEVALUE=blue"

#kubectl run --generator=run-pod/v1 uuidsenderyyyxx100 --overrides='{"kind":"Pod", "apiVersion":"v1", "spec": {"hostNetwork": true}}' --image=princelogan/webhook-generator --env="DESTINATION=https://en8ebcj8ftmb9.x.pipedream.net" --env="WAITTIME=2" --env="SOURCEVALUE=blue"

#ansible all -i '198.58.110.204,' --extra-vars "ansible_user=root ansible_password=qWhzvfbOpG" -a "docker run -d -e SOURCEVALUE="green" -e DESTINATION="http://45.79.0.57/reciever" -e WAITTIME="1" princelogan/webhook-generator:latest"
#process1 = subprocess.call(event1, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
#ansible all -i '45.79.24.147,' --extra-vars "ansible_user=root ansible_password=5Bx8ySFcAu" -a "docker run -e SOURCEVALUE="red" -e DESTINATION="https://enz9yjah5e6hn.x.pipedream.net" -e WAITTIME="1" princelogan/webhook-generator:latest"
#ansible-playbook -i '45.79.24.147,' --extra-vars "ansible_user=root ansible_password=5Bx8ySFcAu" deploy.yml
#ansible all -i '45.79.24.147,' --extra-vars "ansible_user=root ansible_password=5Bx8ySFcAu" -a "docker run -e SOURCEVALUE="red" -e DESTINATION="https://enz9yjah5e6hn.x.pipedream.net" -e WAITTIME="1" princelogan/webhook-generator:latest"

