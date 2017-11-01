name "redis"
description "redis"

run_list(
  "role[base]",
  "recipe[webtelemetry::data_collector]"
)

override_attributes(
  :redis => {
    :daemonize => "yes"
  }
)
