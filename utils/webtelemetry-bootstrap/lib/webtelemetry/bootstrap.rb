# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WebTelemetry US Inc.             #
# Author: Yuri Lermonotov <ylermontov@webtelemetry.us>  #
########################################################

require 'webtelemetry/bootstrap/version'
require 'active_support'

module WebTelemetry
  module Bootstrap
    extend ActiveSupport::Autoload

    autoload :Deployment
    autoload :Common
    autoload :Main
    autoload :SSH
    autoload :Scripts

    def self.specification
      @specification ||= Gem.loaded_specs['webtelemetry-bootstrap']
    end

    def self.cached_gem
      if specification && specification.respond_to?(:cache_file)
        specification.cache_file
      else
        Gem.cache_gem('webtelemetry-bootstrap')
      end
    end

    def self.gem_file
      File.basename(cached_gem)
    end
  end
end
