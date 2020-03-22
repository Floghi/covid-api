import pytoml as toml
import yaml
from yaml import load, dump
try:
  from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
  from yaml import Loader, Dumper

def load_config(path):
  with open(path) as f:
    conf = toml.load(f)
  return conf

def load_yaml(path):
  with open(path) as f:
    conf = yaml.load(f, Loader)
  return conf
