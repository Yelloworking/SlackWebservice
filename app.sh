#!/bin/sh

NAME="slackbot"
PID="/tmp/slackbot.pid"
BASE_CMD="uwsgi --ini slackbot.ini"

start()
{
    echo "Starting $NAME."
    echo $BASE_CMD
    $BASE_CMD && echo "OK" || echo "failed";
}

stop()
{
    echo "Stopping $NAME"
    kill -QUIT `cat $PID` && echo "OK" || echo "failed";
}

reload()
{
    echo "Reloading $NAME:"
    if [ -f $PID ]
    then kill -HUP `cat $PID` && echo "OK" || echo "failed";
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        reload
        ;;
    reload)
        reload
        ;;
    force-reload)
        stop && start
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart}"
        RETVAL=1
esac
exit $RETVAL
