#!/bin/env python3
# -*- coding: utf-8 -*-
#
# skim_svn_status3.py : 
#   - Skim svn status output to dealing with filename issue on macOS. 
#      by Uji Nanigashi (53845049+nanigashi-uji@users.noreply.github.com)
#

import os
import sys
import re
import subprocess
import unicodedata
import argparse

def unicode_norm_filechk(path):
    for frm in ['NFC','NFKC','NFD','NFKD']: 
        if os.path.exists(unicodedata.is_normalized(frm, path)):
            return True
    return False

def main():
    """
    Skim svn status output to dealing with filename issue on macOS. 
    """
    argpsr = argparse.ArgumentParser(description='Example: showing greeting words')
    argpsr.add_argument('svnarguments', nargs='*', type=str, default=[],  help='Arguments for svn command')
    argpsr.add_argument('-v', '--verbose', action='store_true', help='Show verbose output')
    argpsr.add_argument('-i', '--ignore-pattern', action='append', help='Add file name pattern to ignore (regular expression)')
    argpsr.add_argument('-m', '--ignore-msoffice-tmp', action='store_true', help='Ignore temporary file by MS-Office ~$*.(docx|xlsx|pptx)')
    argpsr.add_argument('-g', '--ignore-dot-git-dir',  action='store_true', help='Ignore .git directory')
    argpsr.add_argument('-p', '--ignore-python-site-packages-dir',  action='store_true', help='../lib/python/site-package/?.?...')
    args = argpsr.parse_args()

    proc = subprocess.Popen(["svn", "status"]+args.svnarguments,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    data = {}
    ignore_patterns=[]
    pttrn = re.compile(r'^(?P<vflag>[ ADMRCXI\?\!~])(?P<pflag>[ MC])(?P<dlflag>[ L])(?P<aflag>[ \+])(?P<Pflag>[ S])(?P<flflag>[ KOTB])(?P<uflag>[ *])?(?P<padding>\s*)(?P<fname>\S.*)\s*$')

    if args.ignore_msoffice_tmp:
        ignore_patterns.append(re.compile(r'~\$.*(xlsx?|docx?|pptx?)\s*$'))
    if args.ignore_dot_git_dir:
        ignore_patterns.append(re.compile(r'[\w/].git(/.*)?\s*$'))
    if args.ignore_python_site_packages_dir:
        ignore_patterns.append(re.compile(r'/lib/python/site-packages/\d.*$'))

    if args.ignore_pattern is not None:
        for ipattern in args.ignore_pattern:
            ignore_patterns.append(re.compile(ipattern))

    while True:
        line = proc.stdout.readline()
        if len(line)>0:
            m = pttrn.search(line.rstrip(b'\n').decode())
            if m:
                fn = unicodedata.normalize('NFD', m.group('fname'))
                if data.get(fn) is None:
                    data.update({fn: {'vflag': [ str(m.group('vflag')) ],
                                      'line' : [ str(line.rstrip(b'\n').decode()) ] }})
                else:
                    data.get(fn).get('vflag').append(str(m.group('vflag')))
                    data.get(fn).get('line').append(str(line.rstrip(b'\n').decode()))
            else:
                sys.stderr.write("Unknown statement:"+line.decode())

        if not line and proc.poll() is not None:
            break


    for fn in sorted(data.keys()):
        if '?' in data.get(fn).get('vflag') and '!' in data.get(fn).get('vflag'):
            if args.verbose:
                print('Skip:  ', fn, data.get(fn).get('vflag'))
            continue
        elif '!' in data.get(fn).get('vflag') and unicode_norm_filechk(fn):
            if args.verbose:
                print('Fake-!:', fn, data.get(fn).get('vflag'))
            continue
        else:
            flg_ignore=False
            for pttrn2 in ignore_patterns:
                if pttrn2.search(fn):
                    flg_ignore=True
                    if args.verbose:
                        print('Ignore:', fn, data.get(fn).get('vflag'))
                    break
            if flg_ignore:
                continue

        for l in data.get(fn).get('line'):
            print(str(l))


if __name__ == '__main__':
    main()
