#!/bin/bash
##  Initialize POSTGRESQL DB for webtelemetry Apps ##
#
#  Required: postgresql-root/admin account and password
#  Access to postgresql server
#  postgresql client
#
#  Envs: prod, dev, test, pilot
#    custom: enter name
#
#  Apps:
#    grafana - db: webtelemetry_db
#           user: grafana-<env>
#    grafana  - db:telemetrix_db
#            user: grafana-<env>
#    snmp - db: wt_db
#            user: snmp-<env>
#    telemetrix - db: telemetrix_db
#            user: telemetrix-<env>
#    fluxe - db: fluxe_db
#            user: fluxe-<env>
#    telegraf - db: telegraf_db
#            user: telegraf-<env>
#

[[ ${WT_SAVE_FILE} ]] || WT_SAVE_FILE=/WT/.postgresql.auth

# Defaults #
# -- grafana -- #
WEBTELEMETRY_DB_NAME=webtelemetry_db
WEBTELEMETRY_DB_USER=webtelemetry
WEBTELEMETRY_DB_PASS='webtelemetryPass'
WEBTELEMETRY_SQL_FILE=''
# -- grafana -- #
TELEMETRIX_DB_NAME=metrix_db
TELEMETRIX_DB_USER=grafana
TELEMETRIX_DB_PASS='dsoPass'
TELEMETRIX_SQL_FILE=''
# -- snmp -- #
TELEMETRIX_DB_NAME=wt_db
TELEMETRIX_DB_USER=snmp
TELEMETRIX_DB_PASS='metrixPass'
TELEMETRIX_SQL_FILE=''
# -- telemetrix -- #
TELEMETRIX_DB_NAME=telemetrix_db
TELEMETRIX_DB_USER=telemetrix
TELEMETRIX_DB_PASS='telemetrixPass'
TELEMETRIX_SQL_FILE=''
# -- fluxe -- #
FLUXE_DB_NAME=fluxe_db
FLUXE_DB_USER=fluxe
FLUXE_DB_PASS='fluxe18'
FLUXE_SQL_FILE=''
# -- telegraf -- #
TELEGRAF_DB_NAME=telegraf_db
TELEGRAF_DB_USER=telegraf
TELEGRAF_DB_PASS='telegraf76'
TELEGRAF_SQL_FILE=''

# -- BACKUP USER -- #
BACKUP_USER=backup-user
BACKUP_PASS="veuK6tOw9yei"

# -- ADMIN DEFAULTS -- #
POSTGRES_SERVER=127.0.0.1
POSTGRES_PORT=3306
POSTGRES_ADMIN_USER=root

# Random Password Generator #
randpw(){ env LC_CTYPE=C tr -dc "a-zA-Z0-9" < /dev/urandom | head -c12;echo;}

# validation
#  - check for postgresql client
check_postgresql(){
    if [[ ! $(which postgresql) ]]; then
        echo "Error: postgresql client not found!"
        exit 1
    fi
}

# Enter Admin inputs #
postgresql_admin_auth(){
    echo "Enter POSTGRESQL Admin info..."

    read -p "  postgresql server host [${POSTGRES_SERVER}]: " resp
    [[ $resp ]] && POSTGRES_SERVER=${resp}
    read -p "  postgresql server port [${POSTGRES_PORT}]: " resp
    [[ $resp ]] && POSTGRES_PORT=${resp}
    read -p "  postgresql admin user [${POSTGRES_ADMIN_USER}]: " resp
    [[ $resp ]] && POSTGRES_ADMIN_USER=${resp}

    while [[ -z $PASSWORD_IS ]]; do
        echo  -n "  postgresql admin password: "
        read -s resp
        [[ $resp ]] && PASSWORD_IS=${resp}
        echo
    done
    POSTGRES_ADMIN_PASS=${PASSWORD_IS}
    unset PASSWORD_IS
}

test_postgresqlclient(){
    echo -n "Checking Admin POSTGRESQL port: ${POSTGRES_PORT} ..."
    nc -zv ${POSTGRES_SERVER} ${POSTGRES_PORT} 2>/dev/null
    ncstatus=$?
    if [ ${ncstatus} -ne 0 ]; then
        echo "[failed]"
        echo "Verify POSTGRESQL server ${POSTGRES_SERVER} is available and settings."
        exit 1
    fi
    echo -n "Checking Admin POSTGRESQL connection..."
    postgresql --user="${POSTGRES_ADMIN_USER}" --password="${POSTGRES_ADMIN_PASS}" -h "${POSTGRES_SERVER}" --port=${POSTGRES_PORT} -e exit 2>/dev/null
    retstatus=`echo $?`
    if [ ${retstatus} -ne 0 ]; then
        echo "[failed]"
        echo "Verify POSTGRESQL server ${POSTGRES_SERVER} is available and settings."
        exit 1
    else
        echo "[passed]"
    fi
}

