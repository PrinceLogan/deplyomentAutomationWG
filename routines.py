#!/usr/bin/python3

import engine
import sys

command1 = sys.argv[1]

if 'sm_destroy_all'in command1:
    engine.sm_destroy_all()
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
elif 'kb_restart_everything' in command1:
    engine.sm_start_all()
    engine.sm_build_reciever()
    engine.start_all_kb_cluster()
    engine.build_kb_master()
    engine.build_kb_worker()
    engine.join_kb()
elif 'sm_restart_everything' in command1:
    engine.sm_destroy_all()
    engine.sm_initate_all()
    engine.sm_start_all()
    engine.sm_build_reciever()
    engine.sm_build_sender()
    engine.sm_call_sender()
    engine.sm_call_sender()
    engine.sm_call_sender()
elif 'destroy_all' in command1:
    engine.destroy_cluster()
    engine.sm_destroy_all()
elif 'az_launch_machine' in command1:
    engine.az_initate_all()
    engine.az_launch_machine()
elif 'az_kill_machine' in command1:
    engine.az_kill_machine()
elif 'az_create_sender' in command1:
    engine.az_create_sender()
elif 'az_call_sender' in command1:
    engine.az_call_sender()
else:
    none
