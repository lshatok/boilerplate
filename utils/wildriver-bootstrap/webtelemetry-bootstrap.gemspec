# coding: utf-8
lib = File.expand_path('../lib', __FILE__)
$LOAD_PATH.unshift(lib) unless $LOAD_PATH.include?(lib)
require 'webtelemetry/bootstrap/version'

Gem::Specification.new do |spec|
  spec.name = 'webtelemetry-bootstrap'
  spec.version = WebTelemetry::Bootstrap::VERSION
  spec.authors = ['Yuri Lermonotov']
  spec.email = %w(ylermontov@wildrivertechnologies.com)
  spec.description = %q{Automatically install and update WebTelemetry's applications}
  spec.summary = %q{WebTelemetry Bootstrap script}
  spec.homepage = 'https://github.com/ylermontov/webtelemetry-bootstrap'

  spec.files = `git ls-files`.split($/)
  spec.executables = spec.files.grep(%r{^bin/}) {|f| File.basename(f)}
  spec.test_files = spec.files.grep(%r{^(test|spec|features)/})
  spec.require_paths = %w(lib)

  spec.add_dependency 'thor'
  spec.add_dependency 'activesupport'

  spec.add_development_dependency 'bundler', '~> 1.3'
  spec.add_development_dependency 'rake'
  spec.add_development_dependency 'yard'
  spec.add_development_dependency 'redcarpet'
end
