#! /bin/bash

DATE=`date "+%Y-%m-%d-%H-%M"`

SIMDIR="/simulator"
LOGDIR="/simulator/is"
LOGFORMAT="????-??-??-??-??-??.csv"
BACKUPDIR="/default-sim-log"
RUNSH="./default.sh"

# # check if killall hangs up
# ps -a | grep sim_autoexecutor.sh
# if [ $? = 0 ]
#   killall -SIGKILL sim_autoexecutor.sh
#   killall -SIGKILL java
#   echo "[sim_autoexecutor] ${DATE} ** java was killed"
# fi

# trying to terminate java process
ps aux | grep java | grep -v "grep"
if [ $? = 0 ]; then
  # send SIGTERM signal
  killall -SIGTERM --wait java
  ps aux | grep java | grep -v "grep"
  if [ $? = 0 ]; then
    # can not terminate java process
    echo "[sim_autoexecutor] ${DATE} !! can not terminating java"
    exit 1
  fi
fi

# verifying the existence of BACKUPDIR
if [ ! -d $BACKUPDIR ]; then
  mkdir -p ${BACKUPDIR}
fi

# trying to backup logfiles
FINDFILE=`find $LOGDIR -maxdepth 1 -name $LOGFORMAT`
if [ $? -ne 0 ]; then
  echo "[sim_autoexecutor] ${DATE} !! Error finding logfile."
elif [ -z "$FINDFILE" ]; then
  echo "[sim_autoexecutor] ${DATE} ** Logfile dir is empty."
else
  mv -f --backup=numbered ${LOGDIR}/* ${BACKUPDIR}/

  mv ${BACKUPDIR}/log4j2.xml ${SIMDIR}/is/log4j2.xml
  echo "[sim_autoexecutor] ${DATE} Backup complete."
fi

# run simulator
cd ${SIMDIR}
${RUNSH} > /dev/null &
exit 0