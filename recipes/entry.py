import os
import sys
from pathlib import Path
import utils

args = os.sys.argv
args = args[1:]
command = args[0] if len(args) > 0 else ''
home_dir = os.path.expanduser('~')
cur_dir = os.path.dirname(os.path.abspath(__file__))
reciepes_dir = Path(cur_dir)

if command is None:
  print('command is empty')
  exit(1)
args = args[1:]

reciepes = []
for directory in os.listdir(reciepes_dir):
  if os.path.isdir(checkpath := Path(reciepes_dir) / directory):
    checkpath = Path(checkpath)
    #if checkpath has justfile
    if os.path.isfile(checkpath / 'justfile'):
      reciepes.append(checkpath)

def run_recipe(recipe, args):
  # make soft link replace to real path
  recipe = os.path.realpath(recipe) + '/justfile'
  pwd = os.getcwd()
  if len(args) == 0:
    cmd = f'cd {pwd} && just --choose -f {recipe}'
  else:
    cmd = f'cd {pwd} && just -f {recipe} {" ".join(args)}'

  print(cmd)
  os.system(cmd)

recipe = reciepes_dir / command
if recipe in reciepes:
  run_recipe(recipe, args)
else:
  reciepes = [str(r).replace(str(reciepes_dir) + '/', '') for r in reciepes]
  reciepes = [r.replace('/justfile', '') for r in reciepes]
  print(f'no such recipe: {command}')
  print(f'available recipes: {reciepes}')
  recipe = utils.choose_in_options(reciepes)
  if recipe is not None:
    recipe = reciepes_dir / recipe
    run_recipe(recipe, args)
    exit(0)
  exit(1)
