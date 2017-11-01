base_dir = File.expand_path(File.dirname(__FILE__) + "/..")
cookbook_path ["#{base_dir}/cookbooks"]
role_path ["#{base_dir}/roles"]
data_bag_path ["#{base_dir}/data_bags"]
