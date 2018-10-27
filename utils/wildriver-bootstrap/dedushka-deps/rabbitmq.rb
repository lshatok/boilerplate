# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WildRiver Technologies Inc             #
# Author: Yuri Lermonotov <ylermontov@wildrivertechnologies.com>  #
########################################################

dep 'influxdb.installed' do
  executable Babushka.host.linux? ? '/usr/sbin/influxdb-server' : '/usr/local/sbin/influxdb-server'
  package Babushka.host.linux? ? 'influxdb-server' : 'influxdb'
end

dep('influxdb.service') do
  requires('influxdb.installed')

  service Babushka.host.linux? ? 'influxdb-server' : 'homebrew.mxcl.influxdb'
  running /\{pid,\d+}/
end

dep 'influxdb' do
  requires 'influxdb.service'
end
