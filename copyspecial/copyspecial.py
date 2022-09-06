#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(dir):
  """
  Returns a list of the absolute paths of the special files in the given directory 
  """
  # Functional style
  # def filter_special(file):
  #   return re.search(special_file_pattern, file)
  # special_file_pattern = r'__\w+__'
  # files = os.listdir(dir)
  # file_abspaths = map(os.path.abspath, filter(filter_special, files))
  # for file in file_abspaths:
  #   print(file)

  special_file_pattern = r'__\w+__'
  files = os.listdir(dir)

  abspaths_special = []
  for file in files:
    match = re.search(special_file_pattern, file)
    if match: 
      # Gets us the absolute path of a path without including any parent directories
      # abspath = os.path.abspath(file)
      # print(abspath)
      relativepath = os.path.join(dir, file)
      abspath = os.path.abspath(relativepath)
      abspaths_special.append(abspath)
  return abspaths_special

def copy_to(paths, dir):
  if not os.path.exists(dir):
    os.makedirs(dir)
  for path in paths:
    shutil.copy(path, dir)

def zip_to(paths, zippath):
  cmd = f"zip -j {zippath}"
  cmd += " " + " ".join(paths)
  print(f"Command to run: {cmd}", end="\n\n")
  (exitcode, output) = subprocess.getstatusoutput(cmd)
  if exitcode:
    sys.stderr.write(output)
    sys.exit(exitcode)
  print(output)

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print("error: must specify one or more dirs")
    sys.exit(1)

  # +++your code here+++
  # Call your functions

  abspaths = [] 

  for arg in args:
    abspaths.extend(get_special_paths(arg))
  if not todir and not tozip:
    for path in abspaths:
      print(path)
  if todir:
    copy_to(abspaths, todir)
  if tozip:
    zip_to(abspaths, tozip)
  
if __name__ == "__main__":
  main()
