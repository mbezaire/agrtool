import json
import os

from datetime import datetime, timedelta

localtest = False

if os.path.exists('/autograder/source'):
    LOG_DIR = '/autograder/source/'    
    RESULTS_DIR = '/autograder/results/'
else: # localtest
    RESULTS_DIR = './test/' # '/autograder/results/'
    LOG_DIR = './test/' #'/autograder/source/'
    localtest = True

RESULTS_FINAL = RESULTS_DIR + 'leaderboard.json'



auto_test = []

# # This will store the combination of all of the individual test results.    
# error_flag = False;

# if os.path.exists('/autograder/source/classes/test_error.txt'):
#     with open('/autograder/source/classes/test_error.txt', 'r') as fin:
#         error_string = fin.read() 
#         error_string = error_string.replace("Error: Could not find or load the necessary classes","Encountered an error during auto-testing:")
#         auto_test['output'] +=   error_string    
#         if len(error_string)>1:
#             error_flag = True
            
# if (error_flag):
#     auto_test.append({"name": "Errors", "value": 1, "order": "asc"})
# else:
#     auto_test.append({"name": "Errors", "value": 0, "order": "asc"})
  
# {"name": "Accuracy", "value": .926},
    


def getdate(datestr):
    subdate = datetime.strftime(datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%f%z") + timedelta(hours = 3),"%b %d, %I:%M:%S %p")
    return subdate

def makedate(datestr):
    return datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%f%z") + timedelta(hours = 3)
    
def lateness(f_results):
    numsubs = len(f_results['previous_submissions'])
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
 

def get_sub_data(subdata):
    submitters = len(subdata['users'])
    subbed = lateness(subdata)
    return submitters, subbed    
    
def main():

    if os.path.exists('/autograder/submission_metadata.json'):
        with open('/autograder/submission_metadata.json', 'r') as fin:
            submitters, first_time = get_sub_data(json.load(fin))
    # elif os.path.exists('submission_metadata_other.json'):
    #     with open('submission_metadata_ethan.json', 'r') as fin:
    #         submitters, first_time = get_sub_data(json.load(fin))

    numstars = 5
    if submitters < 2:
        numstars -= 1
    if first_time > 0:
        numstars -= 1
        if first_time > 2:
            numstars -= 1

    auto_test.append({"name": "Stars", "value": "*"*numstars})
    auto_test.append({"name": "Submitters", "value": submitters})
    auto_test.append({"name": "Timeliness", "value": first_time, "order": "asc"})


    # Write the combined results to the file that Gradescope expects.
    f = open(RESULTS_FINAL, 'w')
    json.dump(auto_test, f, indent=2)
    f.close()


if __name__ == "__main__":
    main()