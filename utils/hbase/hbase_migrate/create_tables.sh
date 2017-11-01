#!/usr/bin/env bash
create 'TELEMETRIX_temp_test', {NAME => 'actual', COMPRESSION => 'SNAPPY'}, {NAME => 'fcst', COMPRESSION => 'SNAPPY'}
create 'device_data_webtelemetry', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_cmcapital', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_cpi', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_rrd', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_equity', {NAME => 'actual'}
create 'device_data_equityoffice', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_hp', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_lockheedmartin', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_maxtest2', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_mtsac', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_parc', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_sap', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_test_tenant', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_tibco', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_uci', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_variant', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_yahoo', {NAME => 'actual'}
create 'fcst_webtelemetry', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_cmcapital', {NAME => 'current', COMPRESSION => 'SNAPPY', CONFIG => {'COMPRESSION_COMPACT' => 'SNAPPY'}}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY', CONFIG => {'COMPRESSION_COMPACT' => 'SNAPPY'}}
create 'fcst_cpi', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_rrd', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_equityoffice', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_hp', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_lockheedmartin', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_maxtest2', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_mtsac', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_parc', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_sap', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_test_tenant', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_tibco', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_uci', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_variant', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'test_table', {NAME => 'test', COMPRESSION => 'SNAPPY'}
create 'snmp_data', {NAME => 'actual', COMPRESSION => 'SNAPPY'}, {NAME => 'raw', COMPRESSION => 'SNAPPY'}


create 'device_data_cbre', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'device_data_palo-alto-city-hall', {NAME => 'actual', COMPRESSION => 'SNAPPY'}
create 'fcst_cbre', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}
create 'fcst_palo-alto-city-hall', {NAME => 'current', COMPRESSION => 'SNAPPY'}, {NAME => 'dayahead', COMPRESSION => 'SNAPPY'}