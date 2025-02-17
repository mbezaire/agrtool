import json
import os

driver = 'Driver'
localtest = False

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
        
    test = {'score': 0,'max_score': 5,'name': f'{driver}.java file','output': f'No {driver}.java file found.\nResubmit with {driver}.java, which must\ncontain code to create your child class object(s).','visibility': 'visible'}

    if os.path.exists('/autograder/source/compile_error.txt'):
        with open('/autograder/source/compile_error.txt', 'r') as fin:
            test['output'] +=   fin.read() 

    results_all['tests'] += [test]

    # Write the combined results to the file that Gradescope expects.
    f = open(RESULTS_FINAL, 'w')
    json.dump(results_all, f, indent=2)
    f.close()


if __name__ == "__main__":
    main()