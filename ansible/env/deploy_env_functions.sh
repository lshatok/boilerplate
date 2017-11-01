#!/usr/bin/env bash
debug () {
    if [ $DEBUG ]; then
        echo ""
        echo "$1"
    fi
}

store_var () {
    eval VARVALUE=\$$1
    echo "$1=\"$VARVALUE\"" >> $CONFIGFILE
}

setup_hosts () {
    VPCVARFILENAME="$ENVNAME-vpc_vars.yml"
    store_var VPCVARFILENAME
    HOSTSFILENAME="$ENVNAME-hosts.yml"
    store_var HOSTSFILENAME
    AWSHOSTVARDIR="../playbooks/aws/host_vars/$ENVNAME"
    WTHOSTVARDIR="../playbooks/webtelemetry/host_vars/$ENVNAME"
    HOSTVARS=""

    #create the VPC Vars file
    debug "Creating VPC Vars file $VPCVARFILENAME"
    {
    	echo "---"
    	echo "vpcid:  $VPCID"
    	echo "region:  $EC2REGION"
    	echo "key_name:  aws_ps_20150311"
    	echo "count: 1"
    	echo "security_groups: $SECURITYGROUPID"
    	echo "tags:"
    customer: $ENVNAME"
    	echo "network_name: $ENVNAME"
	}  > $VPCVARFILENAME
	VPCVARS="vpc_var=../../../deployments/$VPCVARFILENAME"

    debug "Creating inventory file $HOSTSFILENAME"
    #create the hosts.yml file
    {
    	echo "[$ENVNAME]"
    	echo "$ENVNAME-ops.{{ product.url }} type=m3.medium $VPCVARS subnet=$FRONTHAULSUBNETID"
        echo "$ENVNAME-grafana.webtelemetry.amazon.aws type=m3.large $VPCVARS subnet=$FRONTHAULSUBNETID"
	    echo "$ENVNAME-grafana.webtelemetry.amazon.aws type=m3.medium $VPCVARS subnet=$FRONTHAULSUBNETID"
	    echo "$ENVNAME-jrrd.webtelemetry.amazon.aws type=m3.large $VPCVARS subnet=$BACKHAULSUBNET1ID"
    	echo "$ENVNAME-hbase-master.webtelemetry.amazon.aws type=m3.large $VPCVARS subnet=$BACKHAULSUBNET1ID"

    	echo "[$ENVNAME-hbase-workers]"
    	echo "$ENVNAME-hbase-worker[1:$HBASEWORKERS].webtelemetry.amazon.aws type=m3.large $VPCVARS subnet=$BACKHAULSUBNET1ID"

	    echo "[$ENVNAME-rds]"
    	echo "$ENVNAME-rds.webtelemetry.amazon.aws $VPCVARS"
	} > $HOSTSFILENAME

	#Devops
	echo "application: DevOps"

volumes:
  - device_name: /dev/sda1
    volume_size: 30
    delete_on_termination: false
  - device_name: /dev/sdf
    volume_size: 30
    delete_on_termination: false

assign_eip: no" > $AWSHOSTVARDIR-ops.{{ product.url }}
	HOSTVARS+="$AWSHOSTVARDIR-ops.{{ product.url }} "

    echo "---"
branch: master
webtelemetry_home: /WT

domain: dev.{{ product.url }}" > $AGHOSTVARDIR-ops.{{ product.url }}
    HOSTVARS+="$AGHOSTVARDIR-ops.{{ product.url }}"
	
	#grafana
	echo "application: grafana"

volumes:
  - device_name: /dev/sda1
    volume_size: 30
    delete_on_termination: false
  - device_name: /dev/sdf
    volume_size: 30
    delete_on_termination: false

assign_eip: yes" > $AWSHOSTVARDIR-grafana.webtelemetry.amazon.aws
	HOSTVARS+="$AWSHOSTVARDIR-grafana.webtelemetry.amazon.aws "

    echo "---"
branch: 2.0
webtelemetry_home: /WT
webtelemetry_path:  /WT/appserver" > $AGHOSTVARDIR-grafana.webtelemetry.amazon.aws
    HOSTVARS+="$AGHOSTVARDIR-grafana.webtelemetry.amazon.aws"

	#
	echo "application: {{ product.codename }}"

volumes:
  - device_name: /dev/sda1
    volume_size: 30
    delete_on_termination: false
  - device_name: /dev/sdf
    volume_size: 30
    delete_on_termination: false

assign_eip: yes" > $AWSHOSTVARDIR-grafana.webtelemetry.amazon.aws
	HOSTVARS+="$AWSHOSTVARDIR-grafana.webtelemetry.amazon.aws "

    echo "---
branch: \"1.10\"
webtelemetry_home: /WT
webtelemetry_path: /WT/appserver" > $AGHOSTVARDIR-grafana.webtelemetry.amazon.aws
    HOSTVARS+="$AGHOSTVARDIR-grafana.webtelemetry.amazon.aws"

	#Grafana
	echo "application: Grafana"

volumes:
  - device_name: /dev/sda1
    volume_size: 30
    delete_on_termination: false
  - device_name: /dev/sdf
    volume_size: 30
    delete_on_termination: false

assign_eip: false" > $AWSHOSTVARDIR-jrrd.webtelemetry.amazon.aws
	HOSTVARS+="$AWSHOSTVARDIR-jrrd.webtelemetry.amazon.aws "

	#HBase Master
	echo "application: HBase-Master"

volumes:
  - device_name: /dev/sda1
    volume_size: 30
    delete_on_termination: false
  - device_name: /dev/sdf
    volume_size: 30
    delete_on_termination: false
  - device_name: /dev/sda1
    volume_size: 100
    delete_on_termination: false
  - device_name: /dev/sdf
    volume_size: 30
    delete_on_termination: false
  - device_name: /dev/sdi
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdj
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdk
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdl
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdm
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdn
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdo
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdp
    volume_size: 50
    delete_on_termination: false

assign_eip: false" > $AWSHOSTVARDIR-hbase-master.webtelemetry.amazon.aws
	HOSTVARS+="$AWSHOSTVARDIR-hbase-master.webtelemetry.amazon.aws "

	#HBase Workers
	for (( i=1; i<=$HBASEWORKERS; i++ )); do
		echo "application: HBase-Worker"
    done

volumes:
  - device_name: /dev/sda1
    volume_size: 30
    delete_on_termination: false
  - device_name: /dev/sdf
    volume_size: 30
    delete_on_termination: false
  - device_name: /dev/sda1
    volume_size: 100
    delete_on_termination: false
  - device_name: /dev/sdf
    volume_size: 30
    delete_on_termination: false
  - device_name: /dev/sdi
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdj
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdk
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdl
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdm
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdn
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdo
    volume_size: 50
    delete_on_termination: false
  - device_name: /dev/sdp
    volume_size: 50
    delete_on_termination: false

assign_eip: false" > $AWSHOSTVARDIR-hbase-worker$i.webtelemetry.amazon.aws
	done
	HOSTVARS+="$AWSHOSTVARDIR-hbase-worker.webtelemetry.amazon.aws "

    #RDS Instance
    echo "rds_subnets:
  - $BACKHAULSUBNET1ID
  - $BACKHAULSUBNET2ID

region: $EC2REGION

zone: $AVAILABILITYZONE1

subnetgroup_name: \"SubnetGroup_$ENVNAME\"

description: $ENVNAME

type: db.t2.small

instance_name: \"$DBINSTANCENAME\"
size: 30

admin_user:  "{{ product.admin }}"
admin_pass: "{{ product.admin.pass }}"

# Backup retention days [0-35]
backup_retention: 3

vpc_security_groups: \"$SECURITYGROUPID\"" > $AWSHOSTVARDIR-rds.webtelemetry.amazon.aws
    HOSTVARS+="$AWSHOSTVARDIR-rds.webtelemetry.amazon.aws "

    store_var HOSTVARS

}

