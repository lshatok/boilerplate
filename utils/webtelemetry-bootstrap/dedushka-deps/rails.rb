meta :rake do
  accepts_value_for :commands

  def rake(*commands)
    shell("./bin/rake #{commands.join(' ')} APP_ENV=#{env}")
  end

  template do
    meet {rake(commands)}
  end
end

dep 'bundler.gem' do
  provides 'bundle'
end
dep 'foreman.gem'
dep 'rubygems-bundler.gem' do
  provides []
end

dep 'binstubs regenerated.task' do
  requires 'rubygems-bundler.gem'
  run {shell('gem regenerate_binstubs')}
end

dep 'rails bundled', :root, :env, :user do
  requires 'bundler.gem'
  requires 'binstubs regenerated.task'

  met? do
    if (root / 'Gemfile').exists?
      shell? 'bundle check', cd: root, log: true
    else
      log 'No Gemfile - skipping bundling.'
      true
    end
  end

  meet do
    install_args = %w[development test].include?(env) ? '' : "--binstubs --deployment --without 'development test'"
    unless shell("cd #{root} && bundle install #{install_args} | grep -v '^Using '", log: true)
      confirm('Try a `bundle update`', default: 'n') do
        shell 'bundle update', log: true
      end
    end
  end
end

dep 'rails assets precompiled.rake', :env do
  commands %w(assets:precompile)

  met? {'public/assets'.p.exists?}
end

dep 'rails db migrated.rake', :env do
  commands %w(db:migrate)

  met? {rake('db:abort_if_pending_migrations')}
end

dep 'rails tmp dirs exists.rake', :env do
  commands %w(tmp:create)
  met? {'tmp'.p.exists?}
end

dep('config unicorn.rb.file', :app_name, :port, :worker_processes) do
  worker_processes.default(4)
  file_name(path / 'config' / 'unicorn.rb')
end

dep('config nginx.conf.file', :app_name, :domain, :port, :unsecure) do
  unsecure.choose('disable', 'redirect').default('redirect')
  file_name(path / 'config' / 'nginx.conf')
end

dep('.foreman.file', :app_name, :port) do
  requires 'foreman.gem'
  file_name('.foreman')
end

dep('.env.file', :env) do
  file_name('.env')
end

dep 'upstart.file', :app_name do
  requires 'foreman.gem'

  file_name "tmp/upstart/#{app_name}.conf"
  meet {shell('foreman export upstart tmp/upstart')}
end

dep 'app configured', :app_name, :path, :env, :port, :domain do
  requires 'config database.yml.file'.with(app_name: app_name, env: env)
  requires 'config unicorn.rb.file'.with(app_name: app_name, port: port)
  requires 'config nginx.conf.file'.with(app_name: app_name, domain: domain, port: port)
  requires '.foreman.file'.with(app_name: app_name, port: port)
  requires '.env.file'.with(env: env)
  requires 'upstart.file'.with(app_name)
end

dep('rails log dir exists') do
  met? {'log'.p.directory?}
  meet {shell('mkdir log')}
end

dep 'app install.bootstrap', :app_name, :prefix, :user, :group, :repo, :branch, :env, :port, :domain, :path do
  def reconfigure;
    @reconfigure ||= Babushka::Parameter.new('reconfigure').default!('false')
  end

  prefix.default!(File.dirname(File.expand_path('.')))

  setup {load_bootstrap_config}

  requires 'customize app profile.task'.with(env: env, rbenv_root: "/home/#{user}/.rbenv", prefix: prefix, app_name: app_name)
  requires 'customize git config'.with(user, domain)
  requires 'app installed'.with(path: path, user: user, repo: repo, branch: branch)
  requires 'rails bundled'.with(path, env, user)
  requires 'app configured'.with(app_name, path, env, port, domain)
  requires 'rails tmp dirs exists.rake'.with(env)
  requires 'rails log dir exists'
  requires 'rails db set up'.with(env)
  requires 'rails db migrated.rake'.with(env)
  requires 'rails assets precompiled.rake'.with(env)
  requires 'rails custom install'.with(env) if Dep('rails custom install')
end

dep 'rails update.bootstrap', :app_name, :prefix, :user, :group, :repo, :branch, :env, :port, :domain, :reconfigure, :path do
  setup {load_bootstrap_config}

  requires 'pull repo.task'
end
