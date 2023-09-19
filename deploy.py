import argparse
import subprocess

def parse():
    parser = argparse.ArgumentParser(description='Service deployment')
    parser.add_argument('-s1', '--version_service1', required=True, help='Service1 version')
    parser.add_argument('-s2', '--version_service2', required=True, help='Service2 version')
    args = parser.parse_args()
    return args.version_service1, args.version_service2


def get_commits_id_messages_dict():
    result = subprocess.run(["git", "log", "--oneline"], capture_output=True).stdout
    result = result.decode("utf-8")
    lines = result.splitlines()
    d = {}
    for line in lines:
        commit, mess = line.split(" ", maxsplit=1)
        d[mess] = commit
    return d

def git_clone():
    s1_url = "https://github.com/dominikstipic/AVL-service1"
    s2_url = "https://github.com/dominikstipic/AVL-service2"
    subprocess.run(["git", "clone", s1_url, "services"], capture_output=True)
    subprocess.run(["git", "clone", s2_url, "services"], capture_output=True)
    subprocess.run("mv", "services/AVL-service1", "services/service1")
    subprocess.run("mv", "services/AVL-service2", "services/service2")




s1_version, s2_version = parse()
d = get_commits_id_messages_dict()
print(d)

s1_commit = d.get(s1_version, None)
s2_commit = d.get(s2_version, None)

git_clone()
# Process the file and directory
