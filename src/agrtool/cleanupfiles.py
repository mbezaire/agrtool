"""This module can be called to cleanup file names by removing version numbers.
    
It will remove the automatic version numbering applied by the Mac or PC OS when
multiple copies of the same file are saved in a directory. This module assumes
there are no duplicate file names in the current path. It can remove the
numbering from all files with particular extensions in a directory. If called 
with a path as a command line argument, the file names in that directory will be 
cleaned. If called without a command line argument, the files in the current 
directory will be cleaned.


Example usage::

    python cleanupfiles.py path/to/directory

    python cleanupfiles.py # run on the current directory

    python -m cleanupfiles path/to/directory
"""
import os
import re  
import sys

def main():
    # call without arguments to use the command line arguments
    clean_files()

def clean_files(path = None):
    """Given a path to a folder of files, clean the file names

    Get a list of all the file names in the folder. For files with
    extensions in the default list (or other supplied list), remove
    any occurrences of numbers added by Mac or PC, like FileName-1.java
    (Mac) becomes FileName.java or data (2).txt (PC) becomes data.txt.
    Rename the files in the folder with the cleaned names.

    :param path: a Path or str object that points to the folder
        where the file names are to be cleaned. If None, the 
        current path is used. defaults to None
    :type path: Path/str, optional
    """

    if path:
        cleanfiles = os.listdir(path)
    else:
        if len(sys.argv) > 1:
            # there should only be one additional argument if calling it with the path.
            # ignoring anything else
            path = sys.argv[1]
            cleanfiles = os.listdir(sys.argv[1])
        else:
            path = './'
            cleanfiles = os.listdir()

    newfiles = []

    for file in cleanfiles:
        newfiles.append(clean_name(file))
        
    for of, nf in zip(cleanfiles,newfiles):
        os.rename(os.path.join(path, of), os.path.join(path,nf))

def clean_name(name, exts = ['.java','.py','.txt','.csv','.c']):
    """Remove number versions automatically added to files on pc or Mac

    When a file of the same name is saved in the same directory, a number
    is often added to the end of the name of the additional file(s). This
    can cause problems for Java class source code where the file and the
    class name need to match, or for programs that read in from data files
    but the data file no longer matches the hard-coded name due to the
    number being added to the file name.

    :param name: Name of file
    :type name: str
    :param exts: List of extensions for which the file names should be cleaned of any numbers, defaults to ``['.java', '.py', '.txt', '.csv', '.c']``.
    :type exts: list, optional.
    :return: A cleaned version of the name (without any number versions)
    :rtype: str
    """

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