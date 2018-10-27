# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WildRiver Technologies Inc             #
# Author: Yuri Lermonotov <ylermontov@wildrivertechnologies.com>  #
########################################################

meta :installed do
  accepts_value_for :executable
  accepts_value_for :package
  accepts_value_for :ppa, nil

  template {
    if Babushka.host.linux?
      requires('apt')
    else
      requires('homebrew')
    end

    met? {
      File.executable?(executable)
    }

    meet on: :linux do
      if ppa
        log_shell "Adding PPA for #{package}: #{ppa}", "apt-add-repository -y #{ppa}", sudo: true
      end
      log_shell "Installing #{package}", "apt-get install -y #{package}", sudo: true
    end
    meet on: :osx do
      log_shell "Installing #{package}", "brew install #{package}"
    end
  }
end

meta :service do
  accepts_value_for :service
  accepts_value_for :running, /running/
  accepts_value_for :sudo, false
  accepts_value_for :upstart, false

  def process_exists?(process, match)
    shell("ps aux | grep #{process}").to_s.match(match)
  end

  template do
    on :linux do
      met? do
        if upstart
          shell?("sudo status #{service}").to_s.match(running)
        else
          shell("sudo service #{service} status").to_s.match(running)
        end
      end
      meet do
        if upstart
          log_shell("Starting service: #{service}", "sudo start #{service}")
        else
          log_shell("Starting service: #{service}", "sudo service #{service} start")
        end
      end
    end
    on :osx do
      met? do
        pid, status, _ = shell("launchctl list | grep #{service}").to_s.split(/\s+/, 3)
        pid.to_i > 0 || status == '1'
      end
      meet do
        shell("launchctl load #{'~' unless sudo}/Library/LaunchAgents/#{service}.plist", sudo: sudo)
        sleep 1
      end
    end
  end
end

meta :file do
  accepts_value_for :mode, '0644'
  accepts_value_for :file_name
  accepts_value_for :templates_path, 'templates'
  accepts_value_for :path, File.expand_path(Dir.pwd)
  accepts_value_for :user, ENV['USER']

  def basename
    File.basename(file_name)
  end

  def template_name
    "#{templates_path}/#{basename}.erb"
  end

  def dirname
    File.dirname(file_name)
  end

  def file_stat
    File.stat(file_name)
  end

  def file_exists?
    File.exists?(file_name).tap {|b| log("No #{basename} file") unless b}
  end

  def file_owned?
    (file_stat.uid == shell("id -u #{user}").chomp.to_i).tap {|b| log("#{basename} file doesn't belong to #{user} user") unless b}
    #(file_stat.gid == shell("id -g #{group}").chomp.to_i).tap { |b| log("#{basename} file doesn't belong to #{group} group") unless b }
  end

  def file_mode?
    (file_stat.mode.to_s(8)[2..-1] == mode).tap {|b| log("#{basename} file's mode is not #{mode}") unless b}
  end

  def check_file?
    file_exists? && file_owned? && file_mode?
  end

  def generate_file
    render_erb template_name, to: file_name
    chown_chmod_file! unless user.to_s == ENV['USER']
  end

  def chown_chmod_file!
    shell("chown #{user}:#{group} #{file_name}", sudo: true)
    shell("chmod #{mode} #{file_name}", sudo: true)
  end

  template do
    met? {check_file?}
    meet {generate_file}
  end
end

meta :symlink do
  template do
    met? do
      File.symlink?(destination).tap {|b| log("File #{destination} does not exists") unless b} &&
        (File.readlink(destination) == source.to_s).tap {|b| log("File #{destination} is not linked to #{source}") unless b} &&
        File.exists?(source).tap {|b| log("File #{source} does not exists") unless b}
    end

    meet do
      shell("rm #{destination}", sudo: true) if File.exists?(destination)
      shell("ln -s #{source} #{destination}", sudo: true)
    end
  end
end
