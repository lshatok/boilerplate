# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WebTelemetry US Inc.             #
# Author: Yuri Lermonotov <ylermontov@webtelemetry.us>  #
########################################################

dep 'nginx upstart.file' do
  path '/etc/init'
  file_name 'nginx.conf'

  def template_name
    "#{templates_path}/nginx.conf"
  end
end

dep 'nginx init.d removed' do
  met? {!('/etc/rc0.d/K20nginx'.p.file?)}
  meet {shell('update-rc.d -f nginx remove', sudo: true)}
end

dep 'nginx upstart', :source, :destination do
  requires 'nginx init.d removed'

  source.default! File.expand_path('../templates/nginx.conf', __FILE__)
  destination.default! '/etc/init/nginx.conf'

  met? {destination.p.exists?}
  meet {shell("cp #{source} #{destination}", sudo: true)}
end

dep 'nginx default site removed' do
  def default_nginx_site
    '/etc/nginx/sites-enabled/default'.p
  end

  met? {!default_nginx_site.file?}
  meet {shell("rm #{default_nginx_site}", sudo: true)}
end

dep('nginx.installed') do
  executable Babushka.host.linux? ? '/usr/sbin/nginx' : '/usr/local/bin/nginx'
  package 'nginx'
end

dep('nginx.service') do
  requires('nginx.installed')
  requires('nginx default site removed')
  requires('nginx upstart')

  service Babushka.host.linux? ? 'nginx' : 'homebrew.mxcl.nginx'
  upstart true

  met? {shell? "netstat -an | grep -E '^tcp.*[.:]80 +.*LISTEN'"}
end

dep 'nginx' do
  requires 'nginx.service'
end
