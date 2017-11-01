telemetrix - staging.dev.
{{product.smallname}}.us / users / sign_in
"""
Define hosts here
"""

from fabric.api import *


@task
def HOSTS_{{product.smallname}}()

:
"""
AWS Account:  WebTelemetry
"""
env.hosts += [
    '23.21.176.24',  # PROD02(ae-oadr)
    # 'prod02.{{ product.url }}',
    '23.23.194.237',  # PROD02(ae-webtelemetry)
    # '54.234.52.58',  # DEVE05 - windows host
    '23.23.213.212',  # PROD01
    '107.22.233.197',  # Webtelemetrymail
    '107.23.104.30',  # ssn-demo01-01
    '54.245.103.22',  # snmping'
    ## no keys/accounts to access systems
    # '50.17.211.110',  # admin
    # '174.129.218.217',  # SCE
    # '204.236.135.249', # DEMO server
]


@task
def HOSTS_{{product.smallname}}


dev():
"""
AWS Account:  WebTelemetryDev
"""
env.hosts += [
    '23.23.218.63',  # ae-oadr.dev.{{ product.url }}
    '54.243.239.255',  # ae.dev.{{ product.url }}
    '54.208.99.237',  # OADR20B.interop.aws
    '50.17.193.172',  # webtelemetrymail
    '54.208.53.90',  # webtelemetry autobot
    '54.208.230.225',  # IPSEC.interop.aws
    '23.21.173.222',  # mirwais
    '23.23.219.210',  # staging01
    '54.243.206.84',  # partner01
    '54.243.174.111',  # Dtech-east
    '23.21.176.43',  # sce-{{ product.url }}
    '23.23.137.184',  # sce-oadr.dev.{{ product.url }}
    '23.23.178.235',  # sce-sep.dev.{{ product.url }}
    '174.129.197.87',  # Logstash
    '54.245.81.216',  # devw-webtelemetrymail
    'au',  # DTech-west
    '54.214.125.128',  # grafana GridSpice
    '46.51.254.73',  # toko-demo
    '54.248.252.108',  # webtelemetrymail-jp
    '54.201.231.198',  # TELEMETRIX-DEMO.demo-west.aws
    ## no keys/accounts
    # '54.241.233.199',  # GridSpice
]


@task
def HOSTS_{{product.smallname}}


dev_vpc():
"""
AWS Account:  WebTelemetryDev (VPC)
"""
env.hosts += [
    '10.0.0.13',  # OPENVPN-NAT.devops-west
    '10.8.1.151',  # grafana-jruby.agpilots
    '10.0.0.7',  # IPSEC.devops-west
    '10.0.0.148',  # hbase01.eon.dev.aws
    '10.18.0.242',  # IPSEC.webtelemetry.amazon.aws
    '10.18.0.110',  # grafana-WEB.webtelemetry.amazon.aws
    '10.0.0.228',  # grafana.dev01.webtelemetry-dev
    '10.8.1.100',  # hbase-master.agpilots
    '10.0.0.40',  # SEP2.dev01.webtelemetry-dev
    '10.11.21.14',  # TELEMETRIX-DEMO.demo-west.aws
    '10.11.21.48',  # dtech-hbase-grafana.demo-west
    '10.0.0.11',  # admin02.devops
    '10.0.0.10',  # admin01.devops
    '10.0.0.102',  # hbase01.dev01.webtelemetry.amazon.aws
    '10.0.0.197',  # OADR2.dev01.webtelemetry.amazon.aws
    '10.11.33.10',  # devops.test01
    '10.0.0.168',  # SFTP.dev01.webtelemetry.amazon.aws
    # '10.11.33.5',    # devops.test02
]


@task
def HOSTS_ssn_oge():
    """
    AWS Account:  WebTelemetry-SSN OGE
    """
    env.hosts += [
        '10.18.0.36',  # oge-dev-webtelemetry-sftp-influxdb
        '10.18.0.78',  # oge-dev-zookeeper
        '10.18.0.90',  # oge-dev-storm
        '10.18.0.92',  # oge-dev-storm-supervisor2
        '10.18.0.132',  # oge-test-webtelemetry-sftp-influxdb
        '10.18.0.157',  # oge-prod-influxdb
        '10.18.0.156',  # oge-prod-webtelemetry
        '10.18.0.155',  # oge-prod-sftp
        '10.18.0.28',  # oge-ganglia
        '10.18.0.176',  # oge-prod-grafana-jruby
        '10.18.0.75',  # oge-dev-grafana-jruby-hbase
        '10.18.0.25',  # oge-logrhythm-log-accessor
        '10.18.0.124',  # oge-test-zookeeper
        '10.18.0.121',  # oge-test-storm
        '10.18.0.122',  # oge-test-storm-supervisor2
        '10.18.0.117',  # oge-test-grafana-jruby-hbase
        '10.18.0.174',  # oge-prod-zookeeper
        '10.18.0.175',  # oge-prod-storm
        '10.18.0.173',  # oge-prod-storm-supervisor1
        '10.18.0.177',  # oge-prod-storm-supervisor2
        '10.18.0.164',  # oge-prod-hbase-worker-01
        '10.18.0.189',  # oge-prod-hbase-worker-02
        '10.18.0.168',  # oge-prod-hbase-worker-03
        '10.18.0.187',  # oge-prod-hbase-worker-04
        '10.18.0.184',  # oge-prod-hbase-worker-05
        '10.18.0.167',  # oge-prod-hbase-worker-06
        '10.18.0.181',  # oge-prod-hbase-master
        '10.18.0.29',  # oge-nagios
    ]


