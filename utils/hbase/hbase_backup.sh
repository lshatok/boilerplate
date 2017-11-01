#!/bin/bash
##########################################
#  hbase Backup to S3 Script
#   Exports Hbase data to HDFS then to S3
#
#   Usage: hbase_backup.sh $HBASE_TABLE_NAME
#
#  Requirements:
#     s3cmd - used to managed the S3 bucket
#
#  __author__ = Larry Sellars
#  __copyright__ = Copyright 2017, WebTelemetry US
#  __version__ = "0.7.6"
#  __email__ = larry.sellars@webtelemetry.us
#
##########################################

ConfigFile=~/.hbase_backup.conf
# AWS_KEY_ID=
# AWS_KEY_SECRET=
# HDFS_BACKUP_DIR=/tmp/backup
# HADOOP_NAMESERVER=<name_server>:port
# S3Bucket=

# -- steps
# Clean up any staged exports and logs (if any exists)
# Export Hbase to HDFS
# Get list of
# Distcp Export to HDFS
# Rotate local copy
# Export HDFS export & log to local copy
# Remove prev S3 bucket and prev local copy
# Clean up staged exports and logs


export JAVA_HOME=/usr/lib/jvm/j2sdk1.6-oracle

if [ $1 ]; then
    NOWDATE=$1
else
    NOWDATE=`date +%Y-%m-%d`
fi

WEEKAGO=$(date +%Y-%m-%d -d '7 days ago')

PARENT_DIR=/vol02/HBASE_BACKUP_FOR_S3
BACKUP_DIR=${PARENT_DIR}/backup/${NOWDATE}
#BACKUP_FILE=OGE_PROD_HBASE_${NOWDATE}.tgz
#BACKUP_FILE_7DAYS_AGO=OGE_PROD_HBASE_$(date +%Y-%m-%d -d '7 days ago').tgz

GZIP_STREAMS=3
S3PUT_STREAMS=3

#HBASE_METER_TABLE_NAME=test 
HBASE_METER_TABLE_NAME=meter_data_oge_prod
HBASE_WEATHER_TABLE_NAME=snmp_data_oge_prod

ErrorCount=0


function Delete_Old_Data
{
    ## Fix to delete processed files ##
    
    # Delete the old data files from HDFS and local dir
    echo "Deleting HDFS meter data file /tmp/backup/${HBASE_METER_TABLE_NAME}..."  
    sudo -H -u hdfs bash -c "hadoop fs rm -r /tmp/backup/${HBASE_METER_TABLE_NAME}"

    echo "Deleting HDFS weather data file /tmp/backup/${HBASE_WEATHER_TABLE_NAME}..."  
    sudo -H -u hdfs bash -c "hadoop fs rm -r /tmp/backup/${HBASE_WEATHER_TABLE_NAME}"

    # ?? - we will clean up the s3done path
    #echo "Deleting local meter/weather data file /vol01/HBASE_BACKUP_FOR_S3/..."
    #sudo rm -rf ${PARENT_DIR}/backup
}

function Create_Data_Folder
{ 
    echo "Create  meter/weather data  folder in ${BACKUP_DIR}..."
    mkdir -p ${BACKUP_DIR}/${HBASE_METER_TABLE_NAME}
    mkdir -p ${BACKUP_DIR}/${HBASE_WEATHER_TABLE_NAME}
    chmod 755 ${BACKUP_DIR}/${HBASE_METER_TABLE_NAME}
    chmod 755 ${BACKUP_DIR}/${HBASE_WEATHER_TABLE_NAME}
}

function Export_Hbase_to_HDFS
{
    # Export from HBase to HDFS
    echo "Exporting HBase meter data table ${HBASE_METER_TABLE_NAME} to HDFS /tmp/backup/${HBASE_METER_TABLE_NAME}..."
    sudo -H -u hdfs bash -c "hbase org.apache.hadoop.hbase.mapreduce.Export -Dhbase.client.scanner.caching=100000 -D mapred.output.compress=true -D mapred.output.compression.codec=org.apache.hadoop.io.compress.SnappyCodec ${HBASE_METER_TABLE_NAME} /tmp/backup/${HBASE_METER_TABLE_NAME}"

    echo "Exporting HBase weather data table ${HBASE_WEATHER_TABLE_NAME} to HDFS /tmp/backup/${HBASE_WEATHER_TABLE_NAME}..."
    sudo -H -u hdfs bash -c "hbase org.apache.hadoop.hbase.mapreduce.Export -Dhbase.client.scanner.caching=100000 -D mapred.output.compress=true -D mapred.output.compression.codec=org.apache.hadoop.io.compress.SnappyCodec ${HBASE_WEATHER_TABLE_NAME} /tmp/backup/${HBASE_WEATHER_TABLE_NAME}"
}

