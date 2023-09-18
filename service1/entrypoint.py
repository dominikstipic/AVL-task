import sys
import hashlib

def read_input():
    inp = sys.stdin.readlines()
    hash_func = inp[0].strip()
    message = '\n'.join(inp[1:]).strip()
    return hash_func, message
 
def process(hash_func, message):
    h = hashlib.new(hash_func)
    h.update(str.encode(message))
    hash = h.hexdigest()
    return hash

if __name__ == "__main__":
    hash_func, message = read_input()
    h = process(hash_func, message)
    print(f"{hash_func}(m) = {h}")