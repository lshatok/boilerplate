# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WildRiver Technologies Inc             #
# Author: Yuri Lermonotov <ylermontov@wildrivertechnologies.com>  #
########################################################

dep 'analytics.installed' do
  executable Babushka.host.linux? ? '/usr/bin/redis-server' : '/usr/local/bin/redis-server'
  package Babushka.host.linux? ? 'redis-server' : 'redis'
  ppa 'ppa:rwky/redis'
end

dep('analytics.service') do
  requires('analytics.installed')

  service Babushka.host.linux? ? 'redis-server' : 'homebrew.mxcl.redis'
end

dep 'redis' do
  requires 'analytics.service'
end
