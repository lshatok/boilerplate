# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WildRiver Technologies Inc             #
# Author: Yuri Lermonotov <ylermontov@wildrivertechnologies.com>  #
########################################################

require 'webtelemetry/bootstrap'
require 'active_support/core_ext/class/attribute'

module WebTelemetry
  module Bootstrap
    class Deployment
      include Common

      class_attribute :github_user
      class_attribute :verbose

      APP_NAMES={
        'grafana' => 'webtelemetry',
        'webtelemetry-selena2' => 'mirwais',
        'webtelemetry-sep2' => 'sep2',
      }

      # @return [String]
      attr_accessor :name

      def app_name
        APP_NAMES[name]
      end

      # @return [String]
      attr_accessor :branch

      # @return [String]
      attr_accessor :domain

      # @return [String]
      attr_accessor :app_user

      # @return [String]
      attr_accessor :sudo_user

      # @return [String]
      attr_accessor :private_key

      # @return [String]
      attr_accessor :prefix

      # @return [String]
      attr_accessor :common_group

      # @return [Boolean]
      attr_accessor :configure

      # @return [String]
      attr_accessor :invoke_command

      attr_accessor :subdirectory

      # @return [Integer]
      attr_accessor :port

      # @return [String]
      def git_repo
        @git_repo ||= "git@github.com:#{github_user}/#{name}.git"
      end

      attr_writer :git_repo

      # @return [String]
      def https_repo
        @https_repo ||= "https://github.com/#{github_user}/#{name}"
      end

      attr_writer :https_repo

      def bootstrap_gem
        Bootstrap.gem_file
      end
    end
  end
end
