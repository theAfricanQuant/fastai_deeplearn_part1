#!/usr/bin/env python

# Objective:  run a script to check an *.md file to see that all links are valid

# EXAMPLE of how to run file:  
"""
▶ pwd
/Users/reshamashaikh/ds/my_repos/fastai_deeplearn_part1/tools

my_repos/fastai_deeplearn_part1/tools 
▶ python check_links.py -v /Users/reshamashaikh/ds/my_repos/fastai_deeplearn_part1/README.md
VALID   http://www.fast.ai
VALID   http://forums.fast.ai/c/part1-v2
VALID   http://forums.fast.ai/c/part1v2-beg
VALID   https://github.com/fastai/fastai
VALID   tools/aws_ami_gpu_setup.md
VALID   tools/tmux.md
VALID   resources.md

my_repos/fastai_deeplearn_part1/tools
▶ python check_links.py -v /Users/reshamashaikh/ds/my_repos/fastai_deeplearn_part1/tools/tmux.md
VALID   #section-a
VALID   #section-b
VALID   #section-c
VALID   #section-d
VALID   #section-e
VALID   https://hackernoon.com/a-gentle-introduction-to-tmux-8d784c404340
VALID   https://alekshnayder.com
VALID   http://console.aws.amazon.com/

"""

# Running Python 3

__author__ = 'taylanbil'


import os
import markdown
from argparse import ArgumentParser

from bs4 import BeautifulSoup


class LinkChecker(object):

    def __init__(self, mdfilename, verbose=False):
        """
        input: mdfilename has to be the full path!!!
        """
        self.mdfilename = mdfilename
        self.path = os.path.abspath(os.path.dirname(mdfilename))
        self.soup = self.get_soup()
        self.verbose = verbose

    def validate_link(self, link):
        if link.startswith('http'):
            return True
        elif link.startswith('#'):
            return bool(self.soup.find_all('a', {'name': link[1:]}))
        elif link.startswith('/'):
            return os.path.exists(os.path.join(self.path, link[1:]))
        else:
            return os.path.exists(os.path.join(self.path, link))

    def get_soup(self):
        with open(self.mdfilename, 'r') as f:
            md = markdown.markdown(f.read())
        return BeautifulSoup(md, "lxml")

    def get_links(self):
        for link in self.soup.find_all('a', href=True):
            yield link['href']

    def process_link(self, link):
        isvalid = 'VALID' if self.validate_link(link) else 'INVALID'
        if self.verbose or isvalid == 'INVALID':
            print('{isvalid}\t{link}'.format(isvalid=isvalid, link=link))

    def main(self):
        for link in self.get_links():
            self.process_link(link)


def get_namespace():
    parser = ArgumentParser()
    parser.add_argument(
        'mdfilename', help='''full path to the .md file you would like
        to check links in''')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='''verbose flag. if specified, prints all links with
        results. Otherwise, prints invalid links only''')
    return parser.parse_args()


if __name__ == '__main__':
    ns = get_namespace()
    LC = LinkChecker(ns.mdfilename, verbose=ns.verbose)
    LC.main()

    # # a test here
    # mdfile = '/Users/reshamashaikh/ds/my_repos/fastai_deeplearn_part1/README.md'
    # LC = LinkChecker(mdfile)
    # LC.main()

