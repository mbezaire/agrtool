from datetime import datetime, timedelta
import json
import os


localtest = False
if os.path.exists('/autograder/source'):
    LOG_DIR = '/autograder/source/'    
    RESULTS_DIR = '/autograder/results/'
else: # localtest
    RESULTS_DIR = './test/'
    LOG_DIR = './test/'
    localtest = True

RESULTS_FINAL = RESULTS_DIR + 'results.json'

def main():
    # This will store the combination of all of the individual test results.
    results_all = {'tests': []}

    auto_test = {'score': 1,'max_score': 1,'name': 'Project compilation','output': 'Program compiles!','visibility': 'visible'}
    printed_output = ""
    if os.path.exists('/autograder/source/classes/test_results.txt'):
        with open('/autograder/source/classes/test_results.txt', 'r') as fin:
            printed_output = fin.read() 
            auto_test['output'] +=   printed_output

    error_flag = False

    if os.path.exists('/autograder/source/classes/test_error.txt'):
        with open('/autograder/source/classes/test_error.txt', 'r') as fin:
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
                    results_all['tests'] += [{"name":"Autograder Error","output":"not all results were loaded correctly - email Dr. Bezaire a link to this page"},
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
    elif os.path.exists('submission_metadata_other.json'):
        with open('submission_metadata_ethan.json', 'r') as fin:
            f_results = json.load(fin)
            print_history(f_results)
            
    # check if less than full autograder credit. If so, add a blue entry at top:

    score = 0
    total = 0
    for test in results_all['tests']:
        if 'score' not in test or 'max_score' not in test: continue
        score += test['score']
        total += test['max_score']

    if score < total:
        helpstr = "This code doesn't pass all the autograder checks yet.\nLook at the feedback below for details.\n" + \
                    "If you're still stuck after, use the <a target=\"_blank\" href=\"https://udl4cs.education.ufl.edu/debugging-detective/\">Debugging Detective</a>"
        test = {"output_format": "html", "output":helpstr}
        results_all['tests'].insert(0, test)

    # else:
    #     helpstr = "All logic checks passed!\nWould you like to add a README for this assignment with some notes?"
    #     test = {"output_format": "html", "output":helpstr}
    #     results_all['tests'].insert(0, test)

    # Write the combined results to the file that Gradescope expects.
    f = open(RESULTS_FINAL, 'w')
    json.dump(results_all, f, indent=2)
    f.close()

def getdate(datestr):
    subdate = datetime.strftime(datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%f%z") + timedelta(hours = 3),"%b %d, %I:%M:%S %p")
    return subdate

def print_history(f_results):
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