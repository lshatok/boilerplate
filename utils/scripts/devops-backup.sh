#!/bin/bash

## Backup databases and apps for:
#   TELEMETRIX, WT Basalt, Revenue Assurance, and SignUp app ##
#    (WT Basalt = telemetrix and snmp)
#
# - rotate logsfile if over 20mb
# - remove any archives older than 1 year
# - postgresql dump to local
# -  

# Retain versions in days
LOCAL_RETAIN=2
S3_RETAIN=14
LOGFILE=/home/ubuntu/log/devops_backups.log

TIMESTAMP=$(date +%F_%H%M)
S3_BUCKET=com.webtelemetry-dev.dtech

## Database Info ##
POSTGRES_RR_HOST=dtech2014-main-rr1.seksejwlaqos.us-west-2.rds.amazonaws.com

TELEMETRIX_DB="metrix_db"
TELEMETRIX_BACKUP_PATH=/mnt/backup/grafana
TELEMETRIX_S3_PATH=backups/grafana

TELEMETRIX_DB="telemetrix_db"
TELEMETRIX_BACKUP_PATH=/mnt/backup/telemetrix
TELEMETRIX_S3_PATH=backups/telemetrix

TELEMETRIX_DB="wt_db"
TELEMETRIX_BACKUP_PATH=/mnt/backup/snmp
TELEMETRIX_S3_PATH=backups/snmp

REVASSURE_DB="revassure_db"
REVASSURE_BACKUP_PATH=/mnt/backup/revassure
REVASSURE_S3_PATH=backups/revassure

SIGNUP_DB="signup_db"
SIGNUP_BACKUP_PATH=/mnt/backup/signup
SIGNUP_S3_PATH=backups/signup
####################

export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games'

logger() {
    message="$1"
    echo "[$(date +%F_%H%M)] ${message}" | tee -a $LOGFILE
}

# rotate logfile if larger than 20MB
rotate_logs()
{ 
    if [ -f ${LOGFILE} ] && [[ "$(find ${LOGFILE} -size +20000k)" ]]; then
        logger "logfile over 20MB, rotating logfile."
        gzip -q --suffix .$(date +%F).gz ${LOGFILE} && echo "[done]"
        logger "New Logfile Created.. previous logfile rotated"
    fi
    # remove any archives over 1 year #
    #if [[ "$(find ${LOGFILE}.*.gz -mtime +365)" ]]; then
    #    logger "rotating archives (older than 1 year"
    #    find ${LOGFILE}.*.gz -mtime +365 | xargs rm -f >> ${LOGFILE}
    #    logger "done"
    #fi 
}

do_postgresql_backup()
{
    ## ARGS:  
    DB_NAME=$1
    BACKUP_PATH=$2
    S3_PATH=$3
    logger "starting postgresqldump for $DB_NAME"
    postgresqldump -h ${POSTGRES_RR_HOST} ${DB_NAME} | gzip > ${BACKUP_PATH}/${DB_NAME}_${TIMESTAMP}.sql.gz 2>&1 | tee -a $LOGFILE
    logger "postgresqldump for $DB_NAME done."

    logger "copying to s3.."
    s3cmd put "${BACKUP_PATH}/${DB_NAME}_${TIMESTAMP}.sql.gz" "s3://${S3_BUCKET}/${S3_PATH}/" 2>&1 | tee -a $LOGFILE
    RETVAL=$?
    if [ $RETVAL == 0 ]; then
        # local clean up #
        find ${BACKUP_PATH} -name "${DB_NAME}.*.sql.gz" -type f -mtime +${LOCAL_RETAIN} | xargs rm -f 2>&1 | tee -a $LOGFILE
    else
        logger "s3cmd for $DB_NAME to s3://${S3_BUCKET}/${S3_PATH}/ had an error"
        email_ops error devops@wildrivertechnologies.com "s3cmd for $DB_NAME to s3://${S3_BUCKET}/${S3_PATH}/ had an error"
    fi
}

email_ops()
{
    # Usage email_ops (info|error) email@addr "Message "
    MSG_TYPE=$1
    FROM_ADDR=devops@wildrivertechnologies.com
    TO_LIST=$2
    EMAIL_MSG="$3"
   
    case $MSG_TYPE in
        info)
            EMAIL_SUB="[DTech-TELEMETRIX Backup] - info $(date +%x)"
            ;;
        error)
            EMAIL_SUB="[DTech-TELEMETRIX Backup] - error $(date +%x)"
            ;;
        *)
            EMAIL_SUB="[DTech-TELEMETRIX] - $(date +%x)"
            ;;
    esac
    logger "sending mail to $TO_LIST"
    echo "${EMAIL_MSG}" | mail -s "${EMAIL_SUB}" -aFrom:${FROM_ADDR} ${TO_LIST}
}

