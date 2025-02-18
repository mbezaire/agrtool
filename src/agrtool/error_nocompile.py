"""
Author: Marianne Case Bezaire

Produce a stock autograder output when files fail to
compile. Include the compilation error message(s) for
details.
"""

import json
import os
import re
from checklocal import * # gives us localtest, RESULTS_DIR, LOG_DIR, SUB_DIR, RESULTS_FINAL
from guidance import error_advice, java_specific
driver = 'TesterJP' # client code class 

def main():
    check_compile()

def check_compile():
    """ Produce a result file with one failed test for compilation

    If compiling the program produced a compile_errortester.txt file,
    there was a compilation error. This function will check for the file
    and if it finds the file, indicating an error, it will create a
    results file (for the autograder in Gradescope) to indicate the
    failure and will include the specific error message given.
    """

    # This will be store the combination of all of the individual test results.
    results_all = {'tests': []}
        
    test = {'score': 0,'max_score': 1,'name': 'Project compilation','output': 'This code doesn\'t compile yet. It generated the following error:\n\n','visibility': 'visible'}

    if os.path.exists(LOG_DIR + 'compile_errortester.txt'):
        with open(LOG_DIR + 'compile_errortester.txt', 'r') as fin:
            edited = fin.read().replace(f"location: class {driver}","")
            msg = ""
            # Java specific help
            for problem in java_specific:
                if problem in edited:
                    msg += "\n" + java_specific[problem]
            test['output'] +=   re.sub(f'src/{driver}.java:[0-9]*[:]* ', '', msg + "\n" + edited) 
            test['output'] += f"\n\nIf you're not sure what to do with this error, {error_advice}\n"

    results_all['tests'] += [test]

    # Write the combined results to the file that Gradescope expects.
    f = open(RESULTS_FINAL, 'w') # type: ignore - imported from checklocal
    json.dump(results_all, f, indent=2)
    f.close()


if __name__ == "__main__":
    main()