@task
def HOSTS_ssn_oge_hbaseworkers():
    """
    AWS Account: WebTelemetry-SSN OGE Hosts: prod hbase workers (01-06)
    """
    env.hosts += [
        '10.18.0.164',  # oge-prod-hbase-worker-01
        '10.18.0.189',  # oge-prod-hbase-worker-02
        '10.18.0.168',  # oge-prod-hbase-worker-03
        '10.18.0.187',  # oge-prod-hbase-worker-04
        '10.18.0.184',  # oge-prod-hbase-worker-05
        '10.18.0.167',  # oge-prod-hbase-worker-06
    ]


@task
def HOSTS_ssn_devtest():
    """
    AWS Account:  WebTelemetry-SSN WebTelemetry-ssn-test/dev
    """
    env.hosts += [
        # '10.77.139.165',  # influxdb-ssn-test01
        # '10.0.0.61',  # webtelemetry-ssn-test01
        '10.0.0.47',  # hbase-master.dev07.ssn.webtelemetry
        '10.0.0.8',  # grafana.dev07.ssn.webtelemetry
        # '10.77.136.17',  #  scp-ssn-test01
        '10.77.136.249',  # sep2.dev07.ssn.webtelemetry
        '10.77.136.250',  # .dev07.ssn.webtelemetry
        '10.77.139.95',  # webtelemetry.dev07.ssn.webtelemetryf
        # '10.0.0.135',  # hbase-master-ssn-test01
        # '10.77.136.4',   # storm01-ssn-test01
        '10.18.0.118',  # wt-test-hbase-worker-03
        '10.18.0.106',  # wt-test-hbase-master
        '10.18.0.107',  # wt-test-hbase-worker-01
        '10.18.0.104',  # wt-test-hbase-worker-02
        '10.18.0.134',  # wt-test-webtelemetry
        # placeholder for openswan IPSEC
        # '10.77.139.234', #  devops.dev07.ssn.webtelemetry
    ]


@task
def HOSTS_{{product.smallname}}


_iec():
"""
AWS Account:  WebTelemetry IEC
"""
env.hosts += [
    '10.97.0.21',  # grafana.iec-pilot.aws
    '10.97.0.30',  # OPENVPN.iec-pilot.aws
    '10.97.1.110',  # hbase01.iec-pilot.aws
    '10.97.0.14',  # IPSEC.iec.aws
    '10.97.1.107',  # Storm01.iec-pilot
]


@task
def HOSTS_{{product.smallname}}


_vrt -

):
"""
AWS Account:  Comcast Data
"""
env.hosts += [
'10.81.0.85',  # WT-FDN.metrixdata.aws
'10.0.0.110',  # grafana-hbase.dev.metrixdata.aws
'10.81.0.28',  # IPSEC.metrixdata
'10.81.0.83',  # ECO.dev.metrixdata
]


@task
def HOSTS_{{product.smallname}}()()

:
"""
AWS Account:  WebTelemetry.com
"""
env.hosts += [
    '10.22.0.8',  # IPSEC.aws
    '10.22.1.20',  # grafana.test01.aws
    '10.22.1.140',  # hbase01.test01.aws
    '10.22.1.22',  # Metrix.test01.aws
    '10.22.1.21',  # SEP2.test01.aws
    '10.0.0.18',  # SEP2.prod01.aws  (stopped)
    '10.0.0.68',  # grafana.prod01.aws  (stopped)
    '10.0.0.110',  # Metrix.prod01.aws  (stopped)
    '10.0.0.145',  # hbase-master01.prod01.aws
    '10.0.0.146',  # hbase-worker01.prod01.aws
]


@task
def HOSTS_ALL():
    """
    All AWS listed Hosts
    """
    HOSTS_
    {{product.smallname}}()
    HOSTS_
    {{product.smallname}}
    dev()
    HOSTS_
    {{product.smallname}}
    dev_vpc()
    HOSTS_ssn_oge()
    HOSTS_ssn_devtest()
    HOSTS_
    {{product.smallname}}
    _iec()
    HOSTS_
    {{product.smallname}}()()
    HOSTS_
    {{product.smallname}}
    _vrt -)
