#!/bin/bash

prog=$(basename $0)
dirpath=$(dirname $0)

##  manage-accounts.sh -h <host(s)> [-i ssh_keyfile] { user1 user2 | -g user_group1 user_group2 }
USAGE="  $prog -H <host(s)> [-i ssh_keyfile] user1 user2 (or -g user_group1 user_group2
        $prog --help   : This help message

        -u <user>   : Change user from default 'ubuntu'
        -P <host(s)> : use instead of -H to run in parallel mode
        -D    : Debug mode (show running & output)
          *development versions - Debug on by default"


SSH_ID_OPT="-k"
FAB_USER=ubuntu
#FAB_HIDE="--hide=running,output"

[ ! $1 ] && echo "USAGE:$USAGE" && exit 1

ACCOUNTS_FILE=accounts/wtusers.yml

# check if list or help #
case $1 in
    --help|help|"-?"|"?")
            echo "USAGE:$USAGE"
            echo
            exit 0
            ;;
esac

ACCOUNT_TASK=users
# process command line args #
while getopts "H:P:i:u:Dgs" opt; do
    case ${opt} in
        H)  HOST="$OPTARG"
            ;;
        P)  P_HOST="$OPTARG"
            ;;
        i)  SSH_ID_OPT="-i $OPTARG"
            ;;
        u)  FAB_USER="$OPTARG"
            ;;
        D)  FAB_HIDE=""
            DEBUG=True
            ;;
        g)  ACCOUNT_TASK=user_groups
            ;;
        *)  echo "USAGE:$USAGE"
            echo
            exit 1
    esac
done
shift $(( OPTIND - 1 ))
CLI_NAMES=$@

# expand Names to prepend fab function in a single line #
for urol in ${CLI_NAMES}; do
    [ -z $CLI_LINE ] && CLI_LINE=$urol || CLI_LINE="$CLI_LINE/$urol"
done

if [[ $P_HOST ]]; then
    HOST_CMD="-H ${P_HOST} -P"
else
    HOST_CMD="-H ${HOST}"
fi

#DEBUG
if [[ $DEBUG == "True" ]]; then
    echo "DEBUG: fab --user=$FAB_USER $HOST_CMD $SSH_ID_OPT $FAB_HIDE manage_accounts:$ACCOUNTS_FILE,${ACCOUNT_TASK}:$CLI_LINE"
else
    cd ${dirpath} && fab --user=$FAB_USER $HOST_CMD $SSH_ID_OPT $FAB_HIDE manage_accounts:$ACCOUNTS_FILE,${ACCOUNT_TASK}:$CLI_LINE
fi

