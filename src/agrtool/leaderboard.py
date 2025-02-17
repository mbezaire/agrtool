import json
import os
from checklocal import * # gives us localtest, RESULTS_DIR, LOG_DIR, SUB_DIR, RESULTS_FINAL

from datetime import datetime, timedelta

auto_test = []

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