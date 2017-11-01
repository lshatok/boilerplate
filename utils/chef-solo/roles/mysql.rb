name "postgresql"
description "postgresql"

run_list(
  "role[base]",
  "recipe[webtelemetry::postgresql_server]"
)
override_attributes(
  :postgresql => {
    :server_root_password => "abc123",
    :server_repl_password => "abc123",
    :server_debian_password => "abc123",
    :wtuser => webtelemetry,
    :{{product.smallname}} _password => "abc123"
}
)
