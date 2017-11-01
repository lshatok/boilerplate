name "influxdb"
description "influxdb"

run_list(
  "role[base]",
  "recipe[webtelemetry::influxdb_server]"
)

override_attributes(
  :influxdb => {
    :use_distro_version => true
  }
)
