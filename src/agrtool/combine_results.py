"""
Author: Marianne Case Bezaire

Combine all results json files created by different
processes into one singular results.json for Gradescope
to create its autograder output from.
"""

from datetime import datetime, timedelta
import json
import os

from .checklocal import * # gives us localtest, RESULTS_DIR, LOG_DIR, SUB_DIR, RESULTS_FINAL
from .guidance import email_teacher_incorrect_grader, help_string, what_next
def main():
    generate_results()

def generate_results():
    """Create a summary results json for Gradescope from all results

    Create a placeholder output that reports on compilation and running
    of the program. Then, loop through all the other (results) files in
    the results directory. If there are any results files aside from the
    leaderboard, remove the placeholder output and open the results
    file(s) and load them in. Ensure the json is correct. Add some
    general feedback or tips for students based on their overall score.

    If there is a leaderboard file available, load it in as the
    leaderboard field contents.

    Create a new json structure from all the available results and
    save it in a results file where Gradescope can find it.

    Then, print out the history of submissions so it is available
    in the autograder results on the Gradescope site.
    """

    # This will store the combination of all of the individual test results.
    results_all = {'tests': []}

    auto_test = {'score': 1,'max_score': 1,'name': 'Project compilation','output': 'Program compiles!','visibility': 'visible'}
    printed_output = ""
    if os.path.exists(LOG_DIR + 'classes/test_results.txt'):
        with open(LOG_DIR + 'classes/test_results.txt', 'r') as fin:
            printed_output = fin.read() 
            auto_test['output'] +=   printed_output

    error_flag = False

    if os.path.exists(LOG_DIR + 'classes/test_error.txt'):
        with open(LOG_DIR + 'classes/test_error.txt', 'r') as fin:
            error_string = fin.read() 
            error_string = error_string.replace("Error: Could not find or load the necessary classes","Encountered an error during auto-testing:")
            auto_test['output'] +=   error_string    
            if len(error_string)>1:
                error_flag = True
                
    if (error_flag):
        auto_test['score'] = 0    
        
    results_all['tests'] += [auto_test]
        
    json_files = [f for f in os.listdir(RESULTS_DIR) if f[-5:] == '.json']
    json_files.sort()

    # Process each file, adding its test results to results_all.
    if len(json_files) > 0:
        
        for file in json_files:
            if 'leaderboard' not in file:
                print("Triggering deletion...")
                print(results_all)
                results_all['tests'] = []

        for fname in json_files:       
            f_results, mystr = getokjson(fname)

            if 'leaderboard' in fname:
                results_all['leaderboard'] = f_results
            else:
                if type(f_results) == list:
                    results_all['tests'] += [{"name":"Autograder Error","output":email_teacher_incorrect_grader},
                                            {"name":"json issues at positions:","output":", ".join([str(i) for i in f_results]), "visibility":"hidden"}]
                                            #{"name":"json:","output":mystr, "visibility":"hidden"}]
                    print(mystr)
                    results_all['score'] = 0
                else: # dict
                    results_all['tests'] += f_results['tests']

    results_all['tests'] += [{"name":"Printed Output", "output":printed_output}]  

    # try:
    #     with open('/autograder/source/classes/error.txt', 'r') as fin:
    #         test['output'] +=   fin.read()   
    # It looks like your tester file works, but the autograder didn't supply any inputs for the Scanner.    

    if os.path.exists('/autograder/submission_metadata.json'):
        with open('/autograder/submission_metadata.json', 'r') as fin:
            print_history(json.load(fin))
            
    # check if less than full autograder credit. If so, add a blue entry at top:
    score = 0
    total = 0
    for test in results_all['tests']:
        if 'score' not in test or 'max_score' not in test: continue
        score += test['score']
        total += test['max_score']

    if score < total:
        test = {"output_format": "html", "output":help_string}
        results_all['tests'].insert(0, test)

    elif len(what_next) > 0:
        test = {"output_format": "html", "output":what_next}
        results_all['tests'].insert(0, test)

    # Write the combined results to the file that Gradescope expects.
    f = open(RESULTS_FINAL, 'w') # type: ignore - imported from checklocal
    json.dump(results_all, f, indent=2)
    f.close()

