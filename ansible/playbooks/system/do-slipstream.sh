#!/bin/bash
#

prog=$(basename $0)
dirpath=$(dirname $0)

##  do-bootstrap.sh.sh -h <host> [-i ssh_keyfile] [-D] <Role1> <Role2>
USAGE="  $prog -H <host> [-i ssh_keyfile] role1 role2
        $prog --list   : List available Roles
        $prog --help   : This help message

        -t <task> : only perform the task(s).
            Single role can only be specified with task option
            comma separate multiple tasks (no spaces)
        -I    : Ignore existing Bootstrap roles check for reapply
        -u <user>   : Change user from default 'ubuntu'
        -D    : Debug mode (show running & output)
          *development versions - Debug on by default"

ROLES_FOUND=$(cat ${dirpath}/roles.yml | grep -v -e ^# -e ^$ -e '^ ' | cut -d: -f1)
SSH_ID_OPT="-k"
FAB_USER=ubuntu
#FAB_HIDE="--hide=running,output"

[ ! $1 ] && echo "USAGE:$USAGE" && exit 1

# check if list or help #
case $1 in
    --list|list|-l)
            echo "Available Roles:"
            for r in ${ROLES_FOUND}; do
                echo "      $r"
            done
            echo
            exit 0
            ;;
    --help|help|"-?"|"?")
            echo "USAGE:$USAGE"
            echo
            exit 0
            ;;
esac

# process command line args #
while getopts "H:P:i:u:t:ID" opt; do
    case ${opt} in
        H)  HOST="$OPTARG"
            ;;
        P)  P_HOSTS="$OPTARG"
            ;;
        i)  SSH_ID_OPT="-i $OPTARG"
            ;;
        u)  FAB_USER="$OPTARG"
            ;;
        D)  FAB_HIDE=""
            ;;
        t)  FAB_TASKS="$OPTARG"
            ;;
        I)  IGNORE_EXISTING="YES"
            ;;
        *)  echo "USAGE:$USAGE"
            echo
            exit 1
    esac
done
shift $(( OPTIND - 1 ))
CLI_ROLES=$@
CLI_TASK_ROLE=$1

# make sure we only have one role with task option #
if [ ${FAB_TASKS} ]; then
    if [ ${CLI_TASK_ROLE} ]; then
        Found="false"
        for rf in ${ROLES_FOUND}; do
            if [ $(echo "$CLI_TASK_ROLE" | cut -d: -f1) == "$rf" ]; then
                Found="true"
            fi
        done
        if [ "$Found" == "false" ]; then
            echo "Unknown bootstrap role: ${CLI_TASK_ROLE}"
            exit 1
        fi
    fi
    TASK_ROLE=${CLI_TASK_ROLE}
    #_fab_tasks=$(echo ${FAB_TASKS} | sed -e 's/,/ /g')
    _fab_tasks=$(echo ${FAB_TASKS})
fi

# check for valid roles #
for cr in ${CLI_ROLES}; do
    Found="false"
    for rf in ${ROLES_FOUND}; do
        if [ $(echo "$cr" | cut -d: -f1) == "$rf" ]; then
            Found="true"
        fi
    done
    if [ "$Found" == "false" ]; then
        echo "Unknown bootstrap role: ${cr}"
        exit 1
    fi
done

if [ ${HOST} ]; then
    HOST_CMD="-H ${HOST}"
elif [ ${P_HOSTS} ]; then
    HOST_CMD="-H ${P_HOSTS} -P"
fi

if [ ${_fab_tasks} ]; then
    # Process Fab Tasks
    TASK_LINE="bootstrap_tasks:${TASK_ROLE},${_fab_tasks}"

    #DEBUG
    #echo "DEBUG: fab --user=$FAB_USER $HOST_CMD $SSH_ID_OPT $FAB_HIDE $TASK_LINE"
    cd ${dirpath} && IGNORE_EXISTING="$IGNORE_EXISTING" fab --user=$FAB_USER $HOST_CMD $SSH_ID_OPT $FAB_HIDE $TASK_LINE
else
    # Process Fab Roles
    # expand Roles prepend fab function and single line #
    for urol in ${CLI_ROLES}; do
        ROLE_LINE="$ROLE_LINE bootstrap_role:$urol"
    done

    #echo "DEBUG: fab --user=$FAB_USER $HOST_CMD $SSH_ID_OPT $FAB_HIDE $ROLE_LINE"
    cd ${dirpath} && IGNORE_EXISTING="$IGNORE_EXISTING" fab --user=$FAB_USER $HOST_CMD $SSH_ID_OPT $FAB_HIDE $ROLE_LINE
fi



