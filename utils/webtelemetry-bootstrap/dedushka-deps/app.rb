# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WebTelemetry US Inc.             #
# Author: Yuri Lermonotov <ylermontov@webtelemetry.us>  #
########################################################

dep 'app installed', :path, :user, :repo, :branch do
  met? {File.directory?(path)}
  meet {shell("git clone #{repo} #{path} -b #{branch}", as: user)}
end

dep('available nginx.conf.symlink', :source, :destination)
dep('enabled nginx.conf.symlink', :source, :destination)
dep('config nginx.conf.symlinks', :domain, :path, :nginx_path) do
  on(:linux) {nginx_path.default!('/etc/nginx')}
  on(:osx) {nginx_path.default!('/usr/local/etc/nginx')}

  def nginx_source
    path / 'config' / 'nginx.conf'
  end

  def nginx_available
    nginx_path / 'sites-available' / domain
  end

  def nginx_enabled
    nginx_path / 'sites-enabled' / domain
  end

  requires 'available nginx.conf.symlink'.with(source: nginx_source, destination: nginx_available)
  requires 'enabled nginx.conf.symlink'.with(source: nginx_available, destination: nginx_enabled)
end

dep 'telemetrix' do
  requires 'nginx', 'postgresql', 'influxdb', 'redis'
end

dep 'startup scripts generated', :app_name do
  met? {"/etc/init/#{app_name}.conf".p.exists?}
  meet {shell("sudo mv tmp/upstart/#{app_name}* /etc/init/")}
end

dep('app.service', :app_name) do
  requires 'startup scripts generated'.with(app_name)
  service app_name
  upstart true
end

dep 'app pre-install.bootstrap', :app_name, :prefix, :user, :group, :repo, :branch, :env, :port, :domain, :reconfigure, :path do
  prefix.default('/WT')
  user.default('webtelemetry')
  group.default('wtuser')
  branch.default('master')
  env.default!('production').choose('production', 'staging', 'development', 'test')
  group.ask('Unix group')
  port.ask('Unicorn port')
  domain.ask('Main deployment domain')
  path.default!(ENV['APP_PATH'] || prefix / app_name)

  setup {load_bootstrap_config}

  requires 'telemetrix'
  requires 'postgresql.headers'
  requires 'customize ai profile'.with(rbenv_root: "/home/#{user}/.rbenv", prefix: prefix, app_name: app_name)
  requires 'custom app pre-install' if Dep('custom app pre-install')
  requires 'save.bootstrap'.with(app_name, prefix, user, group, repo, branch, env, port, domain, reconfigure, path)
end

dep 'app post-install.bootstrap', :app_name, :prefix, :user, :group, :repo, :branch, :env, :port, :domain, :reconfigure, :path do
  path.default!(ENV['APP_PATH'] || prefix / app_name)
  env.default!('production').choose('production', 'staging', 'development', 'test')

  requires 'config nginx.conf.symlinks'.with(path: path, domain: domain)
  requires 'removed postgresql root password'
  requires 'custom app post-install' if Dep('custom app post-install')

  requires 'nginx.service'
  requires 'influxdb.service'
  requires 'analytics.service'
  requires 'app.service'.with(app_name)
end
