import os
from pathlib import Path
from checklocal import * # gives us localtest, RESULTS_DIR, LOG_DIR, SUB_DIR, RESULTS_FINAL

def main(pth = LOG_DIR):
    check_unchecked(pth)

def check_unchecked(pth):
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