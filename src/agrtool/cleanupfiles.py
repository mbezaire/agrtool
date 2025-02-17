# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 21:41:44 2022

@author: marianne.bezaire
"""

import os
import re  
import sys

def main():
    clean_files()

def clean_files(path = None):
    if path:
        cleanfiles = os.listdir(path)
    else:
        if len(sys.argv) > 1:
            # there should only be one additional argument if calling it with the path.
            # ignoring anything else
            cleanfiles = os.listdir(sys.argv[1])
        else:
            cleanfiles = os.listdir()

    newfiles = []

    for file in cleanfiles:
        newfiles.append(clean_name(file))
        
    for of, nf in zip(cleanfiles,newfiles):
        os.rename(os.path.join(path, of), os.path.join(path,nf))

def clean_name(name, exts = ['.java','.py','.txt','.csv','.c']):
    if type(exts) == list:
        if len(exts) == 0 or not any(name.endswith(extension) for extension in exts):
            return name
    elif type(exts) == str and len(exts) > 0:
        if '.' not in exts:
            exts = '.' + exts
            if not name.endswith(exts):
                return name
            exts = [exts]

    # exts is a (now) list of extensions and name ends with one of them, or exts is None
    filext = '.' + name.split('.')[-1]

    # strip off numbering from mac and/or pc
    while re.findall(rf"(-[0-9]+|[\s]*\([0-9]+\)){filext}", name):
        name = re.sub(rf"(-[0-9]+|[\s]*\([0-9]+\)){filext}", filext, name)

    return name

if __name__ == "__main__":
    main()