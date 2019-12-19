#!/usr/bin/python3

import engine
import sys
import time

command1 = sys.argv[1]

if 'routine1' in command1:
    engine.sm_initate_all()
    engine.sm_start_all()
    engine.meta_sleepy_time()
    engine.sm_build_reciever()
    engine.sm_build_sender()
    engine.sm_call_sender()
    engine.sm_call_sender()
    engine.sm_call_sender()
elif 'routine2' in command1:
    engine.start_all_kb_cluster()
    engine.build_kb_master()
    engine.build_kb_worker()
    engine.meta_sleepy_time()
    engine.join_kb()
    engine.kb_start_process()
    engine.kb_start_process()
    engine.kb_start_process()
    engine.kb_start_process()
elif 'routine3' in command1:
    engine.az_initate_all()
    engine.az_launch_machine()
    engine.az_create_sender()
    engine.az_call_sender()
elif 'fullRun' in command1:
    engine.sm_initate_all()
    engine.sm_start_all()
    engine.meta_sleepy_time()
    engine.sm_build_reciever()
    engine.sm_build_sender()
    engine.sm_call_sender()
    engine.sm_call_sender()
    engine.sm_call_sender()
    engine.meta_sleepy_time()
    engine.start_all_kb_cluster()
    engine.build_kb_master()
    engine.build_kb_worker()
    engine.meta_sleepy_time()
    engine.join_kb()
    engine.kb_start_process()
    engine.kb_start_process()
    engine.kb_start_process()
    engine.kb_start_process()
elif 'routine4' in command1:
    engine.sm_initate_all()
    engine.sm_start_all()
    engine.meta_sleepy_time()
    engine.sm_build_reciever()
    engine.start_all_kb_cluster()
    engine.build_kb_master()
    engine.build_kb_worker()
    engine.kb_start_process()
    engine.kb_start_process()
elif 'routine5' in command1:
    engine.az_initate_all()
    engine.az_launch_machine()
    engine.az_create_sender()
    engine.az_call_sender()
elif 'sm_destroy_all' in command1:
    engine.sm_destroy_all()
    engine.meta_delete_hostkey()
elif 'sm_start_all' in command1:
    engine.sm_initate_all()
    engine.sm_start_all()
elif 'sm_build_reciever' in command1:
    engine.sm_build_reciever()
elif 'sm_build_sender' in command1:
    engine.sm_build_sender()
elif 'sm_call_sender' in command1:
    engine.sm_call_sender()
elif 'start_all_kb_clusteer' in command1:
    engine.start_all_kb_cluster()
elif 'build_kb_master' in command1:
    engine.build_kb_master()
elif 'build_kb_worker' in command1:
    engine.build_kb_worker()
elif 'join_kb' in command1:
    engine.join_kb()
elif 'kb_start_process' in command1:
    engine.kb_start_process()
elif 'destroy_cluster' in command1:
    engine.destroy_cluster()
    engine.meta_delete_hostkey()
elif 'destroy_all' in command1:
    engine.sm_initate_all()
    engine.destroy_cluster()
    engine.sm_destroy_all()
    engine.meta_delete_hostkey()
elif 'az_launch_machine' in command1:
    engine.az_initate_all()
    engine.az_launch_machine()
elif 'az_kill_machine' in command1:
    engine.az_kill_machine()
elif 'az_create_sender' in command1:
    engine.az_create_sender()
elif 'az_call_sender' in command1:
    engine.az_call_sender()
elif 'delete_hostkey' in command1:
    engine.meta_delete_hostkey()
elif 'aws_initate_all' in command1:
    engine.aws_initate_all()
elif 'aws_create_sender' in command1:
    engine.aws_create_sender()
elif 'aws_launch_machine' in command1:
    engine.aws_launch_machine()
else:
    print("Sorry, Charlie! That is not a valid routine.")
