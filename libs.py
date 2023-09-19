import subprocess
import json

def interactive_proc_start(cmd):
    cmds = cmd.strip().split()
    process = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while process.poll() == None:
        output = process.stdout.readline()
        if output == b'': break
        print(output.decode('utf-8'))

def exec_pipe_cmd(cmd):
    cmds = cmd.split("|")
    process = subprocess.Popen(cmds[0].strip().split(), stdout=subprocess.PIPE)
    for i in range(1, len(cmds)):
        process = subprocess.Popen(cmds[i].strip().split(), stdin=process.stdout, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.read().decode()
    return output.strip()

def get_json(json_file_path):
    with open(json_file_path, "r") as f:
        json_data = json.load(f)
    return json_data 