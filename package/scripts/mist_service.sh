#!/bin/sh
### BEGIN INIT INFO
# Provides:          Mist
# Required-Start:    $local_fs $network $named $time $syslog
# Required-Stop:     $local_fs $network $named $time $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       Hydrosphere Mist
### END INIT INFO

NAME="mist"
SCRIPT="/usr/share/mist/bin/$NAME"
SCRIPT_AGRS=" start master"
RUNAS="root"

PIDFILE=/var/run/$NAME.pid
LOGFILE=/var/log/$NAME.log

export SPARK_HOME=/usr/hdp/current/spark-client

set -e

start() {
  if [ -f $PIDFILE ] && kill -0 $(cat $PIDFILE); then
    echo 'Service already running' >&2
    return 1
  fi
  echo 'Starting service...' >&2
  local CMD="$SCRIPT $SCRIPT_AGRS &>> \"$LOGFILE\" & echo \$!"
  su -c "$CMD" $RUNAS > "$PIDFILE"
  echo 'Service started' >&2
}

stop() {
  if [ ! -f "$PIDFILE" ] || ! kill -0 $(cat "$PIDFILE"); then
    echo 'Service not running' >&2
    return 1
  fi
  echo 'Stopping service...' >&2
  $SCRIPT stop && rm -f "$PIDFILE"
  echo 'Service stopped' >&2
}

case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
esac
