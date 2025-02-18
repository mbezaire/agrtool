"""
Author: Marianne Case Bezaire

Produce stock autograder output when a runtime error occurs.
Include any error specifices in the output.
"""

import json
import os
import re
from checklocal import * # gives us localtest, RESULTS_DIR, LOG_DIR, SUB_DIR, RESULTS_FINAL

driver = 'TesterJP' # client code class name

def main():
    check_runtime()

def check_runtime():
    """ Produce a result file with one failed test for program run

    If the running of the program produced a test_error.txt file,
    there was a runtime error. This function will check for the file
    and if it finds the file, indicating an error, it will create a
    results file (for the autograder in Gradescope) to indicate the
    failure and will include the specific error message given.
    """

    # This will be store the combination of all of the individual test results.
    results_all = {'tests': []}

    test = {'score': 0,'max_score': 5,'name': 'Program runs','output': 'Program failed to run. See error message below and resubmit:\n\n','visibility': 'visible'}

    if os.path.exists(LOG_DIR + 'test_error.txt'):
        with open(LOG_DIR + 'test_error.txt', 'r') as fin:
            edited = fin.read()
            checkstr = "Caused by: "
            if "Exception" in edited and checkstr in edited:
                test['output'] +=   edited[(edited.index(checkstr) + len(checkstr)):]
            else:
                test['output'] +=   re.sub(f"at {driver}.main\({driver}.java:[0-9]*\)", '', edited) 

    results_all['tests'] += [test]

    # Write the combined results to the file that Gradescope expects.
    f = open(RESULTS_FINAL, 'w') # type: ignore - imported from checklocal
    json.dump(results_all, f, indent=2)
    f.close()  

if __name__ == "__main__":
    main()

"""
Note: If your autograder uses reflection, 
you can get some very nested exceptions like:

       
    samplestr = 'Exception in thread "main" java.lang.reflect.InvocationTargetException\n' +\
        "at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)" +\
        "at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:77)" +\
        "at java.base/jdk.internal.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)" +\
        "at java.base/java.lang.reflect.Constructor.newInstanceWithCaller(Constructor.java:499)" +\
        "at java.base/java.lang.reflect.Constructor.newInstance(Constructor.java:480)" +\
        "at ConstructorTester.newInstance(ConstructorTester.java:29)" +\
        "at TesterJP.testSubmission(TesterJP.java:70)"
"""