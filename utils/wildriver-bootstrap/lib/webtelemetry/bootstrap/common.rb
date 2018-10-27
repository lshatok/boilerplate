# coding: utf-8

########################################################
# Copyright (c) 2013—2017 WildRiver Technologies Inc             #
# Author: Yuri Lermonotov <ylermontov@wildrivertechnologies.com>  #
########################################################

require 'webtelemetry/bootstrap'

module WebTelemetry
  module Bootstrap
    module Common
      def initialize(attributes = {})
        assign_attributes(attributes)
      end

      def assign_attributes(attributes)
        @attributes ||= {}
        attributes.each do |name, value|
          writer = "#{name}="
          if respond_to?(writer)
            public_send(writer, value)
          else
            @attributes[name] = value
            STDERR.puts "#{self.class.name}##{writer} is not implemented"
          end
        end
      end
    end
  end
end
