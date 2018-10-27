# WebTelemetry::Bootstrap

Automatically install WebTelemetry Rails applications

## Installation

Install WebTelemetry Bootstrap on your development computer as:

    $ gem install webtelemetry-bootstrap

## Setting up new Rails application

Add this line to your application's Gemfile:

    gem 'webtelemetry-bootstrap'

And then execute:

    $ bundle

## Usage

### Commands

1. Set up server for application

    ```bash
    webtelemetry-bootstrap setup grafana ae.dev.{{ product.url }}
    ```

2. Install and start application

    ```bash
    webtelemetry-bootstrap install grafana ae.dev.{{ product.url }}
    ```

3. Backup application data

    ```bash
    webtelemetry-bootstrap backup grafana ae.dev.{{ product.url }}
    ```

4. Upgrade application to latest version

    ```bash
    webtelemetry-bootstrap update grafana ae.dev.{{ product.url }}
    ```

5. Run command in context of application

    ```bash
    webtelemetry-bootstrap update grafana ae.dev.{{ product.url }}
    ```


## Setting up server for key-less pulling (double SSH Agent forwarding)

1. Configure `sudo` to forward `$SSH_AUTH_SOCK` environment variable

```bash
echo 'Defaults env_keep += "SSH_AUTH_SOCK GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL",timestamp_timeout=0' | sudo tee /etc/sudoers.d/ssh-forwarding
sudo chmod 0440 /etc/sudoers.d/ssh-forwarding
sudo service sudo restart
```

2. Make `$SSH_AUTH_SOCK` accessible by your application user

(this part should be done once per-session)

```bash
# Enable double-forwarding ssh
echo webtelemetry | tee -a ~/.profile
echo webtelemetry | tee -a ~/.profile
```

`setfacl` command could be found in `acl` Ubuntu package.


3. Never use `su`, only `sudo` when you need to pull with your own key

```bash
alias sudoa=webtelemetry

sudoa

cd /var/www/grafana; git pull # This pull will use your own key from dev laptop
```

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