#params: instance ID, status to wait for
wait_for_ec2 () {
    if [ -z "$1" ]; then
		echo 'Please pass an instance ID' 1>&2
		exit 1
    fi
    if [ -z "$2" ]; then
		LOOKFOR="running"
    else
		LOOKFOR=$2
    fi
    echo "Waiting for $1 to be $LOOKFOR"
    OVER=0
    TESTS=0
    while [ $OVER != 1 ] && [ $TESTS -lt $MAX_TESTS ]; do
    	description=$(ec2-describe-instances $1)
		if  [ $LOOKFOR == running ]; then
		    STATE=$(echo "$description" | awk '/^INSTANCE/ {print $5}')
		else
		    STATE=$(echo "$description" | awk '/^INSTANCE/ {print $4}')
		fi
		if [ "$STATE" = "" ]; then
		    echo "No instance $1 existing. Crashed or was terminated." 1>&2
		    exit 1
		fi
		echo "STATE = $STATE"
		if [ $STATE = $LOOKFOR ]; then
		    OVER=1
		else
		    TESTS=$(echo $TESTS+1 | bc)
		    sleep 2
		fi
    done
    if [ $TESTS -eq $MAX_TESTS ] && [ $LOOKFOR == 'running' ]; then
		echo "$1 never got to $LOOKFOR state" 1>&2
		ec2-terminate-instances $1
		destroy_env
		exit 1
    fi
}