# Input Environment
choose_environment() {
    echo
    echo "  Valid environment prefixes: dev, test, pilot, demo, prod"
    echo "    examples:  dev01, test01, pilot01, prod01, demo01"
    echo
    PASSED="no"
    while [ $PASSED == "no" ]; do
        while [[ -z ${POSTGRES_ENV_NAME} ]]; do
            read -p " Enter postgresql env name: " POSTGRES_ENV_NAME
        done
        case ${POSTGRES_ENV_NAME} in
            dev[0-9][0-9]|test[0-9][0-9]|pilot[0-9][0-9]|demo[0-9][0-9]|prod[0-9][0-9])
                PASSED="yes"
                WEBTELEMETRY_DB_USER=${WEBTELEMETRY_DB_USER}-${POSTGRES_ENV_NAME}
                TELEMETRIX_DB_USER=${TELEMETRIX_DB_USER}-${POSTGRES_ENV_NAME}
                TELEMETRIX_DB_USER=${TELEMETRIX_DB_USER}-${POSTGRES_ENV_NAME}
                TELEMETRIX_DB_USER=${TELEMETRIX_DB_USER}-${POSTGRES_ENV_NAME}
                FLUXE_DB_USER=${FLUXE_DB_USER}-${POSTGRES_ENV_NAME}
                TELEGRAF_DB_USER=${TELEGRAF_DB_USER}-${POSTGRES_ENV_NAME}
                [[ ${POSTGRES_ENV_NAME} == prod* ]] && POSTGRES_PROD="yes"
                [[ ${POSTGRES_ENV_NAME} == test* ]] && POSTGRES_PROD="yes"
                ;;
            *)
                POSTGRES_ENV_NAME=""
                echo "Invalid name: $POSTGRES_ENV_NAME"
                echo "Environment name format is: "
                echo " ( dev## | test## | pilot## | prod## | demo## )"
                ;;
        esac
    done
}


# Select DB Apps to create #
choose_apps() {
    echo
    APPS_LIST="grafana grafana snmp telemetrix fluxe telegraf DONE"
    webtelemetry=''
    grafana=''
    snmp=''
    telemetrix=''
    fluxe=''
    telegraf=''

    while : ; do
        cat << EOF
  =============================================
  Select Database App to Create
  ---------------------------------------------
EOF
        printf "\n  (1) [%1s] grafana" "$webtelemetry"
        printf "\n  (2) [%1s] grafana" "$dso"
        printf "\n  (3) [%1s] snmp" "$grafana"
        printf "\n  (4) [%1s] telemetrix" "$telemetrix"
        printf "\n  (5) [%1s] fluxe" "$fluxe"
        printf "\n  (6) [%1s] telegraf" "$telegraf"
        printf "\n  (q) Done"
        printf "\n\n Enter Selection: "
        read opt

        case $opt in
            "1")    if [[ ${{{ product.smallname }}} ]]; then
                        webtelemetry=''
                    else
                        [[ ${POSTGRES_PROD} == "yes" ]] && WEBTELEMETRY_DB_PASS=$(randpw)
                        read -p "Enter a grafana user DB password [${WEBTELEMETRY_DB_PASS}]: " pass_w
                        [[ "${pass_w}" ]] && WEBTELEMETRY_DB_PASS=${pass_w}
                        unset pass_w
                        read -p "Enter SQL file to load [none]: " WEBTELEMETRY_SQL_FILE
                        webtelemetry='X'
                    fi
                    ;;
            "2")    if [[ ${grafana} ]]; then
                        grafana=''
                    else
                        [[ ${POSTGRES_PROD} == "yes" ]] && TELEMETRIX_DB_PASS=$(randpw)
                        read -p "Enter a TELEMETRIX user DB password [${TELEMETRIX_DB_PASS}]: " pass_w
                        [[ ${pass_w} ]] && TELEMETRIX_DB_PASS=${pass_w}
                        unset pass_w
                        read -p "Enter SQL file to load [none]: " TELEMETRIX_SQL_FILE
                        grafana='X'
                    fi
                    ;;
            "3")    if [[ ${snmp} ]]; then
                        snmp=''
                    else
                        [[ ${POSTGRES_PROD} == "yes" ]] && TELEMETRIX_DB_PASS=$(randpw)
                        read -p "Enter a TELEMETRIX user DB password [${TELEMETRIX_DB_PASS}]: " pass_w
                        [[ ${pass_w} ]] && TELEMETRIX_DB_PASS=${pass_w}
                        unset pass_w
                        read -p "Enter SQL file to load [none]: " TELEMETRIX_SQL_FILE
                        snmp='X'
                    fi
                    ;;
            "4")    if [[ ${telemetrix} ]]; then
                        telemetrix=''
                    else
                        [[ ${POSTGRES_PROD} == "yes" ]] && TELEMETRIX_DB_PASS=$(randpw)
                        read -p "Enter an TELEMETRIX user DB password [${TELEMETRIX_DB_PASS}]: " pass_w
                        [[ ${pass_w} ]] && TELEMETRIX_DB_PASS=${pass_w}
                        unset pass_w
                        read -p "Enter SQL file to load [none]: " TELEMETRIX_SQL_FILE
                        telemetrix='X'
                    fi
                    ;;
            "5")    if [[ ${fluxe} ]]; then
                        fluxe=''
                    else
                        [[ ${POSTGRES_PROD} == "yes" ]] && FLUXE_DB_PASS=$(randpw)
                        read -p "Enter the SEP20 user DB password [${FLUXE_DB_PASS}]: " pass_w
                        [[ ${pass_w} ]] && FLUXE_DB_PASS=${pass_w}
                        unset pass_w
                        read -p "Enter SQL file to load [none]: " FLUXE_SQL_FILE
                        fluxe='X'
                    fi
		    ;;
            "6")    if [[ ${telegraf} ]]; then
                        telegraf=''
                    else
                        [[ ${POSTGRES_PROD} == "yes" ]] && TELEGRAF_DB_PASS=$(randpw)
                        read -p "Enter the OADR20B user DB password [${TELEGRAF_DB_PASS}]: " pass_w
                        [[ ${pass_w} ]] && TELEGRAF_DB_PASS=${pass_w}
                        unset pass_w
                        read -p "Enter SQL file to load [none]: " TELEGRAF_SQL_FILE
                        telegraf='X'
                    fi
    		    ;;
            "q")    break
                    ;;
            *) echo "invalid option"
               ;;
        esac
    done
}


