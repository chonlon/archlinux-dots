import os
import sys
from pathlib import Path

args = os.sys.argv
args = args[1:]
command = args[0]
home_dir = os.path.expanduser('~')
cur_dir = os.path.dirname(os.path.abspath(__file__))
reciepes_dir = cur_dir

if command is None:
  print('command is empty')
  exit(1)
args = args[1:]

reciepes = []
for file in os.listdir(reciepes_dir):
  if file.endswith('.just'):
    reciepes.append(file)

def run_recipe(recipe, args):
  if len(args) == 0:
    cmd = f'just -f {recipe} --choose'
  else:
    cmd = f'just -f {recipe} {" ".join(args)}'

  print(cmd)
  os.system(cmd)

recipe = command + '.just'
if recipe in reciepes:
  recipe = Path(reciepes_dir) / recipe
  run_recipe(recipe, args)
else:
  print(f'no such recipe: {command}')
  print(f'available recipes: {reciepes}')
  exit(1)