name "storm"
description "storm"

run_list(
  "role[base]",
  "recipe[webtelemetry::storm]"
)