review_settings() {
    echo "Database Host:   ${POSTGRES_SERVER}"
    echo "WebTelemetry Environment:  ${POSTGRES_ENV_NAME}"
    echo "==================================================="
    if [[ ${{{ product.smallname }}} ]]; then
        echo "grafana --"
        echo "   db name:  ${WEBTELEMETRY_DB_NAME}"
        echo "   db user:  ${WEBTELEMETRY_DB_USER}"
        echo "   db pass:  ${WEBTELEMETRY_DB_PASS}"
        [[ ${WEBTELEMETRY_SQL_FILE} ]] && echo "  sql file:  ${WEBTELEMETRY_SQL_FILE}"
        echo
    fi
    if [[ ${grafana} ]]; then
        echo "TELEMETRIX --"
        echo "   db name:  ${TELEMETRIX_DB_NAME}"
        echo "   db user:  ${TELEMETRIX_DB_USER}"
        echo "   db pass:  ${TELEMETRIX_DB_PASS}"
        [[ ${TELEMETRIX_SQL_FILE} ]] && echo "  sql file:  ${TELEMETRIX_SQL_FILE}"
        echo
    fi
    if [[ ${snmp} ]]; then
        echo "TELEMETRIX --"
        echo "   db name:  ${TELEMETRIX_DB_NAME}"
        echo "   db user:  ${TELEMETRIX_DB_USER}"
        echo "   db pass:  ${TELEMETRIX_DB_PASS}"
        [[ ${TELEMETRIX_SQL_FILE} ]] && echo "  sql file:  ${TELEMETRIX_SQL_FILE}"
        echo
    fi
    if [[ ${telemetrix} ]]; then
        echo "TELEMETRIX --"
        echo "   db name:  ${TELEMETRIX_DB_NAME}"
        echo "   db user:  ${TELEMETRIX_DB_USER}"
        echo "   db pass:  ${TELEMETRIX_DB_PASS}"
        [[ ${TELEMETRIX_SQL_FILE} ]] && echo "  sql file:  ${TELEMETRIX_SQL_FILE}"
        echo
    fi
    if [[ ${fluxe} ]]; then
        echo "SEP20 --"
        echo "   db name:  ${FLUXE_DB_NAME}"
        echo "   db user:  ${FLUXE_DB_USER}"
        echo "   db pass:  ${FLUXE_DB_PASS}"
        [[ ${FLUXE_SQL_FILE} ]] && echo "  sql file:  ${FLUXE_SQL_FILE}"
        echo
    fi
    if [[ ${telegraf} ]]; then
        echo "OADR20B --"
        echo "   db name:  ${TELEGRAF_DB_NAME}"
        echo "   db user:  ${TELEGRAF_DB_USER}"
        echo "   db pass:  ${TELEGRAF_DB_PASS}"
        [[ ${TELEGRAF_SQL_FILE} ]] && echo "  sql file:  ${TELEGRAF_SQL_FILE}"
        echo
    fi
    read -p "Record details in LastPass and continue (y/n): " confirm
    [[ ${confirm} == 'y' ]] || exit 0
}


