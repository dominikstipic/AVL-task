import subprocess
import sys
import json
import libs

def exec_pipe_cmd(cmd):
    cmds = cmd.split("|")
    process = subprocess.Popen(cmds[0].strip().split(), stdout=subprocess.PIPE)
    for i in range(1, len(cmds)):
        process = subprocess.Popen(cmds[i].strip().split(), stdin=process.stdout, stdout=subprocess.PIPE)
    process.wait()
    output = process.stdout.read().decode()
    return output.strip()

def check_for_git_changes():
  result = subprocess.run(["git", "status", "--porcelain"], cwd=".", capture_output=True)
  output = result.stdout.decode()
  if output:
    return True
  else:
    return False
  
def git_commit(version):
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "--message", f"version {version}"])

def run_tests():
    sys.path.insert(0, "service1")
    sys.path.insert(0, "service2")
    import service1.test as t1
    import service2.test as t2
    try:
        t1.test_sha256()
        t1 = True
    except Exception:
       t1 = False
    try:
        t2.test_service()
        t2 = True
    except Exception:
       t2 = False
    return dict(test1=t1, test2=t2)

def get_credentials(json_file_path):
    with open(json_file_path, "r") as f:
        json_data = json.load(f)
    return json_data 

def docker_login(username, password):
   cmd = f"docker login -u {username} -p {password}"
   result = subprocess.run(cmd.split(), capture_output=True)
   output = result.stdout.decode()
   print(output)
   
def build():
   cmd = f"docker-compose up -d"
   result = subprocess.run(cmd.split(), capture_output=True)
   print(result)

def push_images():
    cmd1 = "docker image push thegreatgamma/avl-task:s1"
    cmd2 = "docker image push thegreatgamma/avl-task:s2"
    libs.interactive_proc_start(cmd1)


changes = check_for_git_changes()
if not changes:
   print("No changes!")
   sys.exit()
commit_message_cmd = "git log | head -n 5 | tail -n 1"
commit_message = exec_pipe_cmd(commit_message_cmd)
new_version = int(commit_message.split()[1])+1
git_commit(new_version)

t = run_tests()
print(t)

build()

credentials = get_credentials("credentials.json")
docker_login(**credentials)
