"""
Set paths for local or Gradescope environment.

Determine whether this code is running in a Gradescope
Docker environment or on a local machine; set paths
accordingly.
"""

import os

gradescope_path = '/autograder/source'
RESULTS_DIR = './test/'
SUB_DIR = '.'
LOG_DIR = './test/'
localtest = True

def check():
    """Set the path variables to Gradescope paths or local paths.

    Check if a given path exists, one that is likely found on
    Gradescope but not in a local environment. If it is found, set
    all the path variables according to the expected Gradescope
    environment. If the path is not found, set all the variables
    according to the expected local environment.
    """

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


if __name__ == "__main__":
    check()