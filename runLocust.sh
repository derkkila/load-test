#!/bin/bash
#
# Run locust load test
#
#####################################################################
ARGS="$@"
HOST="${1}"
SCRIPT_NAME=`basename "$0"`
INITIAL_DELAY=1
TARGET_HOST="$HOST"
CLIENTS=2
REQUESTS=10
THROTTLE="0"
LOOP_TIME=0


do_check() {

  # check hostname is not empty
  if [ "${TARGET_HOST}x" == "x" ]; then
    echo "TARGET_HOST is not set; use '-h hostname:port'"
    exit 1
  fi

  # check for locust
  if [ ! `command -v locust` ]; then
    echo "Python 'locust' package is not found!"
    exit 1
  fi

  # check locust file is present
  if [ -n "${LOCUST_FILE:+1}" ]; then
  	echo "Locust file: $LOCUST_FILE"
  else
  	LOCUST_FILE="locustfile.py"
  	echo "Default Locust file: $LOCUST_FILE"
  fi
}

do_exec() {
  sleep $INITIAL_DELAY

  # check if host is running
  #STATUS=$(curl -s -o /dev/null -w "%{http_code}" ${TARGET_HOST})
  #if [ $STATUS -ne 200 ]; then
  #    echo "${TARGET_HOST} is not accessible"
  #    exit 1
  #fi

  if [ $THROTTLE -ne "0" ]; then
    echo "Enabling request throttling based on script parameter"
    NEW_CLIENTS=`python -c "import os; os.chdir('/usr/local/bin'); import helpers.helpers as helpers; print helpers.getProbabilityCount($CLIENTS)"`
    NEW_REQUESTS=`python -c "import os; os.chdir('/usr/local/bin'); import helpers.helpers as helpers; print helpers.getProbabilityCount($REQUESTS)"`
  else
    NEW_CLIENTS=$CLIENTS
    NEW_REQUESTS=$REQUESTS
  fi


  if [ $LOOP_TIME -gt 0 ]; then
    echo "Will run $LOCUST_FILE against $TARGET_HOST. Spawning $NEW_CLIENTS clients and $NEW_REQUESTS total requests. Execution will loop for $LOOP_TIME minutes."

    START=`date +%s`
    TOTAL_LOOP_SEC=$((60*$LOOP_TIME))
    while [ $(( $(date +%s) - $TOTAL_LOOP_SEC)) -lt $START ]; do
        locust --host=http://$TARGET_HOST -f $LOCUST_FILE --clients=$NEW_CLIENTS --hatch-rate=25 --num-request=$NEW_REQUESTS --no-web --only-summary

        if [ $THROTTLE -ne "0" ]; then
          NEW_CLIENTS=`python -c "import os; os.chdir('/usr/local/bin'); import helpers.helpers as helpers; print helpers.getProbabilityCount($CLIENTS)"`
          NEW_REQUESTS=`python -c "import os; os.chdir('/usr/local/bin'); import helpers.helpers as helpers; print helpers.getProbabilityCount($REQUESTS)"`
        fi
    done

  else
    echo "Will run $LOCUST_FILE against $TARGET_HOST. Spawning $NEW_CLIENTS clients and $NEW_REQUESTS total requests."
    locust --host=http://$TARGET_HOST -f $LOCUST_FILE --clients=$NEW_CLIENTS --hatch-rate=25 --num-request=$NEW_REQUESTS --no-web --only-summary
  fi
  echo "done"
}

do_usage() {
    cat >&2 <<EOF
Usage:
  ${SCRIPT_NAME} [ hostname ] OPTIONS

Options:
  -d  Delay before starting
  -h  Target host url, e.g. http://localhost/
  -c  Number of clients (default 2)
  -r  Number of requests (default 10)
  -l  Number of minutes to run the load tests in a loop before terminating (default no loop)
  -t  If present, day/time throttling will be applied to throttle loads to simulate human traffic

Description:
  Runs a Locust load simulation against specified host.

EOF
  exit 1
}



while getopts ":d:h:c:r:l:t" o; do
  case "${o}" in
    d)
        INITIAL_DELAY=${OPTARG}
        #echo $INITIAL_DELAY
        ;;
    h)
        TARGET_HOST=${OPTARG}
        #echo $TARGET_HOST
        ;;
    c)
        CLIENTS=${OPTARG:-2}
        #echo $CLIENTS
        ;;
    r)
        REQUESTS=${OPTARG:-10}
        #echo $REQUESTS
        ;;
    l)
        LOOP_TIME=${OPTARG}
        #echo $LOOP_TIME
        ;;
    t)
        THROTTLE="1"
        ;;
    *)
        do_usage
        ;;
  esac
done


do_check
do_exec
