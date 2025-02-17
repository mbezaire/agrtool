import os
from pathlib import Path

localtest = False

# check if running in Gradescope docker or local.
# assume local if there's no /autograder/submission/ path
if os.path.exists('/autograder/submission/'): 
    RESULTS_DIR =  '/autograder/results/'
    LOG_DIR = '/autograder/source/'    
else:
    RESULTS_DIR = './'
    LOG_DIR = './'
    localtest = True


def main(pth = LOG_DIR):
    check_unchecked(pth)

def check_unchecked(pth):
    if type(pth) == str:
        pth = Path(pth)
    remove_flag = False

    if os.path.exists(pth / 'compile_errortester.txt'):
        with open(pth / 'compile_errortester.txt', 'r') as fin:
            edited = fin.read()
            if edited.count("unchecked") > edited.count("\n") - 2:
                remove_flag = True
                
    if remove_flag:
        os.remove(pth / 'compile_errortester.txt')

if __name__ == "__main__":
    main()