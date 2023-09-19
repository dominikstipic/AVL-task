import argparse
import subprocess
import sys
import libs

def parse():
    parser = argparse.ArgumentParser(description='Service deployment')
    parser.add_argument('-s1', '--version_service1', required=True, help='Service1 version')
    parser.add_argument('-s2', '--version_service2', required=True, help='Service2 version')
    args = parser.parse_args()
    return args.version_service1, args.version_service2

def get_commits_id_messages_dict():
    result = subprocess.run(["git", "log", "--oneline"], cwd="services/service1", capture_output=True).stdout.decode("utf-8")
    lines = result.splitlines()
    s1 = {}
    for line in lines:
        commit, mess = line.split(" ", maxsplit=1)
        s1[mess] = commit
    result = subprocess.run(["git", "log", "--oneline"], cwd="services/service2", capture_output=True).stdout.decode("utf-8")
    lines = result.splitlines()
    s2 = {}
    for line in lines:
        commit, mess = line.split(" ", maxsplit=1)
        s2[mess] = commit
    return dict(s1=s1, s2=s2)

def git_clone():
    subprocess.run(["rm", "-r", "service1", "service2", "-f"], cwd="services")
    token = libs.get_json("credentials.json")["github"]["token"]
    s1_url = f"https://dominikstipic:{token}@github.com/dominikstipic/AVL-service1.git"
    s2_url = f"https://dominikstipic:{token}@github.com/dominikstipic/AVL-service2.git"
    subprocess.run(["git", "clone", s1_url], cwd="services")
    subprocess.run(["git", "clone", s2_url], cwd="services")
    subprocess.run(["mv", "services/AVL-service1", "services/service1"])
    subprocess.run(["mv", "services/AVL-service2", "services/service2"])
    
def current_version(home_root):
    git_process = subprocess.Popen(["git", "log", "--oneline"], cwd=home_root, stdout=subprocess.PIPE)
    head_process = subprocess.Popen(["head", "-n", "1"], stdin=git_process.stdout, stdout=subprocess.PIPE)
    head_process.wait()
    output = head_process.stdout.read().decode()
    return output

def git_checkout(s1_commit, s2_commit):
    subprocess.run(["git", "checkout", s1_commit], cwd="services/service1", capture_output=True)
    subprocess.run(["git", "checkout", s2_commit], cwd="services/service2", capture_output=True)
    s1_version = current_version("services/service1")
    s2_version = current_version("services/service2")
    print(f"service1 head = {s1_version.strip()}")
    print(f"service2 head = {s2_version.strip()}")

############################################################################################
s1_version, s2_version = parse()
git_clone()
commits = get_commits_id_messages_dict()
print(commits)

s1_commit = commits["s1"].get(s1_version, None)
s2_commit = commits["s2"].get(s2_version, None)

if not s1_commit or not s2_commit:
    print(f"Couldn't find versions {s1_version} or {s2_version}")
    sys.exit()

print(f"service1 commit = {s1_commit}")
print(f"service2 commit = {s2_commit}")

git_checkout(s1_commit, s2_commit)

build_cmd = "docker-compose up --build"
libs.interactive_proc_start(build_cmd, False)