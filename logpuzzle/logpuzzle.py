#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import subprocess
import sys
from urllib import request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  # +++your code here+++
  uris = {} 
  pattern = r'GET\s.*puzzle.*\sHTTP'
  uri_pattern = r'GET\s(\S+)\sHTTP'
  suffix_pattern = r'-[a-z]{4}-([a-z]{4})\.jpg'
  prefix = "https://"
  hostname = filename.split("_")[-1]

  sort_by_second = False
  f = open(filename, 'r')
  for line in f:
    is_puzzle = re.search(pattern, line)
    if is_puzzle:
      match_uri = re.search(uri_pattern, line)
      match_suffix = re.search(suffix_pattern, line)
      if not sort_by_second and match_suffix:
        sort_by_second = True
      if match_uri:
        uri = match_uri.group(1)
        if uri not in uris:
          uris[uri] = 1
  f.close()

  def sort_by_second_word(uri): 
    match_suffix = re.search(suffix_pattern, uri)
    return match_suffix.group(1)

  def assemble_urls(sort_function=None):
    base_url = prefix + hostname
    return [ base_url + uri for uri in sorted(uris.keys(), key=sort_function) ]
      
  if sort_by_second:
    return assemble_urls(sort_by_second_word)
  return assemble_urls() 

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creaes the directory if necessary.
  """
  # +++your code here+++
  def fetch_images():
    images = [] 
    img_urls_total = len(img_urls)
    print(f"Will fetch {img_urls_total} images")
    for i in range(img_urls_total):
      print("Retrieving...")
      img_filename = f"img{i + 1}.jpg"
      images.append(img_filename)
      img_path = os.path.join(dest_dir, img_filename) 
      request.urlretrieve(img_urls[i], img_path) 
    return images

  def create_index_html(images):
      index_html_path = os.path.join(dest_dir, "index.html")
      f = open(index_html_path, "w")

      html_content = "" 
      for image in images:
        html_content += f'<img src="{image}"/>'

      html_string = f"<html><body>{html_content}</body></html>"

      f.write(html_string)
      f.close()

  if not os.path.exists(dest_dir):  
    os.makedirs(dest_dir)

  images = fetch_images()
  create_index_html(images)
  print("Finished")

def main():
  args = sys.argv[1:]

  if not args:
    print('usage: [--todir dir] logfile ')
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print('\n'.join(img_urls))

if __name__ == '__main__':
  main()