#params: VPN Connection ID, status to wait for
wait_for_vpn () {
    if [ -z "$1" ]; then
		echo 'Please pass a VPN Connection ID' 1>&2
		exit 1
    fi
    if [ -z "$2" ]; then
		LOOKFOR="deleted"
    else
		LOOKFOR=$2
    fi
    echo "Waiting for $1 to be $LOOKFOR"
    OVER=0
    TESTS=0
    while [ $OVER != 1 ] && [ $TESTS -lt $MAX_TESTS ]; do
    	cmd=$(ec2-describe-vpn-connections $1)
		STATE=$(echo "$cmd" | awk '/^VPNCONNECTION/ {print $3}')
		if [ "$STATE" = "" ]; then
		    echo "No VPN Connection $1 existing." 1>&2
		    exit 1
		fi
		echo "STATE = $STATE"
		if [ $STATE = $LOOKFOR ]; then
		    OVER=1
		else
		    TESTS=$(echo $TESTS+1 | bc)
		    sleep 2
		fi
    done
    if [ $TESTS -eq $MAX_TESTS ] && [ $LOOKFOR == 'available' ]; then
		echo "$1 never got to $LOOKFOR state" 1>&2
		ec2-delete-vpn-connection $1
		destroy_env
		exit 1
    fi
}

#params: VPN Gateway ID
wait_for_vgw-detachment() {
    if [ -z "$1" ]; then
		echo 'Please pass a VPN Gateway ID' 1>&2
		exit 1
    fi
    echo "Waiting for $1 to be detached"
    OVER=0
    TESTS=0
    while [ $OVER != 1 ] && [ $TESTS -lt $MAX_TESTS ]; do
    	cmd=$(ec2-describe-vpn-gateways $1)
		STATE=$(echo "$cmd" | awk '/^VGWATTACHMENT.*(ing|attach)/ {print $3}')
		if [ "$STATE" = "" ]; then
			echo "VPN Gateway $1 not attached." 1>&2
			OVER=1
		else
			echo "STATE = $STATE"
		    TESTS=$(echo $TESTS+1 | bc)
		    sleep 2
		fi
    done
    if [ $OVER -eq 0 ]; then
		echo "$1 never got to detached state" 1>&2
		destroy_env
		exit 1
    fi
}

