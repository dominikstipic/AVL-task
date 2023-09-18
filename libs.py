import subprocess

def interactive_proc_start(cmd):
    cmds = cmd.strip().split()
    process = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.start()
    while True:
        output = process.stdout.readline()
        if output == b'': break
        print(output.decode('utf-8'))
    process.terminate()
