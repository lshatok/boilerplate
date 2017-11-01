meta :bootstrap do
  def bootstrap_config
    path / 'config' / 'settings' / 'bootstrap.local.yml'
  end

  def bootstrap_config?
    File.exists?(bootstrap_config)
  end

  def config_updated?
    bootstrap_config? && reconfigure.to_s == 'false' || $bootstrap_configured #File.stat(bootstrap_config).mtime < $bootstrap_started
  end

  def saved_params
    %w(app_name prefix user group repo branch env port domain)
  end

  def load_bootstrap_config
    $bootstrap_started = Time.now
    if bootstrap_config?
      require 'yaml'
      params = YAML.load_file(bootstrap_config)
      params.each do |name, value|
        if respond_to?(name)
          if reconfigure.to_s == 'true'
            send(name).default(value)
          else
            send(name).default!(value)
          end
        end
      end
      reconfigure.default!('false')
    else
      reconfigure.default!('true')
    end

    if reconfigure.to_s == 'true'
      saved_params.each {|name| send(name).to_s}
    end
  end
end

dep 'save.bootstrap', :app_name, :prefix, :user, :group, :repo, :branch, :env, :port, :domain, :reconfigure, :path do
  met? {config_updated?}
  meet do
    require 'yaml'
    require 'tempfile'
    config = {}.tap do |config|
      saved_params.each do |name|
        config[name] = send(name).to_s
      end
    end
    Tempfile.open('bootstrap.local.yml') do |file|
      file.write(config.to_yaml)
      file.flush
      shell("mv #{file.path} #{bootstrap_config}", sudo: true)
      shell("chown #{user}:#{group} #{bootstrap_config}", sudo: true)
      shell("chmod ug+rw #{bootstrap_config}", sudo: true)
      file.close
    end
    reconfigure.default!('false')
    $bootstrap_configured = true
  end
end