backup_app_dir()
{
    APP_BU=$1
    logger "starting backup_app_dir for $APP_BU"
    case $APP_BU in
        grafana)
            WT_APP_PATH=/WT
            LOCAL_BACKUP_PATH=$TELEMETRIX_BACKUP_PATH
            TAR_BACKUP=$LOCAL_BACKUP_PATH/WT_APP_${TIMESTAMP}.tar.gz
            ;;
        revassure)
            WT_APP_PATH=rev-assure-demo
            LOCAL_BACKUP_PATH=$REVASSURE_BACKUP_PATH
            TAR_BACKUP=$LOCAL_BACKUP_PATH/revassure_APP_${TIMESTAMP}.tar.gz
            ;;
        *)
            echo "fatal error: backup_app_dir unknown arg: $1"
            exit 2
            ;;
    esac
    sudo tar zcf ${TAR_BACKUP} --exclude log --exclude tmp -C /WT $WT_APP_PATH 2>&1 | tee -a $LOGFILE
    #echo "DEBUG: sudo tar zcf ${TAR_BACKUP} --exclude log --exclude tmp -C /WT $WT_APP_PATH 2>&1 | tee -a $LOGFILE"
    if [ $? -gt 0 ]; then
        logger "error: tar command returned an error."
        email_ops error devops@wildrivertechnologies.com "error: tar command returned an error."
    else
        sudo chown ubuntu:ubuntu ${TAR_BACKUP}
        #echo "DEBUG: sudo chown ubuntu:ubuntu ${TAR_BACKUP}"
        s3cmd put ${TAR_BACKUP} "s3://${S3_BUCKET}/${S3_PATH}/" 2>&1 | tee -a $LOGFILE
        #echo "DEBUG: s3cmd put ${TAR_BACKUP} \"s3://${S3_BUCKET}/${S3_PATH}/\" 2>&1 | tee -a $LOGFILE"
        RETV=$?
        if [ $RETV -gt 0 ]; then
            logger "error s3cmd failed for put ${TAR_BACKUP} s3://${S3_BUCKET}/${S3_PATH}/"
            email_ops error devops@wildrivertechnologies.com "error s3cmd failed for put ${TAR_BACKUP} s3://${S3_BUCKET}/${S3_PATH}/"
        else 
            # local clean up #
            logger "cleaning up files older than ${LOCAL_RETAIN} days"
            find ${LOCAL_BACKUP_PATH} -name "*.tar.gz" -type f -mtime +${LOCAL_RETAIN} | xargs rm -f 2>&1 | tee -a $LOGFILE
        fi
    fi
}


## main ##
main()
{
    for DO_DB in $*; do
        rotate_logs
        case "$DO_DB" in
            "grafana")
                # Backup TELEMETRIX
                do_postgresql_backup $TELEMETRIX_DB $TELEMETRIX_BACKUP_PATH $TELEMETRIX_S3_PATH
                backup_app_dir grafana
                ;;
            "telemetrix")
                # Backup Analytics
                do_postgresql_backup $TELEMETRIX_DB $TELEMETRIX_BACKUP_PATH $TELEMETRIX_S3_PATH
                ;;
            "snmp")
                # Backup Grafana
                do_postgresql_backup $TELEMETRIX_DB $TELEMETRIX_BACKUP_PATH $TELEMETRIX_S3_PATH
                ;;
            "revassure")
                # Backup Revenue Assurance
                do_postgresql_backup $REVASSURE_DB $REVASSURE_BACKUP_PATH $REVASSURE_S3_PATH
                backup_app_dir revassure
                ;;
            "signup")
                # Backup Signup App
                do_postgresql_backup $SIGNUP_DB $SIGNUP_BACKUP_PATH $SIGNUP_S3_PATH
                ;;
            "all")
                # Backup all
                do_postgresql_backup $TELEMETRIX_DB $TELEMETRIX_BACKUP_PATH $TELEMETRIX_S3_PATH
                backup_app_dir grafana
                do_postgresql_backup $TELEMETRIX_DB $TELEMETRIX_BACKUP_PATH $TELEMETRIX_S3_PATH
                do_postgresql_backup $TELEMETRIX_DB $TELEMETRIX_BACKUP_PATH $TELEMETRIX_S3_PATH
                do_postgresql_backup $REVASSURE_DB $REVASSURE_BACKUP_PATH $REVASSURE_S3_PATH
                backup_app_dir revassure
                do_postgresql_backup $SIGNUP_DB $SIGNUP_BACKUP_PATH $SIGNUP_S3_PATH
                email_ops info eric@wildrivertechnologies.com "backup all completed"
                ;; 
            *)
                logger "error - unknown arg $DO_DB"
                echo "Usage : $0 {all | grafana | telemetrix | snmp | revassure | signup}"
                exit 2
                ;;
        esac 
    done
    logger "============= END $0 ===============" 
}

if [ $# -lt 1 ]; then
    echo "Usage : $0 {all | grafana | telemetrix | snmp | revassure | signup | help}"
    exit 1
fi
case $1 in
    "help"|"-h"|"?"|"--help")
        echo "Usage : $0 {all | grafana | telemetrix | snmp | revassure | signup}"
        exit
        ;;
    snmp|revassure|grafana|signup|telemetrix|all)
        logger "====  Starting $0 ======================="
        ;;
    *)
        echo  "ERROR - unknown arg $1"
        echo "Usage : $0 {all | grafana | telemetrix | snmp | revassure | signup}"
        exit 1
        ;;
esac
main $*