def getdate(datestr):
    """Convert a Gradescope datetime stamp to a datetime object

    This function takes in a string of a Gradescope datetime
    stamp (probably the submission time) and converts it into
    a datetime object, adds 3 hours (for US Eastern time) and
    then converts the datetime back to a string, formatted
    differently than the input.

    :param datestr: A string containing a datetime stamp
    :type datestr: str
    :return: A datetime string, formatted differently, representing
        the datetime from the string parameter (with three hours
        added for US East Coast time)
    :rtype: str
    """

    # Convert a Gradescope datetime stamp to a datetime object

    # This function takes in a string of a Gradescope datetime
    # stamp (probably the submission time) and converts it into
    # a datetime object, adds 3 hours (for US Eastern time) and
    # then converts the datetime back to a string, formatted
    # differently than the input.

    # Args:
    #     datestr (str): A string containing a datetime stamp

    # Returns:
    #     str: A datetime string, formatted differently, representing
    #     the datetime from the string parameter (with three hours
    #     added for US East Coast time)

    subdate = datetime.strftime(datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%f%z") + timedelta(hours = 3),"%b %d, %I:%M:%S %p")
    return subdate

def makedate(datestr):
    """Convert a Gradescope datetime stamp to a datetime object

    This function takes in a string of a Gradescope datetime
    stamp (probably the submission time) and converts it into
    a datetime object. It also adds 3 hours to account for the
    timezones (assuming the user is on US East Coast)

    Args:
        datestr (str): A string containing a datetime stamp

    Returns:
        datetime object: A datetime object representing the
        datetime from the string parameter
    """

    return datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%f%z") + timedelta(hours = 3)

def lateness(f_results):
    """Computes the penalty for late submissions

    Given the submission date(s) and the due date, calculates how much of
    a penalty to assess. If the student turns in their work before the
    due date, this function returns 0. If the student turned in multiple
    submissions, and the first one was before the due date but the latest
    one is after the due date, the student's penalty will be smaller. The
    penalty is capped at 0.5.

    Args:
        f_results (dict): a dictionary of Gradescope submission data

    Returns:
        float or int: size of the penality to assess, between 0 and 0.5
    """

    # numsubs = len(f_results['previous_submissions'])
    if f_results['created_at'] <= f_results['users'][0]['assignment']['due_date']:
        return 0
    days_late = makedate(f_results['created_at']) - makedate(f_results['users'][0]['assignment']['due_date'])
    late_score = max(0.5, days_late.total_seconds()/(24*3600))
    
    if f_results['previous_submissions'][0]['submission_time'] <= f_results['users'][0]['assignment']['due_date']:
        n = 0
        for sub in f_results['previous_submissions']:
            if sub['submission_time'] <= f_results['users'][0]['assignment']['due_date']:
                n += 1
        reprieve =  (n/(len(f_results['previous_submissions']) + 1))*.5 + .5
    else:
        reprieve = 1
        
    return late_score * reprieve
 

def print_history(f_results):
    """Reads submission metadata, prints out all submission datetimes and points

    Given a json structure (dict) read from a file of Gradescope submission
    metadata, this function extracts all submission datetimes and points achieved
    and prints them out, which can be collected into a hidden autograder listing
    to view while grading or reviewing submissions on the Gradescope site.

    Args:
        f_results (json): a dict from a json file of Gradescope submission data
    """

    numsubs = len(f_results['previous_submissions'])
    if numsubs == 0:
        print("This is the first submission")
        if f_results['created_at'] <= f_results['users'][0]['assignment']['due_date']:
            print("ON TIME")
    else:
        highest = 0
        for sub in f_results['previous_submissions']:
            if float(sub['score']) > highest:
                highest = float(sub['score'])
        print("Previous submissions: " + str(numsubs) + ", highest PREVIOUS score: " + str(highest))
        desc = 'none of the'
        if f_results['previous_submissions'][0]['submission_time'] <= f_results['users'][0]['assignment']['due_date']:
            n = 1
            desc = 'first'
            while n < numsubs and f_results['previous_submissions'][n - 1]['submission_time'] <= f_results['users'][0]['assignment']['due_date']:
                n += 1
            if f_results['created_at'] <= f_results['users'][0]['assignment']['due_date']:
                desc = 'all'
                n += 1
            print(f"ON TIME {desc} {n} submissions")
        count = 1
        for submission in f_results['previous_submissions']:
            score = f_results['previous_submissions'][count - 1]['score']
            subdate = getdate(f_results['previous_submissions'][count - 1]['submission_time'])
            #result = f_results['previous_submissions'][count - 1]['results']['score']
            print(f'#{count:2}: {score:4} {subdate}' )#+ (f' - Graded: {result}' if result != None else ''))
            count += 1
    subdate = getdate(f_results['created_at'])
    print(f"Now:      {subdate}")#+ (f' - Graded: {result}' if result != None else ''))
    print("Due:      " + getdate(f_results['assignment']['due_date']))



def getokjson(fname):
    """Cleans common escape-related errors from a json file

    This function opens up a json file (fname), reads it in, and
    while there are any errors parsing the json content of the file,
    it checks the error location for any un-escaped or improperly
    escaped characters, swaps them out, and continues checking and
    swapping (up to 10 times). Then, it creates the json structure
    and returns that along with the (corrected) string input.

    Args:
        fname (str): name of a json file

    Returns:
        json, str: a json structure, and stringified json
    """

    fname = RESULTS_DIR + fname
    check = 10
    f = open(fname, 'r')
    mystr = f.read()
    f.close()
    f_results = []
    while check > 0:
        try:
            f_results = json.loads(mystr)
        except json.JSONDecodeError as err:
            if mystr[err.pos] == "\n":
                mystr = mystr[:err.pos] + "\\n" + mystr[err.pos + 1:]
            elif mystr[err.pos] == "\t":
                mystr = mystr[:err.pos] + "\\t" + mystr[err.pos + 1:]
            elif mystr[err.pos] == "\\":
                mystr = mystr[:err.pos] + "\\\\" + mystr[err.pos + 1:]
            elif mystr[err.pos] == '\"':
                mystr = mystr[:err.pos] + '\\"' + mystr[err.pos + 1:]
            check -= 1
            f_results.append(err.pos)
        else:
            check = 0
        return f_results, mystr


if __name__ == "__main__":
    main()