destroy_env () {
	STARTTIME=$(date +%s)

    #Destroy Environment
    echo 'Destroying Environment'

    #Delete VPN Connection
    if [ -n "$VPNCONNECTIONID" ]; then
        ec2-delete-vpn-connection "$VPNCONNECTIONID"
    fi
    
    #Terminate All VPC Instances
    if [ -n "$VPCID" ]; then
        cmd=$(ec2-describe-instances --filter "vpc-id=$VPCID")
        INSTANCES=$(echo "$cmd" | awk '/^INSTANCE.*(runn|shutt|pend)ing/ {print $2}')
        if [ -n "$INSTANCES" ]; then
            ec2-terminate-instances $INSTANCES
        fi
    fi

    #Detach VPN Gateway
    if [[ -n "$VPNGATEWAYID" && -n "$VPCID" ]]; then
        ec2-detach-vpn-gateway "$VPNGATEWAYID" -c "$VPCID"
    fi

    #Wait for VPN to be deleted
    if [ -n "$VPNCONNECTIONID" ]; then
        wait_for_vpn "$VPNCONNECTIONID"
    fi

    #Delete Customer Gateway
    if [ -n "$CUSTOMERGATEWAYID" ]; then
        ec2-delete-customer-gateway "$CUSTOMERGATEWAYID"
    fi

    #Wait for VPN Gateway to be detached
    if [ -n "$VPNGATEWAYID" ]; then
        wait_for_vgw-detachment "$VPNGATEWAYID"

        #Delete VPN Gateway
        ec2-delete-vpn-gateway "$VPNGATEWAYID"
    fi

    #Wait for instances to be terminated
    if [ -n "$INSTANCES" ]; then
        for INSTANCE in $INSTANCES; do
        	wait_for_ec2 $INSTANCE terminated
        done
    fi
    
    #Release Elastic IPs
    if [ -n "$NATADDRESSID" ]; then
        #ec2-disassociate-address -a $NATADDRESSALLOCID
        ec2-release-address -a "$NATADDRESSID"
    fi

    #Delete Route Tables (No need to delete main route table)
    if [ -n "$FRONTHAULRTBASSOCID" ]; then
        ec2-disassociate-route-table "$FRONTHAULRTBASSOCID"
    fi
    if [ -n "$BACKHAULRTBASSOC1ID" ]; then
        ec2-disassociate-route-table "$BACKHAULRTBASSOC1ID"
    fi
    if [ -n "$BACKHAULRTBASSOC2ID" ]; then
        ec2-disassociate-route-table "$BACKHAULRTBASSOC2ID"
    fi
    if [ -n "$BACKHAULROUTETABLEID" ]; then
        ec2-delete-route-table "$BACKHAULROUTETABLEID"
    fi
    
    #Delete Internet Gateway
    if [[ -n "$INTERNETGATEWAYID" && -n "$VPCID" ]]; then 
        ec2-detach-internet-gateway "$INTERNETGATEWAYID" -c "$VPCID"
        ec2-delete-internet-gateway "$INTERNETGATEWAYID"
    fi
    
    #Delete Subnets
    ##Fronthaul
    if [ -n "$FRONTHAULSUBNETID" ]; then 
        ec2-delete-subnet "$FRONTHAULSUBNETID"
    fi
    ##Backhaul 1
    if [ -n "$BACKHAULSUBNET1ID" ]; then 
        ec2-delete-subnet "$BACKHAULSUBNET1ID"
    fi
    ##Backhaul 2
    if [ -n "$BACKHAULSUBNET2ID" ]; then 
        ec2-delete-subnet "$BACKHAULSUBNET2ID"
    fi

    #Delete VPC
    if [ -n "$VPCID" ]; then 
        ec2-delete-vpc "$VPCID"
        if [ $? -ne 0 ]; then
            echo "Could not delete VPC"
            exit
        fi
    fi

    if [ -n "$HOSTSFILENAME" -a -a "$HOSTSFILENAME" ]; then 
        rm "$HOSTSFILENAME"
    fi
    if [ -n "$VPCVARFILENAME" -a -a "$VPCVARFILENAME" ]; then 
        rm "$VPCVARFILENAME"
    fi
    if [ -n "$HOSTVARS" ]; then 
        for HOSTVAR in "$HOSTVARS"; do
            rm $HOSTVAR
            if [ $? -ne 0 ]; then
                echo "Could not delete $HOSTVAR"
                exit
            fi
        done
    fi

    rm $CONFIGFILE

    ENDTIME=$(date +%s)
	TIMETODESTROY=$(($ENDTIME - $STARTTIME))
	echo "Time to Destroy Environment: $TIMETODESTROY seconds"
}

setup_vpn () {
    #Create Customer Gateway
    debug "Create Customer Gateway"
    debug "ec2-create-customer-gateway -t ipsec.1 -i $OFFICEIP -b 65000"
    cmd=$(ec2-create-customer-gateway -t ipsec.1 -i $OFFICEIP -b 65000)
    CUSTOMERGATEWAYID=$(echo "$cmd" | awk '/^CUSTOMERGATEWAY/ {print $2}')
    ec2-create-tags $CUSTOMERGATEWAYID --tag "Name=$ENVNAME WebTelemetry Office Customer Gateway"
    store_var CUSTOMERGATEWAYID

    #Setup Virtual Private Gateway
    cmd=$(ec2-create-vpn-gateway -t ipsec.1)
    VPNGATEWAYID=$(echo "$cmd" | awk '/^VPNGATEWAY/ {print $2}')
    ec2-create-tags $VPNGATEWAYID --tag "Name=$ENVNAME VPN Gateway"
    store_var VPNGATEWAYID

    #Attach VPN Gateway to VPC
    debug "Attach VPN Gateway to VPC"
    debug "ec2-attach-vpn-gateway $VPNGATEWAYID -c $VPCID"
    ec2-attach-vpn-gateway $VPNGATEWAYID -c $VPCID

    #Create VPN Connection
    cmd=$(ec2-create-vpn-connection -t ipsec.1 --customer-gateway $CUSTOMERGATEWAYID --vpn-gateway $VPNGATEWAYID)
    VPNCONNECTIONID=$(echo "$cmd" | awk '/^VPNCONNECTION/ {print $2}')
    ec2-create-tags $VPNCONNECTIONID --tag "Name=$ENVNAME WebTelemetry Office VPN Connection"
    store_var VPNCONNECTIONID
}

