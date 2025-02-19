"""
Remove compile errors from autograder output if they are warnings.

Remove any compile error flags if they are only warnings
and compilation actually succeeded. So far this is very
specific and only removes the file if it sees 'unchecked'
more than once per line in the error file.
"""

import os
from pathlib import Path
from .checklocal import * # gives us localtest, RESULTS_DIR, LOG_DIR, SUB_DIR, RESULTS_FINAL

def main(pth = LOG_DIR):
    check_unchecked(pth)

def check_unchecked(pth):
    """ Remove an unnecessary error file when compilation succeeded

    If the program compiled successfully but left a warning message,
    an error file is created and could cause later functionality to
    wrongly indicate the program did not compile. This program checks
    for a specific common "false positive" - if the file contains the
    word "unchecked" and only a couple lines, remove the file so it
    doesn't wrongly appear that the program failed to compile.
    """
        
    # convert pth argument to Path if it is a str
    if type(pth) == str:
        pth = Path(pth)
    remove_flag = False

    # check if there is an error message from attempting to compile
    if os.path.exists(pth / 'compile_errortester.txt'):

        # if so, check if the only messages in the error are about
        # unchecked exceptions / XLint that can be disregarded in
        # student submissions
        with open(pth / 'compile_errortester.txt', 'r') as fin:
            edited = fin.read()
            if edited.count("unchecked") > edited.count("\n") - 2:
                remove_flag = True

    # if the only problem in the file can be ignored, remove the file   
    if remove_flag:
        os.remove(pth / 'compile_errortester.txt')

if __name__ == "__main__":
    main()