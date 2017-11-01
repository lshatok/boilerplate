#!/bin/bash

Usage="deploy-ops.sh [webtelemetry | hbase | ai | sftp] <env name> \n
    grafana type: m1.medium \n
    Hbase type: m1.large \n
    ai type: t1.micro \n
    SFTP type: m1.medium \n\n
  valid env names:  dev*, test* \n\n
  Override flag: \n
    -t <instance type> \n "

while getopts "t:" opt; do
    case ${opt} in
        t) TYPE="$OPTARG"
            ;;
        *) echo -e $Usage
           exit 1
            ;;
    esac
done
shift $(( OPTIND -1 ))

AWSAPP=$1
ENVNAME=$2

CONF_FILE=aws-devops-west.yml

WEBTELEMETRY_TYPE=m1.medium
WEBTELEMETRY_PROFILE=dev_fronthaul
WEBTELEMETRY_EBS=18GB

HBASE_TYPE=m1.large
HBASE_PROFILE=dev_backhaul
HBASE_EBS=30GB_hbase

DEVOPS_TYPE=t1.micro
DEVOPS_PROFILE=devops_sandbox

SFTP_TYPE=m1.medium
SFTP_PROFILE=dev_fronthaul
SFTP_EBS=18GB


verify-iam() {
    if [ -z $AWS_ACCESS_KEY_ID ]; then
        echo "Error: AWS_ACCESS_KEY_ID needs to be set"
        ERR=Yes
    fi
    if [ -z $AWS_SECRET_ACCESS_KEY ]; then
        echo "Error: AWS_SECRET_ACCESS_KEY needs to be set"
        ERR=Yes
    fi
    [[ $ERR == "Yes" ]] && exit 1
}

verify-opts() {
    if [ -z $AWSAPP ] || [ -z $ENVNAME ]; then
        echo "Error: missing args"
        echo -e $Usage
        exit 1
    fi
    case $AWSAPP in
        webtelemetry)  [ -z $TYPE ] && TYPE=$WEBTELEMETRY_TYPE
                PROFILE=$WEBTELEMETRY_PROFILE
                EBS=$WEBTELEMETRY_EBS
                PRENAME=grafana
                ;;
        hbase)  [ -z $TYPE ] && TYPE=$HBASE_TYPE
                PROFILE=$HBASE_PROFILE
                EBS=$HBASE_EBS
                PRENAME=hbase
                ;;
        devops)  [ -z $TYPE ] && TYPE=$DEVOPS_TYPE
                PROFILE=$DEVOPS_PROFILE
                EBS=''
                PRENAME=devops
                ;;
        sftp)  [ -z $TYPE ] && TYPE=$SFTP_TYPE
                PROFILE=$SFTP_PROFILE
                EBS=$SFTP_EBS
                PRENAME=SFTP
                ;;
        -h|help|--help|-?)  echo -e $Usage
                ;;
        *) echo "Error: unknown option $AWSAPP"
           echo -e $Usage
           exit 1
           ;;
    esac
    case $ENVNAME in
        dev*|test*|qa*)  EC2_NAME=${PRENAME}.$ENVNAME
                ;;
        *)  echo "Error: invalid env name $ENVNAME"
            echo $Usage
            exit 1
            ;;
    esac
}

launch_instance() {
    [ -z $EBS ] && _aws_EBS='' || _aws_EBS="--ebs $EBS"
    ../../AwsLaunch/AwsLaunch.py --file $CONF_FILE --type $TYPE --profile $PROFILE --name $EC2_NAME $_aws_EBS

}

main() {
    verify-iam
    verify-opts
    launch_instance
}

main