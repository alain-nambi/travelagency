
import os
import subprocess
import time
import schedule


def open_cmd():
    directory_path = r"E:\MGBI\semaine27Nov23\DJANGO_tutorial\studybud\studybud"
    os.chdir(directory_path)
    cwd = os.getcwd()
 
    print("Current working directory is:", cwd)
    commands_to_run = [
        'node api.js'
    ]
    for cmd in commands_to_run:
        subprocess.run(cmd, shell=True)
         

# schedule.every().day.at("16:26").do(open_cmd)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
open_cmd()