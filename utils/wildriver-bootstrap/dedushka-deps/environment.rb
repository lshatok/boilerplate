meta :append do
  accepts_value_for :file
  accepts_value_for :line

  def file_name
    File.expand_path(file)
  end

  def file_contents
    File.readlines(file_name)
  end

  def append_file!
    File.write(file_name, (file_contents << "#{line}\n").join(''))
  end

  template do
    met? {file_contents.any? {|file_line| file_line =~ /#{Regexp.escape(line)}/}}
    meet {append_file!}
  end
end

dep 'rbenv PATH.append', :profile, :rbenv_root do
  rbenv_root.default(File.expand_path('~/.rbenv'))
  file profile
  line %'export PATH="#{rbenv_root}/bin:$PATH"'
end

dep 'rbenv init.append', :profile do
  file profile
  line 'eval "$(rbenv init -)"'
end

dep 'rbenv configured', :profile, :rbenv_root do
  requires 'rbenv PATH.append'.with(profile, rbenv_root)
  requires 'rbenv init.append'.with(profile)
end

dep 'sudo webtelemetry alias.append', :profile do
  file profile
  line 'alias sudoa="sudo -iu webtelemetry"'
end

dep 'APP_ENV.append', :profile, :env do
  file profile
  line 'alias sudoa="sudo -iu webtelemetry"'
end

dep 'less ANSI.append', :profile do
  file profile
  line 'alias less="less -R"'
end

dep 'load bashrc.append', :profile do
  file profile
  line '[[ -f ~/.bashrc ]] && . ~/.bashrc'
end

dep 'WT_ROOT.append', :profile, :applications_root do
  applications_root.default('/WT')

  file profile
  line %'export WT_ROOT="#{applications_root}"'
end

dep 'cd dw.append', :profile, :app_name do
  app_name.default!('grafana')

  file profile
  line %'alias cddw="cd $WT_ROOT/#{app_name}"'
end

dep 'binstubs PATH.append', :profile do
  file profile
  line 'export PATH="bin:$PATH"'
end

dep 'customize ai profile', :profile, :env, :rbenv_root, :prefix, :app_name do
  on(:linux) {profile.default!('~/.profile')}
  on(:osx) {profile.default!('~/.bash_profile')}

  rbenv_root.default('/WT/.rbenv')

  requires 'load bashrc.append'.with(profile)
  requires 'rbenv PATH.append'.with(profile, rbenv_root)
  requires 'rbenv init.append'.with(profile)
  requires 'less ANSI.append'.with(profile)
  requires 'sudo webtelemetry alias.append'.with(profile)
  requires 'APP_ENV.append'.with(profile, env)
  requires 'WT_ROOT.append'.with(profile, prefix)
  requires 'cd dw.append'.with(profile, app_name)
  requires 'binstubs PATH.append'.with(profile)
end

dep 'customize app profile.task', :profile, :env, :rbenv_root, :prefix, :app_name do
  on(:linux) {profile.default!('~/.profile')}
  on(:osx) {profile.default!('~/.bash_profile')}

  app_name.default!(File.basename(File.expand_path('.')))
  rbenv_root.default!(File.expand_path('~/.rbenv'))

  env.default(ENV['APP_ENV'] || ENV['RACK_ENV'] || 'production')

  requires 'load bashrc.append'.with(profile)
  requires 'rbenv PATH.append'.with(profile, rbenv_root)
  requires 'rbenv init.append'.with(profile)
  requires 'less ANSI.append'.with(profile)
  requires 'APP_ENV.append'.with(profile, env)
  requires 'WT_ROOT.append'.with(profile, prefix)
  requires 'cd dw.append'.with(profile, app_name)
  requires 'binstubs PATH.append'.with(profile)
end