create_env () {
	STARTTIME=$(date +%s)

	##########################################
	#Create Environment
	echo "Creating Environment for $ENVNAME"

    touch $CONFIGFILE; cat /dev/null > $CONFIGFILE

	#Create VPC
	cmd=$(ec2-create-vpc $VPCCIDR)
	VPCID=$(echo "$cmd" | awk '/^VPC/ {print $2}')
	ec2-create-tags $VPCID --tag "Name=$ENVNAME"
    store_var VPCID

	#Create Subnets
	##Fronthaul
	cmd=$(ec2-create-subnet -c $VPCID -i $FRONTHAULSUBNETCIDR)
	FRONTHAULSUBNETID=$(echo "$cmd" | awk '/^SUBNET/ {print $2}')
	ec2-create-tags $FRONTHAULSUBNETID --tag "Name=$ENVNAME Fronthaul"
    store_var FRONTHAULSUBNETID

	##Backhaul 1
	cmd=$(ec2-create-subnet -c $VPCID -i $BACKHAULSUBNET1CIDR -z $AVAILABILITYZONE1)
	BACKHAULSUBNET1ID=$(echo "$cmd" | awk '/^SUBNET/ {print $2}')
	ec2-create-tags $BACKHAULSUBNET1ID --tag "Name=$ENVNAME Backhaul 1"
    store_var BACKHAULSUBNET1ID

    ##Backhaul 2
    cmd=$(ec2-create-subnet -c $VPCID -i $BACKHAULSUBNET2CIDR -z $AVAILABILITYZONE2)
    BACKHAULSUBNET2ID=$(echo "$cmd" | awk '/^SUBNET/ {print $2}')
    ec2-create-tags $BACKHAULSUBNET2ID --tag "Name=$ENVNAME Backhaul 2"
    store_var BACKHAULSUBNET2ID

	#Create Internet Gateway
	cmd=$(ec2-create-internet-gateway)
	INTERNETGATEWAYID=$(echo "$cmd" | awk '/^INTERNETGATEWAY/ {print $2}')
	ec2-create-tags $INTERNETGATEWAYID --tag "Name=$ENVNAME Internet Gateway"
    store_var INTERNETGATEWAYID

	#Attach Internet Gateway to VPC
    debug "Attaching Internet Gateway"
    debug "ec2-attach-internet-gateway $INTERNETGATEWAYID -c $VPCID"
	ec2-attach-internet-gateway $INTERNETGATEWAYID -c $VPCID

	#Create Route Tables
	##Fronthaul
	cmd=$(ec2-describe-route-tables --filter "vpc-id=$VPCID")
	FRONTHAULROUTETABLEID=$(echo "$cmd" | awk '/^ROUTETABLE/ {print $2}')
	ec2-create-tags $FRONTHAULROUTETABLEID --tag "Name=$ENVNAME Fronthaul/Main Route Table"
    store_var FRONTHAULROUTETABLEID

	###Associate Route Table to Fronthaul Subnet
	cmd=$(ec2-associate-route-table $FRONTHAULROUTETABLEID -s $FRONTHAULSUBNETID)
	FRONTHAULRTBASSOCID=$(echo "$cmd" | awk '/^ASSOCIATION/ {print $2}')
    store_var FRONTHAULRTBASSOCID

	###Add Internet Gateway to Fronthaul Route Table
	ec2-create-route $FRONTHAULROUTETABLEID -r 0.0.0.0/0 -g $INTERNETGATEWAYID

	##Backhaul
	cmd=$(ec2-create-route-table $VPCID)
	BACKHAULROUTETABLEID=$(echo "$cmd" | awk '/^ROUTETABLE/ {print $2}')
	ec2-create-tags $BACKHAULROUTETABLEID --tag "Name=$ENVNAME Backhaul Route Table"
    store_var BACKHAULROUTETABLEID

	###Associate Route Table to Backhaul Subnets
	cmd=$(ec2-associate-route-table $BACKHAULROUTETABLEID -s $BACKHAULSUBNET1ID)
	BACKHAULRTBASSOCID=$(echo "$cmd" | awk '/^ASSOCIATION/ {print $2}')
    store_var BACKHAULRTBASSOC1ID
    cmd=$(ec2-associate-route-table $BACKHAULROUTETABLEID -s $BACKHAULSUBNET2ID)
    BACKHAULRTBASSOCID=$(echo "$cmd" | awk '/^ASSOCIATION/ {print $2}')
    store_var BACKHAULRTBASSOC2ID

	#Security Groups
	cmd=$(ec2-describe-group --filter "vpc-id=$VPCID")
	SECURITYGROUPID=$(echo "$cmd" | awk '/^GROUP/ {print $2}')
	ec2-create-tags $SECURITYGROUPID --tag "Name=$ENVNAME Default"
    store_var SECURITYGROUPID

    #Setup VPN connection (customer gateway, vpn gateway, vpn connection) - deprecated in support of VPC Peering
	#setup_vpn

    #Setup VPC Peering
    cmd=$(ec2-create-vpc-peering-connection -c $VPCID -p $DEVOPSVPCID -o $DEVOPSACCOUNTID)
    VPCPEERINGCONNECTIONID=$(echo "$cmd" | awk '/^VPCPEERINGCONNECTION/ {print $2}')

    ##Add ai CIDR to security group
    ec2-authorize $SECURITYGROUPID -s $DEVOPSCIDR -P all

    ##Add routes to ai cidr
    ec2-create-route $FRONTHAULROUTETABLEID -r $DEVOPSCIDR -p $VPCPEERINGCONNECTIONID
    ec2-create-route $BACKHAULROUTETABLEID -r $DEVOPSCIDR -p $VPCPEERINGCONNECTIONID

    echo 'VPC Peering Connection Requested, please accept it from the ai VPC'

	ENDTIME=$(date +%s)
	TIMETOCREATE=$(($ENDTIME - $STARTTIME))
	echo "Time to Create Environment: $TIMETOCREATE seconds"
}

