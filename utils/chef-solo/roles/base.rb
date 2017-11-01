name "base"
description "base"

run_list(
  "recipe[apt]",
  "recipe[vim]",
  "recipe[webtelemetry::default]"
)
