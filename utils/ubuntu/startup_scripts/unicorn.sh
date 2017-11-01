#!/bin/bash
USAGE="$0 {start|stop|status|restart|pid}"
AS_USER=webtelemetry
WORKING_PATH=/WT/appserver
PID_FILE=$WORKING_PATH/tmp/pids/unicorn.pid
APP_ENV=production

COMMAND_NAME=unicorn
PATH=/WT/.rbenv/shims:$PATH
EXEC_FILE="/WT/.rbenv/shims/unicorn"
EXEC_ARGS="-c config/unicorn.conf.rb -E production -D"
EXEC_CMD="cd $WORKING_PATH && $EXEC_FILE $EXEC_ARGS"


get_pid(){
    PID_IS=""
    PID_STALE=""
    if [ -f $PID_FILE ]; then
        PID_IS=$(cat $PID_FILE)
    fi
    if [[ ! -z "$PID_IS" ]]; then
	# check if pid is live #
	if [ ! -d /proc/$PID_IS ]; then
	     PID_STALE=true
	fi
    fi
}

start_app(){
    case $USER in
	$AS_USER)
            echo "Starting $COMMAND_NAME"
	    eval $EXEC_CMD
	    ;;
	root|ubuntu)
	    sudo su -c "$EXEC_CMD" -l $AS_USER
	    ;;
        *) echo "Invalid user: $USER"
	   exit 2
	   ;;
    esac
}

stop_app(){
    if [[ ! -z "$PID_IS" ]]; then
	    if [[ ! -z "$PID_STALE" ]]; then
	        echo "cleanup stale pid file"
   	        case $USER in
	            $AS_USER)
	    	        /bin/rm $PID_FILE
		            ;;
		        root|ubuntu)
		            sudo /bin/rm $PID_FILE
		            ;;
		        *) echo "Invalid user: $USER"
		            exit 2
		            ;;
	        esac
	    else
	        echo "stoping: $COMMAND_NAME (pid:$PID_IS)"
	        case $USER in
		        $AS_USER)
			        kill $PID_IS
			        ;;
		        root|ubuntu)
			        sudo kill $PID_IS
			        ;;
		        *) echo "Invalid user: $USER"
		        exit 2
		            ;;
	        esac
	    fi
     else
	    echo "$COMMAND_NAME not running"
     fi
}

get_pid
case $1 in
    start)
        if [ -z $PID_IS ] || [[ $PID_STALE = "true" ]]; then
	    start_app
        else
	   echo "$COMMAND_NAME is already running: pid($PID_IS)"
	fi
	;;
    status)
	if [[ ! -z "$PID_IS" ]]; then
	     if [[ "$PID_STALE" ]]; then
		 echo "$COMMAND_NAME is stopped (stale pid found:$PID_IS)"
	     else
		 echo "$COMMAND_NAME is runing (pid:$PID_IS)"
	     fi
	else
	     echo "$COMMAND_NAME is stopped"
	fi
	;;
    stop)
        stop_app
        ;;

    restart)
         stop_app
         sleep 3
         start_app
         ;;
    pid)
         [[ "$PID_STALE" ]] && echo "$PID_IS(stale)" || echo $PID_IS
         ;;

    help|-h|--help|-?) echo "Usage: $USAGE"
	;;

    *) echo "Usage: $USAGE"
       exit 1
	;;
esac