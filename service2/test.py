import json
from entrypoint import process

def read_json_file_as_dict(json_file_path):
  with open(json_file_path, "r") as f:
    json_data = json.load(f)
  return json_data 

def test_service():
  d = read_json_file_as_dict("test.json")
  for k,v in d.items():
    print(k, v)
    h = process(k)
    assert h == v