create_NAT () {
    #Find NAT AMI
    cmd=$(ec2-describe-images -o amazon --filter "name=*amzn-ami-vpc-nat-hvm-2014.09*")
    NATAMIID=$(echo "$cmd" | awk '/^IMAGE/ {print $2}')

    ###Create NAT Instance in Fronthaul Subnet
    cmd=$(ec2-run-instances $NATAMIID --subnet $FRONTHAULSUBNETID --instance-type "t2.micro")
    NATID=$(echo "$cmd" | awk '/^INSTANCE/ {print $2}')
    ec2-create-tags $NATID --tag "Name=$ENVNAME.NAT"
    store_var NATID

    #Release Elastic IPs
    if [ -n "$VPCID" ]; then
        cmd=$(ec2-describe-addresses)
        ADDRESSES=$(echo "$cmd" | awk '/^ADDRESS/ {print $4}')
        if [ -n "$ADRESSES" ]; then
            for ADDRESS in $ADDRESSES; do
                ec2-release-address -a "$ADDRESS"
            done
        else
            debug 'No Elastic IPs to release'
        fi
    else
        echo "Need VPCID"
        exit
    fi

    ###Allocate Elastic IP for NAT
    cmd=$(ec2-allocate-address -d vpc)
    NATADDRESSID=$(echo "$cmd" | awk '/^ADDRESS/ {print $4}')
    store_var NATADDRESSID

    ###Wait for NAT to become ready
    wait_for_ec2 $NATID

    ###Associate Elastic IP to NAT
    cmd=$(ec2-associate-address -i $NATID -a $NATADDRESSID)
    NATADDRESSALLOCID=$(echo "$cmd" | awk '/^ADDRESS/ {print $4}')
    store_var NATADDRESSALLOCID 

    ###Add NAT to Backhaul
    ec2-create-route $BACKHAULROUTETABLEID -r 0.0.0.0/0 -i $NATID

    ###Disable source check
    ec2-modify-instance-attribute $NATID --source-dest-check false
}

