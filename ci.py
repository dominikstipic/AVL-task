import subprocess
import sys
import libs

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
    sys.path.insert(0, "services/service1")
    sys.path.insert(0, "services/service2")
    import services.service1.test as t1
    import services.service2.test as t2
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

def docker_login(username, password):
   cmd = f"docker login -u {username} -p {password}"
   result = subprocess.run(cmd.split(), capture_output=True)
   output = result.stdout.decode()
   print(output)
   
def build():
   cmd = f"docker-compose up -d --build"
   result = subprocess.run(cmd.split(), capture_output=True)
   print(result)

def push_images():
    cmd1 = "docker image push thegreatgamma/avl-task:s1"
    cmd2 = "docker image push thegreatgamma/avl-task:s2"
    libs.interactive_proc_start(cmd1)
    libs.interactive_proc_start(cmd2)

######################################################
# GIT 
changes = check_for_git_changes()
if not changes:
   print("No changes!")
   sys.exit()
commit_message_cmd = "git log | head -n 5 | tail -n 1"
commit_message = libs.exec_pipe_cmd(commit_message_cmd)
new_version = int(commit_message.split()[1])+1
git_commit(new_version)

# TESTS
t = run_tests()
print(t)

# BUILD DOCKER CONTAINERS
build()

# PUSH TO DOCKER REPO
credentials = libs.get_json("credentials.json")["docker"]
docker_login(**credentials)
push_images()