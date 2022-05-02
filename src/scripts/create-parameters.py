#!/usr/bin/env python3

import subprocess
import os
import json

def submodules_count():
  return len(subprocess.run(
    ['git', 'submodule', 'status'],
    check=True,
    capture_output=True
  ).stdout.decode('utf-8').splitlines())

def changed_submodules():
  raw_changes = subprocess.run(
    ['git', 'log', '-p', '--first-parent', '--merges', '-1'],
    check=True,
    capture_output=True
  ).stdout.decode('utf-8').splitlines()
  SUBMODULE = 'Submodule '
  raw_changes = list(filter(lambda submodule: SUBMODULE in submodule, raw_changes))
  raw_changes = [item.replace(SUBMODULE, '').split() for item in raw_changes]
  
  if (len(raw_changes) == 0):
    return []

  changed_list = []

  for item in raw_changes:
    # ['olympus-frontend','b02a2f3..4f6c53c:']
    changed_list.append(item[0])
    print(f'Submodule {item[0]} updated from {item[1][:7]} to {item[1][9:16]}')
  
  return changed_list

def write_json(content):
  output_path = os.environ.get('OUTPUT_PATH')

  with open(output_path, 'w') as fp:
    if(content):
      fp.write(json.dumps(content))
    else:
      fp.write("{}")
    
submodules_count = submodules_count()
terminate = False

if(submodules_count > 0):
  print(f"Total of {submodules_count} submodule(s) detected.")
else:
  print("No submodules in the repo.")
  write_json("")
  terminate = True

changed_list = changed_submodules()

if(len(changed_list) == 0):
  print("No submodule(s) changes detected.")
  write_json("")
  terminate = True

if (terminate):
  exit()
else:
  dict = { i : "true" for i in changed_list }
  write_json(dict)
