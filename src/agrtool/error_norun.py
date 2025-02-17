import json
import os
import re

localtest = False
driver = 'TesterJP'
if os.path.exists('/autograder/source'):
    RESULTS_DIR =  '/autograder/results/'
    LOG_DIR = '/autograder/source/'    
else:
    localtest = True
    RESULTS_DIR = './' # '/autograder/results/'
    LOG_DIR = './' #'/autograder/source/'
    
RESULTS_FINAL = RESULTS_DIR + 'results.json'

def main():
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
    f = open(RESULTS_FINAL, 'w')
    json.dump(results_all, f, indent=2)
    f.close()

        
    samplestr = 'Exception in thread "main" java.lang.reflect.InvocationTargetException\n' +\
        "at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)" +\
        "at java.base/jdk.internal.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:77)" +\
        "at java.base/jdk.internal.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)" +\
        "at java.base/java.lang.reflect.Constructor.newInstanceWithCaller(Constructor.java:499)" +\
        "at java.base/java.lang.reflect.Constructor.newInstance(Constructor.java:480)" +\
        "at ConstructorTester.newInstance(ConstructorTester.java:29)" +\
        "at TesterJP.testSubmission(TesterJP.java:70)"
    

if __name__ == "__main__":
    main()