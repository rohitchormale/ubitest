#!/bin/bash

interpreter=`which python3`
lockfile=/tmp/fpcservice.lock
prgfile=fpcservice.py
prgpath=`realpath $0`
basedir=`dirname $(dirname $prgpath)`
cd $basedir


# make sure only one instance of program is running at given time
if ( set -o noclobber; echo "$$" > "$lockfile") 2> /dev/null; then
    trap 'rm -f "$lockfile"; exit $?' INT TERM EXIT
    # run job
    $interpreter $prgfile
else
    echo "Lock Exists: $lockfile owned by $(cat $lockfile)"
fi