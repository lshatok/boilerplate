meta :git_config do
  accepts_value_for :key
  accepts_value_for :value

  def git_config
    @git_config ||= "/home/#{user}/.gitconfig".p
  end

  def name
    key.split('.', 2)[1]
  end

  template do
    met? {git_config.grep(/#{name}\s*=\s*[^\s]+\s*$/)}
    meet {shell("git config --global #{key} #{value}")}
  end
end

dep 'user name.git_config', :user, :domain do
  key 'user.name'
  value "WebTelemetry #{domain}"
end

dep 'user email.git_config', :user, :domain do
  key 'user.email'
  value "#{domain}@webtelemetry.us"
end

dep 'credentials helper.git_config', :user, :domain do
  key 'credential.helper'
  value 'cache'
end

dep 'customize git config', :user, :domain do
  requires 'user name.git_config'.with(user, domain)
  requires 'user email.git_config'.with(user, domain)
  requires 'credentials helper.git_config'.with(user, domain)
end
