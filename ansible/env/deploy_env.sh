#!/usr/local/bin/bash

#Script for creating and destroying a full VPC environment in the PS AWS environment
#Authors: Leo Shatokhin

#Requirements: bash, ansible, ec2-api-tools, rds-command-line-tools

#Parameters: environment name, action (create/deploy/cleanup/destroy)
#Create: Create VPC container and all networking stuff
#Deploy: Create NAT and run Ansible scripts
#Cleanup: Remove NAT, terminate instances, and release elastic IPs
#Destroy: Remove VPC

#Configurable vars
EC2REGION=us-west-2
CIDRPREFIX=10.15.0
OFFICEIP=50.0.202.98
HBASEWORKERS=3
MAX_TESTS=60
DEBUG=1
RDSROOTPASSWORD=defaultrdspassword

DEVOPSVPCID=vpc-26c9b24d
DEVOPSACCOUNTID=049795576831
DEVOPSCIDR="10.0.0.0/18"

#Set up vars
VPCCIDR=$CIDRPREFIX.0/24
FRONTHAULSUBNETCIDR=$CIDRPREFIX.0/26
BACKHAULSUBNETCIDR1=$CIDRPREFIX.64/26
BACKHAULSUBNETCIDR2=$CIDRPREFIX.128/26
export EC2_REGION=$EC2REGION
export EC2_URL=https://ec2.$EC2REGION.amazonaws.com

#If AWS credentials do not exist, fail and let the user know they need to set these variables.
if [[ -z "$AWS_ACCESS_KEY" || -z "$AWS_SECRET_KEY" || -z "$AWSAccessKeyId" || -z "$AWSSecretKey" ]]; then
    echo "Before you can use these tools you must export some variables to your $SHELL."
    echo 'export AWS_ACCESS_KEY="<Your AWS Access ID>"'
    echo 'export AWS_SECRET_KEY="<Your AWS Secret Key>"'
    echo 'export AWSAccessKeyId="$AWS_ACCESS_KEY"'
    echo 'export AWSSecretKey="$AWS_SECRET_KEY"'
    exit
fi

#Include functions
source "deploy_env_functions.sh"

cmd=$(ec2-describe-availability-zones)
AVAILABILITYZONE1=$(echo "$cmd" | awk '/^AVAILABILITYZONE.*available/ {print $2}' | head -n 1)
AVAILABILITYZONE2=$(echo "$cmd" | awk '/^AVAILABILITYZONE.*available/ {print $2}' | head -n 2 | tail -n 1)

#If Environment Name is not specified, complain
if [ -z $1 ]; then
    echo "Please pass in the environment name"
	echo "Example: $0 BPA create"
    exit
fi

#If action is not specified, complain
if [ -z $2 ]; then
    echo "Please pass in an action (create/deploy/cleanup/destroy)"
	echo "Example: $0 BPA destroy"
    exit
fi

ENVNAME=$1.PS
DBINSTANCENAME="DB-${ENVNAME//./-}"

CONFIGFILE=$ENVNAME-config.cfg

if [ $2 == 'destroy' ]; then
	echo "Loading environment variables"
	source "$CONFIGFILE"
	cleanup_env
	destroy_env
elif [ $2 == 'deploy' ]; then
	echo "Loading environment variables"
	source "$CONFIGFILE"
	cleanup_env
	deploy_env
elif [ $2 == 'create' ]; then
	create_env
elif [ $2 == 'cleanup' ]; then
	echo "Loading environment variables"
	source "$CONFIGFILE"
	cleanup_env
else
	echo "Allowed actions are create, deploy, cleanup, destroy"
fi