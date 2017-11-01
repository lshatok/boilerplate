# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WebTelemetry US Inc.             #
# Author: Yuri Lermonotov <ylermontov@webtelemetry.us>  #
########################################################

require 'webtelemetry/bootstrap'
require 'erb'

module WebTelemetry
  module Bootstrap
    module Scripts
      ROOT = File.expand_path('../scripts', __FILE__)

      module_function

      def generate(name, app)
        @app = app
        source = File.read(File.join(ROOT, "#{name}.erb"))
        ERB.new(source, 0, '<>%-').result(binding)
      end

      def render(name)
        generate("_#{name}", @app)
      end

      def bootstrap_source
        Bootstrap.specification.homepage
      end

      def bootstrap_gem

      end

      def babushka(command)
        "babushka #{command} #{verbose?}"
      end

      def verbose?
        '--debug' if Deployment.verbose
      end
    end
  end
end
