"""
Author: Marianne Case Bezaire

Creates a leaderboard (if desired). Modify the logic below
to adjust the leaderboard categories and weighting. The
combine_results.py module will incorporate the leaderboard
logic below into its results.json as a separate key. When
Gradescope receiveds a results.json with a 'leaderboard'
key, it includes a leaderboard that is viewable to submitters.
"""

import json
import os
from checklocal import * # gives us localtest, RESULTS_DIR, LOG_DIR, SUB_DIR, RESULTS_FINAL
from combine_results import makedate, getdate, lateness

auto_test = []

RESULTS_FINAL = RESULTS_DIR + 'leaderboard.json'

def get_sub_data(subdata):
    submitters = len(subdata['users'])
    subbed = lateness(subdata)
    return submitters, subbed    
    
def main():
    leaderboard()

def leaderboard():
    """Create a leaderboard json for use by Gradescope

    For this submission, read in the submission_metadata.json created
    by Gradescope, get the submitters and their timeliness, and then
    create the leaderboard json structure and data, and write it out
    to leaderboard.json for Gradescope to create the leaderboard from.
    """

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