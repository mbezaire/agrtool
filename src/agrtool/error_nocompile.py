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
    RESULTS_DIR = './'
    LOG_DIR = './'
    
RESULTS_FINAL = RESULTS_DIR + 'results.json'

def main():
    # This will be store the combination of all of the individual test results.
    results_all = {'tests': []}
        
    test = {'score': 0,'max_score': 1,'name': 'Project compilation','output': 'This code doesn\'t compile yet. It generated the following error:\n\n','visibility': 'visible'}

    if os.path.exists(LOG_DIR + 'compile_errortester.txt'):
        with open(LOG_DIR + 'compile_errortester.txt', 'r') as fin:
            edited = fin.read().replace("location: class TesterJP","")
            msg = ""
            # Java specific help
            if 'class, interface, enum, or record expected' in edited:
                msg += "\nYou may have an issue with curly braces! Do you\nclose off your class definition too early with\na premature close curly brace }?\n"
            if "error: '.class' expected" in edited:
                msg += "\nYou may be (re)declaring arguments as you pass them\nto methods/constructors. When passing arguments\nto method calls, you should only pass values\nor variables that you've already declared and already\nassigned a value - don't declare in the method call!\n"
            if 'cannot find symbol' in edited:
                msg += "\nYou may have a typo in a variable name or method name,\nOR you may have called a method without including parenthesis\nat the end of the method name. Parenthesis are\nalways required for method calls, even if you\nare not passing any arguments.\n"
            if 'int this.' in edited:
                msg += "\nYou might be trying to (re)declare an instance field\nwithin a method. This is not possible - you've already declared\nthe variable as a field, so you don't need\nto declare it again. Also, you run the risk\nof declaring a local variable of the same name\nthat blocks access to the instance field within\nthe method where you declared the local variable.\n"
            if 'cannot be referenced from a static' in edited:
                msg += "\nIt looks like you may have accidentally declared an\nobject-level method as static. Object-level methods\nlike setters and getters cannot be static (class level),\nthey are meant to be used with specific objects of the class.\n"
            test['output'] +=   re.sub(f'src/{driver}.java:[0-9]*[:]* ', '', msg + "\n" + edited) 
            test['output'] += "\n\nIf you're not sure what to do with this error, check out our error board or ask the CS50 duck or our Stack Overflow site.\n"

    results_all['tests'] += [test]

    # Write the combined results to the file that Gradescope expects.
    f = open(RESULTS_FINAL, 'w')
    json.dump(results_all, f, indent=2)
    f.close()


if __name__ == "__main__":
    main()