function Copy_HDFS_to_local
{
    # Copy from HDFS to local dir
    echo "Copying from HDFS to local HBASE_BACKUP_FOR_S3 folder..."
    sudo -H -u hdfs bash -c "hadoop fs -copyToLocal /tmp/backup/ ${PARENT_DIR}"
}

function Get_File_list
{
    METER_FILES_TO_BACKUP="$(cd $BACKUP_DIR/${HBASE_METER_TABLE_NAME} && find . -maxdepth 1 -type f -print | sort)"
    NUMBER_OF_METER_FILES=$(cd $BACKUP_DIR/${HBASE_METER_TABLE_NAME} && find . -maxdepth 1 -type f -print | wc -l)
    WEATHER_FILES_TO_BACKUP="$(cd $BACKUP_DIR/${HBASE_WEATHER_TABLE_NAME} && find . -maxdepth 1 -type f -print)"
    NUMBER_OF_WEATHER_FILES=$(cd $BACKUP_DIR/${HBASE_WEATHER_TABLE_NAME} && find . -maxdepth 1 -type f -print | wc -l)
}

 function Backup_METER_File_to_S3
{
    SendFile=$(basename $1).gz
    BACKUP_METER_DIR=$BACKUP_DIR/${HBASE_METER_TABLE_NAME}
    cd $BACKUP_METER_DIR
    [ -d sent ] || mkdir sent
    [ ! -f $SendFile ] && echo "$(date '+%b-%d-%Y %T') [ERROR] *** File: $SendFile Not Found in $BACKUP_METER_DIR ***" && return
    echo "$(date '+%b-%d-%Y %T') Sending file $SendFile to S3..."
    s3cmd put "${SendFile}" "s3://net.webtelemetry().ssn.oge.backup/${NOWDATE}/${HBASE_METER_TABLE_NAME}/"
    EXIT_STATUS=$?
    if [ $EXIT_STATUS == 0 ]; then
        echo "$(date '+%b-%d-%Y %T') Success.. moving $SendFile to sent directory."
        mv $SendFile sent/
    else
        echo "$(date '+%b-%d-%Y %T') [ERROR] S3cmd put failed for $SendFile"
    fi
}


function Backup_WEATHER_File_to_S3
{
    SendFile=$(basename $1).gz
    BACKUP_WEATHER_DIR=$BACKUP_DIR/${HBASE_WEATHER_TABLE_NAME}
    cd $BACKUP_WEATHER_DIR
    [ -d sent ] || mkdir sent
    [ ! -f $SendFile ] && echo "$(date '+%b-%d-%Y %T') [ERROR] *** File: $SendFile Not Found in $BACKUP_WEATHER_DIR ***" && return
    echo "$(date '+%b-%d-%Y %T') Sending file $SendFile to S3..."
    s3cmd put "${SendFile}" "s3://net.webtelemetry().ssn.oge.backup/${NOWDATE}/${HBASE_WEATHER_TABLE_NAME}/"
    EXIT_STATUS=$?
    if [ $EXIT_STATUS == 0 ]; then
        echo "$(date '+%b-%d-%Y %T') Success.. moving $SendFile to sent directory."
        mv $SendFile sent/
    else
        echo "$(date '+%b-%d-%Y %T') [ERROR] S3cmd put failed for $SendFile"
    fi
}


