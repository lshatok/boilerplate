dep('config database.yml.file',
    :app_name, :env,
    :adapter, :encoding, :reconnect, :pool, :socket,
    :database, :username, :password, :host) do
  require 'yaml'
  require 'tempfile'

  host.ask('DB host')
  database.ask('DB name')
  username.ask('DB user')
  password.ask('DB user password')
  adapter.default!('postgresql2')
  encoding.default!('utf8')
  reconnect.default!('false')
  pool.default(5)

  on(:linux) {socket.default('/var/run/postgresqld/postgresqld.sock')}
  on(:osx) {socket.default('/tmp/postgresql.sock')}

  file_name('config' / 'database.yml')

  def database_config
    YAML.load_file(file_name) || {}
  rescue
    {}
  end

  met? do
    file_present = check_file?
    file_basename = File.basename(file_name)
    if file_present
      config = database_config
      config_present = !!config[env.to_s]
      log("#{env} is not configured in #{file_basename}") unless config_present
    end
    file_present && config_present
  end

  meet do
    config = database_config
    env_conf = config[env.to_s] ||= {}
    env_conf['adapter'] = adapter.to_s
    env_conf['host'] = host.default(env_conf['host'] || 'localhost').to_s
    env_conf['database'] = database.default(env_conf['database'] || "#{app_name}_#{env}").to_s
    env_conf['username'] = username.default(env_conf['username'] || app_name).to_s
    env_conf['password'] = password.default(env_conf['password'] || '').to_s
    env_conf['encoding'] = encoding.to_s
    env_conf['reconnect'] = reconnect.to_s
    env_conf['pool'] = pool.to_s.to_i
    env_conf['socket'] = socket.to_s
    File.write(file_name, config.to_yaml)
  end
end

dep 'rails db set up', :env do
  env.default(ENV['APP_ENV'] || ENV['RACK_ENV'] || 'production')

  requires 'config database.yml.file'.with(env: env)

  def root_password
    @root_password ||= begin
      postgresql_root_password = '/tmp/postgresql.root.password'.p
      password = postgresql_root_password.read if postgresql_root_password.file?
      unless password
        password = Babushka::Prompt.prompt_and_read_value('POSTGRESQL root password', ask: true, prompt: '')
      end
      password
    end
  end

  met? do
    config = YAML.load_file('config/database.yml')[env.to_s]
    shell?("postgresql --user #{config['username']} --password='#{config['password']}' -h #{config['host'] || 'localhost'} #{config['database']}")
  end

  meet do
    shell("echo #{root_password} | ./bin/rake db:setup APP_ENV=#{env}")
  end
end
