# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WebTelemetry US Inc.             #
# Author: Yuri Lermonotov <ylermontov@webtelemetry.us>  #
########################################################

dep 'ejabberd.bin' do
  provides 'ejabberd', 'ejabberdctl'
end

dep 'ejabberd.installed' do
  executable Babushka.host.linux? ? '/usr/sbin/ejabberd' : '/usr/local/sbin/ejabberdctl'
  package Babushka.host.linux? ? 'ejabberd' : 'ejabberd'
end

dep('ejabberd.service') do
  requires('ejabberd.installed')

  service Babushka.host.linux? ? 'ejabberd' : 'homebrew.mxcl.ejabberd'

  on :linux do
    met? {process_exists?('ejabberd', /ejabberd\.cfg/)}
  end
  on :osx do
    met? {shell("ejabberdctl status").to_s.match(/running/)}
    meet {shell("ejabberdctl start")}
  end
end

dep 'ejabberd' do
  requires 'ejabberd.service'
end
