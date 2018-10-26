#!/bin/bash

## Stop, Start, or restart the grafana stack ##

# check for root user - only root/sudo
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

WEBTELEMETRY_SERVICES="grafana-unicorn grafana-proxies grafana-resque-pool grafana-resque-scheduler grafana-work-subscribers grafana-topic-subscriber"

case $1 in
    stop)
        echo "Stopping Webtelemetry stack"
        for drom in $WEBTELEMETRY_SERVICES; do
            echo "..$drom.."
            service $drom stop
        done
        ;;
    start)
        echo "Starting Webtelemetry stack"
        for drom in $WEBTELEMETRY_SERVICES; do
            echo "..$drom.."
            service $drom start
        done
        ;;
    status)
        echo "Status Webtelemetry stack"
        for drom in $WEBTELEMETRY_SERVICES; do
            service $drom status
        done
        ;;
    restart)
        echo "Restartin Webtelemetry stack"
        for drom in $WEBTELEMETRY_SERVICES; do
            echo "..$drom.."
            service $drom restart
        done
        ;;
    
    *)
        echo "USAGE: $0 {stop|start|status|restart}"
        ;;
esac 
