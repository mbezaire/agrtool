"""
Author: Marianne Case Bezaire

Create strings of guidance for common autograder results

For each of the following variables, adjust the docstring
to your liking; it will be imported by modules that refer
to it when adding feedback for submitters to Gradescope
assignments.
"""

email_teacher_incorrect_grader = \
    "not all results were loaded correctly " +\
    "- email your teacher a link to this page"

help_string = "This code doesn't pass all the autograder " +\
    " checks yet.\nLook at the feedback below for details.\n" + \
    "If you're still stuck after, use the <a target=\"_blank\" " + \
    "href=\"https://udl4cs.education.ufl.edu/debugging-detective/\">Debugging Detective</a>"

what_next = "All logic checks passed!\nWould you like to add " +\
    "a README for this assignment with some notes?"

error_advice = 'check out our classroom error reference page.'

java_specific = {
    'class, interface, enum, or record expected': 
        "You may have an issue with curly braces! Do you\n" +\
        "close off your class definition too early with\n" +\
        "a premature close curly brace }?\n",

    "error: '.class' expected":
        "You may be (re)declaring arguments as you pass them\n" +\
        "to methods/constructors. When passing arguments\nto " +\
        "method calls, you should only pass values\nor variables " +\
        "that you've already declared and already\nassigned a value -" +\
        " don't declare in the method call!\n",

    'cannot find symbol':
        "You may have a typo in a variable name or method name,\nOR " +\
        "you may have called a method without including parenthesis\nat " +\
        "the end of the method name. Parenthesis are\nalways required for " +\
        "method calls, even if you\nare not passing any arguments.\n",

    'int this.':
        "You might be trying to (re)declare an instance field\n" +\
        "within a method. This is not possible - you've already " +\
        "declared\nthe variable as a field, so you don't need\nto " +\
        "declare it again. Also, you run the risk\nof declaring a " +\
        "local variable of the same name\nthat blocks access " +\
        "to the instance field within\nthe method where you declared " +\
        "the local variable.\n",

    'cannot be referenced from a static':
        "It looks like you may have accidentally declared an\n" +\
        "object-level method as static. Object-level methods\n" +\
        "like setters and getters cannot be static (class level),\n" +\
        "they are meant to be used with specific objects of the class.\n",
    }
