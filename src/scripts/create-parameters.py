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
    # ['submodule-1','b02a2f3..4f6c53c:']
    changed_list.append(item[0])
    print(f'Submodule {item[0]} updated from {item[1][:7]} to {item[1][9:16]}')
  
  return changed_list

submodules_count = submodules_count()

if(submodules_count > 0):
  print(f"Total of {submodules_count} submodule(s) detected.")
else:
  print("No submodules in the repo.")
  exit()

changed_list = changed_submodules()

if(len(changed_list) == 0):
  print("No submodule(s) changes detected.")
  exit()

dict = { i : "true" for i in changed_list }
output_path = os.environ.get('OUTPUT_PATH')

with open(output_path, 'w') as fp:
  fp.write(json.dumps(dict))