function Compress_Meter_Files
{
    ## Process Meter Files ##
    cd $BACKUP_DIR/${HBASE_METER_TABLE_NAME}
    echo "METER_TABLE files to process: $NUMBER_OF_METER_FILES"
    # Create md5sums and gzip #
    echo "$(date '+%b-%d-%Y %T') Creating md5sums.list and gzipping files..."
    for x in $METER_FILES_TO_BACKUP; do
        echo "$(date '+%b-%d-%Y %T') file: $x"
        md5sum $x >> md5sums.list
        ## Restrict the number of concurrent threads ##
        CURR_STREAMS=$(jobs | wc -l)
        while (( CURR_STREAMS >= GZIP_STREAMS )); do
            # wait a bit and check again
            sleep 5
            CURR_STREAMS=$(jobs | wc -l)
        done
        nice -n 19 gzip $x &
    done
    echo "$(date '+%b-%d-%Y %T') md5sums and gzips (done)."
}


function Compress_Weather_Files
{
    ## Process Weather Files ##
    cd $BACKUP_DIR/${HBASE_WEATHER_TABLE_NAME}
    echo "WEATHER_TABLE files to process: $NUMBER_OF_WEATHER_FILES"
    # Create md5sums and gzip #
    echo "$(date '+%b-%d-%Y %T') Creating md5sums.list and gzipping files..."
    for x in $WEATHER_FILES_TO_BACKUP; do
        echo "$(date '+%b-%d-%Y %T') file: $x"
        md5sum $x >> md5sums.list
        ## Restrict the number of concurrent threads ##
        CURR_STREAMS=$(jobs | wc -l)
        while (( CURR_STREAMS >= GZIP_STREAMS )); do
            # wait a bit and check again
            sleep 5
            CURR_STREAMS=$(jobs | wc -l)
        done
        nice -n 19 gzip $x &
    done
    echo "$(date '+%b-%d-%Y %T') md5sums and gzips (done)."
}


function Send_md5list
{
    BACKUP_METER_DIR=$BACKUP_DIR/${HBASE_METER_TABLE_NAME}
    BACKUP_WEATHER_DIR=$BACKUP_DIR/${HBASE_WEATHER_TABLE_NAME}  
    
    SendFile=md5sums.list
    cd $BACKUP_METER_DIR
    echo "$(date '+%b-%d-%Y %T') Sending meter md5sums.list to S3..."
    s3cmd put "$SendFile" "s3://net.webtelemetry().ssn.oge.backup/${NOWDATE}/${HBASE_METER_TABLE_NAME}/"
    EXIT_STATUS=$?
    if [ $EXIT_STATUS == 0 ]; then
        echo "$(date '+%b-%d-%Y %T') Success.. moving Meter $SendFile to sent directory."
        mv $SendFile sent/
    else
        echo "$(date '+%b-%d-%Y %T') [ERROR] S3cmd put failed for $SendFile."
    fi    

    cd $BACKUP_WEATHER_DIR
    echo "$(date '+%b-%d-%Y %T') Sending weather md5sums.list to S3..."
    s3cmd put "${SendFile}" "s3://net.webtelemetry().ssn.oge.backup/${NOWDATE}/${HBASE_WEATHER_TABLE_NAME}/"
    EXIT_STATUS=$?
    if [ $EXIT_STATUS == 0 ]; then
        echo "$(date '+%b-%d-%Y %T') Success.. moving Weather $SendFile to sent directory."
        mv $SendFile sent/
    else
        echo "$(date '+%b-%d-%Y %T') [ERROR] S3cmd put failed for $SendFile"
    fi
}


## Main ##
#Delete_Old_Data
#Create_Data_Folder
#Export_Hbase_to_HDFS
#Copy_HDFS_to_local

Get_File_list
Compress_Meter_Files
Compress_Weather_Files

for x in $METER_FILES_TO_BACKUP; do
    ## Restrict the number of concurrent threads ##
    CURR_STREAMS=$(jobs | wc -l)
    while (( CURR_STREAMS >= S3PUT_STREAMS )); do
        # wait a bit and check again
        sleep 5
        CURR_STREAMS=$(jobs | wc -l)
    done
    Backup_METER_File_to_S3 $x &
done        

for x in $WEATHER_FILES_TO_BACKUP; do
    ## Restrict the number of concurrent threads ##
    CURR_STREAMS=$(jobs | wc -l)
    while (( CURR_STREAMS >= S3PUT_STREAMS )); do
        # wait a bit and check again
        sleep 5
        CURR_STREAMS=$(jobs | wc -l)
    done
    Backup_WEATHER_File_to_S3 $x &
done        

Send_md5list

## Todo: CleanUp if ErrorCount == 0


