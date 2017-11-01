#!/bin/bash
AWSAPP=$1
ENVNAME=$2

CONF_FILE=aws-webtelemetrysyscom.yml

WEBTELEMETRY_TYPE=c3.xlarge
WEBTELEMETRY_PROFILE=prod01_fronthaul
WEBTELEMETRY_EBS=30GB_opt

HBASE_MASTER_TYPE=c3.2xlarge
HBASE_MASTER_PROFILE=prod01_backhaul
HBASE_MASTER_EBS=60GB_hbase_master

HBASE_WORKER_TYPE=c3.2xlarge
HBASE_WORKER_PROFILE=prod01_backhaul
HBASE_WORKER_EBS=100GB_hbase_worker

SEP_TYPE=m3.medium
SEP_PROFILE=prod01_fronthaul

OADR2_TYPE=m3.medium
OADR2_PROFILE=prod01_fronthaul

SFTP_TYPE=m3.medium
SFTP_PROFILE=prod01_fronthaul
SFTP_EBS=30GB_opt


Usage="launch-prod.sh [grafana | grafana | hbase-master | hbase-worker | fluxe | telegraf | sftp ] <env name> \n
    grafana type: $WEBTELEMETRY_TYPE \n
    Hbase-master type: $HBASE_MASTER_TYPE \n
    Hbase-worker type: $HBASE_WORKER_TYPE \n
    fluxe  type: $SEP_TYPE \n
    telegraf  type: $OADR2_TYPE \n
    sftp   type: $SFTP_TYPE \n\n
  valid env names: \n
     prod* \n\n
  Override flag(s): \n
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
        hbase-master)  [ -z $TYPE ] && TYPE=$HBASE_MASTER_TYPE
                PROFILE=$HBASE_MASTER_PROFILE
                EBS=$HBASE_MASTER_EBS
                PRENAME=hbase-master
                ;;
        hbase-worker)  [ -z $TYPE ] && TYPE=$HBASE_WORKER_TYPE
                PROFILE=$HBASE_WORKER_PROFILE
                EBS=$HBASE_WORKER_EBS
                PRENAME=hbase-worker
                ;;
        fluxe)  [ -z $TYPE ] && TYPE=$SEP_TYPE
                PROFILE=$SEP_PROFILE
                EBS=''
                PRENAME=SEP2
                ;;
        telegraf)  [ -z $TYPE ] && TYPE=$OADR2_TYPE
                PROFILE=$OADR2_PROFILE
                EBS=''
                PRENAME=Metrix
                ;;
        sftp)  [ -z $TYPE ] && TYPE=$SFTP_TYPE
                PROFILE=$SFTP_PROFILE
                EBS=''
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
        prod*)  EC2_NAME=${PRENAME}.$ENVNAME
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