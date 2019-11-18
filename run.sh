#!/bin/bash

./clear_db.sh
echo 'DATABASE COLLECTION HAS BEEN CLEARED'
python3 parse.py &
PID=$$
echo 'PARSING HAS BEEN STARTED IN BACKGROUND MODE WITH PID: '$PID
echo 'YOU CAN SEE PARSING LOGS BY COMMAND:'
echo '-------------------'
echo '# tail -f parse.log'
echo '-------------------'
./server.py
