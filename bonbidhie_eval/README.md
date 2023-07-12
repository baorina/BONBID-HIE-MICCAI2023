# bonbidhie2023_eval Evaluation

The source code for the evaluation container for
bonbidhie2023_eval, generated with
evalutils version 0.4.2
using Python 3.8.

Before running, you will need a local docker installation.
For more details, please read grand-challenge documents https://grand-challenge.org/documentation/automated-evaluation/ and https://comic.github.io/evalutils/usage.html 
Please follow these steps to run it on the local machine.

(1) mkdir groud-truth

Put your ground-truth *.mha in the folder

(2) mkdir test

Put your prediction *.mha in the folder

(3) Based on the number of cases you want to evaluate, please change the num_cases in evaluation.py line 881.

(4)./build.sh

(5)./test.sh