env () {
    STARTTIME=$(date +%s)

    #Check for OpenVPN connectivity
    if [ $(ifconfig | grep utun0 -c) -ne 1 ]; then
        echo 'Not connected to OpenVPN tunnel'
        exit
    fi

    echo "Deploying Environment"

    create_NAT

    #Create temporary host inventory file for this deployment
    setup_hosts

    cd ../playbooks/aws/
    INVENTORYFILENAME=../../deployments/$HOSTSFILENAME

    #Set up EC2 instances (grafana, Grafana, etc)
    
    debug "Running ansible-playbook with inventory file $INVENTORYFILENAME"
    ansible-playbook -i $INVENTORYFILENAME aws-launch-ec2.yml -e "target=$ENVNAME-grafana.webtelemetry.amazon.aws"
    ansible-playbook -i $INVENTORYFILENAME aws-launch-ec2.yml -e "target=$ENVNAME-grafana.webtelemetry.amazon.aws"
    #ansible-playbook -i $INVENTORYFILENAME aws-launch-ec2.yml -e "target=$ENVNAME-ops.{{ product.url }}"
    ansible-playbook -i $INVENTORYFILENAME aws-launch-ec2.yml -e "target=$ENVNAME-jrrd.webtelemetry.amazon.aws"
    ansible-playbook -i $INVENTORYFILENAME aws-launch-ec2.yml -e "target=$ENVNAME-hbase-master.webtelemetry.amazon.aws"

    #Set up HBase Workers
    ansible-playbook -i $INVENTORYFILENAME aws-launch-ec2.yml -e "target=$ENVNAME-hbase-workers"

    #Set up RDS instance
    #ansible-playbook --vault-password-file=~/.ansible_vault_pass.txt -i $INVENTORYFILENAME launch.-rds.yml -e "target=$ENVNAME-rds"

    #TODO reset RDS password?



    ENDTIME=$(date +%s)
    echo "Time to Deploy Environment: $(($ENDTIME - $STARTTIME)) seconds"
}

cleanup_env () {
    STARTTIME=$(date +%s)

    if [ -z "$VPCID" ]; then
        echo 'Need VPCID'
        exit
    fi

    echo "Cleaning Up Environment"

    #Terminate All VPC Instances
    cmd=$(ec2-describe-instances --filter "vpc-id=$VPCID")
    INSTANCES=$(echo "$cmd" | awk '/^INSTANCE.*(runn|shutt|pend)ing/ {print $2}')
    if [ -n "$INSTANCES" ]; then
        ec2-terminate-instances $INSTANCES
    fi

    #Delete NAT Route
    ec2-delete-route "$BACKHAULROUTETABLEID" -r 0.0.0.0/0

    #Remove RDS
    rds-delete-db-instance "$DBINSTANCENAME" -f yes --skip-final-snapshot -I $AWS_ACCESS_KEY -S $AWS_SECRET_KEY

    #Wait for instances to be terminated
    if [ -n "$INSTANCES" ]; then
        for INSTANCE in $INSTANCES; do
            wait_for_ec2 $INSTANCE terminated
        done
    fi

    #TODO: Remove inactive volumes

    #Release Elastic IPs
    cmd=$(ec2-describe-addresses)
    ADDRESSES=$(echo "$cmd" | awk '/^ADDRESS/ {print $4}')
    if [ -n "$ADDRESSES" ]; then
        for ADDRESS in $ADDRESSES; do
            ec2-release-address -a $ADDRESS
        done
    fi

    #Remove Ansible-related files
    if [ -n "$HOSTSFILENAME" -a -a "$HOSTSFILENAME" ]; then 
        rm "$HOSTSFILENAME"
    fi
    if [ -n "$VPCVARFILENAME" -a -a "$VPCVARFILENAME" ]; then 
        rm "$VPCVARFILENAME"
    fi
    if [ -n "$HOSTVARS" ]; then 
        for HOSTVAR in $HOSTVARS; do
            if [ -a $HOSTVAR ]; then
                rm $HOSTVAR
            fi
        done
    fi

    ENDTIME=$(date +%s)
    TIMETOCLEANUP=$(($ENDTIME - $STARTTIME))
    echo "Time to Cleanup Environment: $TIMETOCLEANUP seconds"
}