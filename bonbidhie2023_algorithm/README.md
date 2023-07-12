# bondbidhie2023_algorithm Algorithm Docker

The source code for the algorithm container for
bondbidhie2023_algorithm, generated with
evalutils version 0.4.2
using Python 3.8.


Before running, you will need a local docker installation.
For more details, please read grand-challenge documents [https://grand-challenge.org/documentation/automated-evaluation/](https://grand-challenge.org/documentation/creating-an-algorithm-container/) and [https://comic.github.io/evalutils/usage.html](https://comic.github.io/evalutils/usage.html#algorithm-container) 


Please follow these steps to run it on the local machine.


(1)./build.sh

(2)./test.sh

In order to generate the results locally and test your codes, 
In test.sh, use this piece of codes:

docker run --rm \
        --memory="${MEM_LIMIT}" \
        --memory-swap="${MEM_LIMIT}" \
        --network="none" \
        --cap-drop="ALL" \
        --security-opt="no-new-privileges" \
        --shm-size="128m" \
        --pids-limit="256" \
        -v $SCRIPTPATH/test/:/input/ \
        -v $SCRIPTPATH/output/:/output/ \
        bondbidhie2023_algorithm

But for uploading algorithm docker to grand challenge server, please use the codes that I provided in test.sh

docker run --rm \
        --memory="${MEM_LIMIT}" \
        --memory-swap="${MEM_LIMIT}" \
        --network="none" \
        --cap-drop="ALL" \
        --security-opt="no-new-privileges" \
        --shm-size="128m" \
        --pids-limit="256" \
        -v $SCRIPTPATH/test/:/input/ \
        -v bondbidhie2023_algorithm-output-$VOLUME_SUFFIX:/output/ \
        bondbidhie2023_algorithm

(3) ./export.sh 
Running ./export.sh, and submit the generated zip file of the algorithm docker.
