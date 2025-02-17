import os

gradescope_path = '/autograder/source'
RESULTS_DIR = './test/'
SUB_DIR = '.'
LOG_DIR = './test/'
localtest = True

# check if running in Gradescope docker or local.
# assume local if there's no submission path
if os.path.exists(gradescope_path):
    SUB_DIR = '/autograder/submission/'
    LOG_DIR = '/autograder/source/'    
    RESULTS_DIR = '/autograder/results/'
    localtest = False

RESULTS_FINAL = RESULTS_DIR + 'results.json'

def check():
    if os.path.exists(gradescope_path):
        SUB_DIR = '/autograder/submission/'
        LOG_DIR = '/autograder/source/'    
        RESULTS_DIR = '/autograder/results/'
        localtest = False
    else:
        RESULTS_DIR = './test/'
        SUB_DIR = '.'
        LOG_DIR = './test/'
        localtest = True

    RESULTS_FINAL = RESULTS_DIR + 'results.json'