# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WildRiver Technologies Inc             #
# Author: Yuri Lermonotov <ylermontov@wildrivertechnologies.com>  #
########################################################

require 'webtelemetry/bootstrap'
require 'webtelemetry/bootstrap/deployment'
require 'thor'
require 'active_support/core_ext/hash/except'

module WebTelemetry
  module Bootstrap
    class Main < Thor
      class_option :github_user, default: 'webtelemetry'
      class_option :sudo_user, default: 'ubuntu'
      class_option :app_user, default: 'webtelemetry'
      class_option :common_group, default: 'wtuser'
      class_option :private_key, default: '~/.ssh/id_rsa'
      class_option :dry_run, type: :boolean, default: false
      class_option :prefix, default: '/WT'
      class_option :subdirectory
      class_option :configure, type: :boolean, default: false
      class_option :verbose, type: :boolean, default: false

      desc 'setup APP DOMAIN', 'Set up prerequisites for APP on DOMAIN'
      method_option :branch, default: 'master'

      def setup(app, domain)
        defaults(app, domain)

        ssh.run('setup.sh', method: execution_method)
      end

      desc 'install APP DOMAIN', 'Install application APP on DOMAIN'
      method_option :branch, default: 'master'

      def install(app, domain)
        defaults(app, domain)

        ssh.run('install.sh', method: execution_method)
      end

      desc 'update APP DOMAIN', 'Update application APP on DOMAIN'
      method_option :branch, default: 'master'

      def update(app, domain)
        defaults(app, domain)

        ssh.run('update.sh', method: execution_method)
      end

      desc 'command APP DOMAIN COMMAND', 'Run command COMMAND in context of APP on DOMAIN'

      def command(app, domain, command)
        defaults(app, domain)

        deployment.invoke_command = command

        ssh.run('command.sh', method: execution_method)
      end

      private

      def execution_method
        options[:dry_run] ? :dry_run : :execute
      end

      attr_reader :ssh

      def defaults(app, domain)
        Deployment.github_user = options[:github_user]
        Deployment.verbose = options[:verbose]

        options = self.options.dup.except(:dry_run)
        if domain =~ /@/
          options[:sudo_user], domain = domain.split(/@/, 2)
        end
        options[:name] = app
        options[:domain] = domain
        case app
          when 'webtelemetry_selena'
            options[:port] = 9876
          when 'webtelemetry_sep2'
            options[:port] = 9874
          when 'grafana'
            options[:port] = 4200
          when 'telemetrix'
            options[:port] = 4100
            options[:subdirectory] = '/ruby'
          else
            options[:port] = 3000
        end

        @deployment = Deployment.new(options)
        @ssh = SSH.new(deployment: @deployment)
        teleport
      end

      def teleport
        ssh.teleport(method: execution_method)
      end
    end
  end
end
