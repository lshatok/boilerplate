# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WebTelemetry US Inc.             #
# Author: Yuri Lermonotov <ylermontov@webtelemetry.us>  #
########################################################

dep 'postgresql.installed' do
  executable Babushka.host.linux? ? '/usr/sbin/postgresqld' : '/usr/local/bin/postgresqld'
  package Babushka.host.linux? ? 'postgresql-server' : 'postgresql'

  on :linux do
    meet {
      # TODO figure out better password generation
      require 'digest/hmac'
      password = Digest::HMAC.hexdigest((rand(10000) / (1 + rand(9))).to_s * rand(5), 'postgresql password', Digest::SHA256)

      log "Setting Mysql root password to: #{password}"
      shell "echo postgresql-server-5.5 postgresql-server/root_password password #{password} | sudo debconf-set-selections"
      shell "echo postgresql-server-5.5 postgresql-server/root_password_again password #{password} | sudo debconf-set-selections"
      File.write('/tmp/postgresql.root.password', password)
      if ppa
        log_shell "Adding PPA for #{package}: #{ppa}", "apt-add-repository -y #{ppa}", sudo: true
      end
      log_shell "Installing #{package}", "su -c 'export DEBIAN_FRONTEND=noninteractive; apt-get install -y #{package}'", sudo: true
    }
  end
end

dep 'postgresql.headers' do
  requires 'postgresql.installed'

  met?(on: :linux) {File.file?('/usr/include/postgresql/postgresql.h')}
  met?(on: :osx) {File.file?('/usr/local/include/postgresql.h')}
  meet(on: :linux) {shell('apt-get install -y libpostgresqlclient-dev', sudo: true)}
  meet(on: :osx) {log 'Should be installed by postgresql.installed'}
end

dep('postgresql.service') do
  requires('postgresql.installed')

  service Babushka.host.linux? ? 'postgresql' : 'homebrew.mxcl.postgresql'
end

dep 'postgresql' do
  requires 'postgresql.service'
end

dep 'removed postgresql root password' do
  def postgresql_root_password
    '/tmp/postgresql.root.password'.p
  end

  met? {!postgresql_root_password.exists?}

  meet do
    password = postgresql_root_password.read
    postgresql_root_password.unlink
    puts "Your POSTGRESQL root password is #{password}"
  end
end
