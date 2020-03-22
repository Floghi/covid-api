import pytoml as toml

def load_config(path):
  with open(path) as f:
    conf = toml.load(f)
  return conf
