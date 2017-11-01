==============================
ANSIBLE Playbooks WebTelemetry
==============================

Required:
  Ansible Installed
  Boto Installed
  AWS account IAM Key/Secret exported for boto
  VPC Infrastructure prepared & set-up
  VPN / Network connectivity to VPC
  vpc file created under vars with VPC and region defined


Define AWS instances and launch then with ansible.

1. under host_vars, cp host-template <name of instance>

2. edit the host vars file with the required data

3. edit hosts file with name of host, ansible_ssh_host=127.0.0.1, and instance type

4. ansible-playbook -i hostfiles/hosts-{aws-account} ec2_launch.yml -e "target=<instance_name>" --private-key=<keyfile>

### Examples:

EC2

```
ansible-playbook -i inventory/hosts-webtelemetrydev ec2_launch.yml -e "target=telemetrix-qa.redis1.webtelemetry.amazon.aws" --private-key="/path/to/ssh/private-key/webtelemetry-dev"
```

ELB

```
ansible-playbook -i inventory elbs.yml -e "deploy_env=dev01 "
```

Route53 for ELB

```
ansible-playbook -i inventory amazon_route53_elb.yml -e "deploy_env=dev01 "
```
