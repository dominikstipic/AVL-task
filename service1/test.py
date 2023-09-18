from entrypoint import process
import subprocess

def linux_sha256(message):
    echo_process = subprocess.Popen(["echo", message], stdout=subprocess.PIPE)
    hash_process = subprocess.Popen(["sha256sum"], stdin=echo_process.stdout, stdout=subprocess.PIPE)
    hash_process.wait()
    output = hash_process.stdout.read().decode()
    return output.split()[0]

def test_sha256():
    alg = "sha256"
    m1 = "hello"
    m2 = "world"
    m3 = "hello world"
    h1 = process(alg, m1)
    h2 = process(alg, m2)
    h3 = process(alg, m3)
    assert h1 == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    assert h2 == "486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7"
    assert h3 == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"