_create_db(){
    db_user=$1
    db_pass=$2
    db_name=$3
    db_file=$4

#    echo DEBUG: postgresql --user="${POSTGRES_ADMIN_USER}" --password="${POSTGRES_ADMIN_PASS}" -h "${POSTGRES_SERVER} --port=${POSTGRES_PORT}"
    postgresql --user="${POSTGRES_ADMIN_USER}" --password="${POSTGRES_ADMIN_PASS}" -h "${POSTGRES_SERVER}" --port=${POSTGRES_PORT} << EOF
CREATE DATABASE ${db_name};
GRANT ALL PRIVILEGES ON ${db_name}.* TO "${db_user}"@"%" IDENTIFIED BY "${db_pass}";
EOF
    if [[ ${db_file} ]]; then
        if [[ -f ${db_file} ]]; then
            echo "    processing SQL file ${db_file}"
            postgresql --user="${db_user}" --password="${db_pass}" -h "${POSTGRES_SERVER}" ${db_name} < ${db_file}
        fi
    fi
    echo "${POSTGRES_SERVER} : ${db_name}" >> $WT_SAVE_FILE
    echo "    user=${db_user}" >> $WT_SAVE_FILE
    echo "    pass=${db_pass}" >> $WT_SAVE_FILE
    chmod 600 $WT_SAVE_FILE
}


create_databases() {
    echo "Creating Databases and DB Users"
    if [[ ${{{ product.smallname }}} ]]; then
        echo "  grafana"
        _create_db ${WEBTELEMETRY_DB_USER} ${WEBTELEMETRY_DB_PASS} ${WEBTELEMETRY_DB_NAME} ${WEBTELEMETRY_SQL_FILE}
    fi
    if [[ ${grafana} ]]; then
        echo "  grafana"
        _create_db ${TELEMETRIX_DB_USER} ${TELEMETRIX_DB_PASS} ${TELEMETRIX_DB_NAME} ${TELEMETRIX_SQL_FILE}
    fi
    if [[ ${snmp} ]]; then
        echo "  snmp"
        _create_db ${TELEMETRIX_DB_USER} ${TELEMETRIX_DB_PASS} ${TELEMETRIX_DB_NAME} ${TELEMETRIX_SQL_FILE}
    fi
    if [[ ${telemetrix} ]]; then
        echo "  telemetrix"
        _create_db ${TELEMETRIX_DB_USER} ${TELEMETRIX_DB_PASS} ${TELEMETRIX_DB_NAME} ${TELEMETRIX_SQL_FILE}
    fi
    if [[ ${fluxe} ]]; then
        echo "  fluxe"
        _create_db ${FLUXE_DB_USER} ${FLUXE_DB_PASS} ${FLUXE_DB_NAME} ${FLUXE_SQL_FILE}
    fi
    if [[ ${telegraf} ]]; then
        echo "  telegraf"
        _create_db ${TELEGRAF_DB_USER} ${TELEGRAF_DB_PASS} ${TELEGRAF_DB_NAME} ${TELEGRAF_SQL_FILE}
    fi
}

create_backup_user() {
    echo "Creating POSTGRESQL backup user"
    postgresql --user="${POSTGRES_ADMIN_USER}" --password="${POSTGRES_ADMIN_PASS}" -h "${POSTGRES_SERVER}" --port=${POSTGRES_PORT} << EOF
GRANT SELECT, RELOAD, FILE, SUPER, LOCK TABLES, SHOW VIEW ON *.* TO "${BACKUP_USER}"@"%" IDENTIFIED BY "${BACKUP_PASS}";
flush privileges;
EOF
    echo "done"    
}


main() {
    check_postgresql
    postgresql_admin_auth
    test_postgresqlclient
    choose_environment
    choose_apps
    review_settings
    create_databases
    #create_backup_user
}

main

# clean up
unset POSTGRES_ADMIN_PASS
