#!/usr/bin/env bash
#
# Run from ai/ansible/playbooks/grafana and
# make sure ansible.cfg has correct key.
#
# Example:
#
# cd ai/ansible/playbooks/grafana && ../../../utils/scripts/show-vers.sh
#
ENVS="bpa-acceptance bpa-prod bpa-test walmart-prod ffx-test demo demo2 demo3x dev07 dev04 dev01  grafana-performance walmart-prod walmart-test prod04 prod04-acceptance prodops qa04 qa07"

if [ "$1" != "" ]; then
  ENV_STACK="$1"
else
  PS3="Select Stack: "
  select STACK in $ENVS
  do
    ENV_STACK="$STACK"
    unset PS3
    break
  done
fi

INV="inventory/$ENV_STACK"

echo "*** Quering stack $ENV_STACK"

ansible -i $INV -m shell -a "cd /WT/appserver ; git describe" -U webtelemetry --sudo webtelemetry
ansible -i $INV -m shell -a "cd /WT/appserver ; git describe" -U webtelemetry --sudo grafana
ansible -i $INV -m shell -a "cd /WT/influxdb ; git describe" -U webtelemetry --sudo influxdb
ansible -i $INV -m shell -a "cd /WT/appserver ; git describe" -U webtelemetry --sudo telemetrix:snmp
ansible -i $INV -m shell -a "cd /WT/grafana ; git describe" -U webtelemetry --sudo grafana
ansible -i $INV -m shell -a ". /WT/virtualenvs/telemetrix/bin/activate && pip freeze| egrep 'telemetrix|webtelemetry'" -U webtelemetry --sudo telegraf
ansible -i $INV -m shell -a ". /WT/virtualenvs/telemetrix/bin/activate && pip freeze| egrep 'telemetrix|webtelemetry'" -U webtelemetry --sudo hbase-workers

exit
