# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WildRiver Technologies Inc             #
# Author: Yuri Lermonotov <ylermontov@wildrivertechnologies.com>  #
########################################################

require 'webtelemetry/bootstrap'
require 'webtelemetry/bootstrap/scripts'
require 'shellwords'

module WebTelemetry
  module Bootstrap
    class SSH
      include Common

      attr_accessor :deployment

      def run(script, options = {})
        script = Scripts.generate(script, deployment)
        ssh_command = "ssh #{sudo_user}@#{domain} -i #{private_key} -A -t"
        method = options[:method]
        invoke_method(method, ssh_command, script)
      end

      def invoke_method(method, ssh_command, script)
        if respond_to?(method)
          public_send(method, ssh_command, script)
        else
          raise "Unknown method #{self.class}##{method}"
        end
      end

      def dry_run(command, script)
        puts command
        puts script
      end

      def execute(command, script)
        if script
          script = Shellwords.escape(script)
        end
        system [command, script].compact.join(' -- ')
      end

      def app
        deployment
      end

      def teleport(options = {})
        source = Bootstrap.cached_gem
        ssh_command = "scp -i #{private_key} #{source} #{sudo_user}@#{domain}:#{File.basename(source)}"
        invoke_method(options[:method], ssh_command, nil)
      end

      def method_missing(name, *args, &block)
        if deployment.respond_to?(name)
          deployment.public_send(name, *args, &block)
        else
          super
        end
      end
    end
  end
end
