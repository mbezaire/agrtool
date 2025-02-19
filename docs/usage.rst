usage
=====

This package contains modules that are usually called at different points in the autograding process. The process may be mostly contained within the ``run_autograder`` shell script required by Gradescope, or the script may invoke a Python module to coordinate the rest of the steps.

A sample shell script that uses these modules may look like::

    #!/usr/bin/env
    cd /autograder/source
    git pull
    git log -n 1

    # load in a file that contains variable settings
    # to control whether we generically compile and 
    # run the submission or run a specific testing file
    chmod +x /autograder/source/asgnsettings.sh 
    source /autograder/source/asgnsettings.sh

    # copy files into src directory:
    mkdir /autograder/source/src
    cp /autograder/submission/* /autograder/source/src/

    # clean file names to remove any version numbers:
    python3 -m agrtool.src.agrtool.cleanupfiles /autograder/source/src

    chmod +x /autograder/source/tools/compilejava.sh
    source /autograder/source/tools/compilejava.sh
    python3 -m agrtool.src.agrtool.check_compile_error
    python3 -m agrtool.src.agrtool.error_nocompile

    if [ "$runtest" -eq 1 ]; then
        # test that the code runs without exception, manually
        # grade output later in Gradescope
        #
        # add code here to find and run all Java files with
        # main methods

    else
        # Java assignment - specific test using a client class
        sed -i 's/\r$//' "/autograder/source/${asgnpath}grader"
        chmod +x "/autograder/source/${asgnpath}grader"
        source "/autograder/source/${asgnpath}grader"
    fi
    python3 -m agrtool.src.agrtool.error_norun

    # Leaderboard
    python3 -m agrtool.src.agrtool.leaderboard

    # combine all results files into one for Gradescope
    python3 -m agrtool.src.agrtool.combine_results

In addition to the shell script above (which would be in the ``run_autograder`` file), you would also need to include the agrtool package (or a list of dependencies to install), the setup.sh file,
and any other specific files for testing. Zip them up so that they are not within a folder, but
are at the top level of the zip file. See `Gradescope's autograder docs <https://gradescope-autograders.readthedocs.io/>`_ for more instruction.