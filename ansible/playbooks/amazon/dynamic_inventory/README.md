=========================
ANSIBLE Dynamic Inventory
=========================

Required:
--------
  * Ansible Installed
  * Boto Installed
  * AWS account IAM Key/Secret exported for boto
    * Example:
      ```
      export AWS_REGION=us-west-2
      export AWS_SECRET_ACCESS_KEY=LIuthPfKbwOC64m+wXXXXXXXXXXXXXXXXXIBF5p1
      export AWS_ACCESS_KEY_ID=AKxxxxxxxxxxxxxxxxZA
      ```
  * Update ec2.ini file
    * For example - update 'regions' from 'all' to 'us-west-2'. Default value - 'all'
    * or
    * For example - include RDS instances. Change rds = 'False' to rds = 'True'



Use:
---

```
./ec2.py --refresh-cache
ansible-playbook -i ec2.py aws_inventory.yml
```

Also you can declare path to new inventory file

```
./ec2.py --refresh-cache
ansible-playbook -i ec2.py aws_inventory.yml -e dynamic_inv=~/webtelemetry/inventory.ini
```
