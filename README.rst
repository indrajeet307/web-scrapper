Problem Statement
=================

Write an app/program to scan through a given webpage, and display the
top 10 frequent words and the top 10 frequent word pairs (two words in
the same order) along with their frequency. In case the webpage
contains hyperlinks, these hyperlinked urls need to be expanded and
the words on these pages also should be scanned to come up with the
frequent words.

Important points to note:
    1. You will have to assume that the maximum number of levels you
       have to expand for urls within a url as 4
    2. Ignore any external url links

Test URL for the Problem
========================

Use 314e.com website as one of your test data, as we will use this url
to check the validity of your program.

Evaluation criteria
===================

    1. Overall architecture. Provide a write up explaining your
       choices and the architecture as comments in the code.
    2. Thoroughness in testing
    3. How well modelled your code is.
    4. Readability
    5. Extensibility
    6. Logic
    7. Build scripts that will easily integrate with an automated
       CI/CD pipeline. It should build out your solution, execute it,
       run tests, handle dependencies etc.
    8. A useful Readme file
