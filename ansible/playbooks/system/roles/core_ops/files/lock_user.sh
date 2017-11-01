#!/bin/bash
## Lock User script ##

LOCK_USER=$1

# check if root #
if [ "$(whoami)" != "root" ]; then
	echo "Opps, you must be root"
	exit 1
fi

while [ ! $LOCK_USER ]; do
	echo -n "Enter User Account to Lock: "
	read LOCK_USER
done

# Protect root or ubuntu user #
if [ "$LOCK_USER" == "root" ] || [ "$LOCK_USER" == "ubuntu" ]; then
	echo "Cannot lock $LOCK_USER user!"
	exit 1
fi

# check if user exists #
USER_FOUND=$(cat /etc/passwd | cut -d: -f1 | grep "^$LOCK_USER$")
if [ ! $USER_FOUND ]; then
	echo "Error: user '$LOCK_USER' does not exist."
	exit 1
fi

function lock_user() {
	echo -n "Lock user '$LOCK_USER'? (Y/n): "
	read YESNO
	if [ "$YESNO" == 'Y' ]; then
		usermod -L -e 1 $LOCK_USER
		usermod -s /bin/false $LOCK_USER
	else
		echo "skipping.."
		exit
	fi

}


# MAIN #
if [ $USER_FOUND ]; then
	grep $LOCK_USER /etc/passwd /etc/shadow
	lock_user
	grep $LOCK_USER /etc/passwd /etc/shadow
fi
