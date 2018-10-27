################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_tomcat

    tomcat {install_tomcat}
    tomcat_restart
"""
from fabric.api import *

UPSTART_CONF = """
description "Tomcat Server"

    start on runlevel [2345]
    stop on runlevel [!2345]
    respawn
    respawn limit 10 5

    # run as non privileged user
    setuid wtuser
    setgid {{ product.admin }}

    # adapt paths:
    env JAVA_HOME="{{ java.home }}"
    env CATALINA_HOME=/WT/appserver

    # adapt java options to suit your needs:
    env JAVA_OPTS="-Djava.awt.headless=true -Xms512M -Xmx1024M -server -XX:+UseParallelGC"
    # used for snmp:
    #env JAVA_OPTS="-Dfile.encoding=UTF-8 -server -Xms512m -Xmx1024m -XX:NewSize=256m -XX:MaxNewSize=256m -XX:PermSize=256m -XX:MaxPermSize=256m -XX:+DisableExplicitGC"

    exec $CATALINA_HOME/bin/catalina.sh run

    # cleanup temp directory after stop
    post-stop script
    rm -rf $CATALINA_HOME/temp/*
    end script
"""


def install_tomcat():
    """
    TASK:tomcat - install tomcat from apache
    """
    tomcat_ver = 'apache-tomcat-7.0.47.tar.gz'
    unzipped_ver = 'apache-tomcat-7.0.47'
    tomcat_url = \
        'https://s3-us-west-2.amazonaws.com/com.webtelemetry().software-repo.public/apache-tomcat/%s' % tomcat_ver
    tomcat_user = 'webtelemetry'
    tomcat_group = '{{ product.admin }}'
    tomcat_path = '/WT'
    sudo('chown %s:%s %s' % (tomcat_user, tomcat_group, tomcat_path))
    print "task:  tomcat install"
    if 'no' == sudo('[ -d %s/%s ] || echo "no"' % (tomcat_path, unzipped_ver)):
        sudo('[ -d %s ] || mkdir -p %s' % (tomcat_path, tomcat_path))
        with cd(tomcat_path):
            print "   downloading install files"
            sudo('wget %s' % tomcat_url, user=tomcat_user)
            sudo('tar zxf %s && rm %s' % (tomcat_ver, tomcat_ver), user=tomcat_user)
            sudo('ln -s %s apache-tomcat' % unzipped_ver, user=tomcat_user)
            # update configs #
            print "   updating configs and logging properties"
            sudo("""sed -i 's/prefix="localhost_access_log." suffix=".txt"/prefix="localhost_access_log" \
                    suffix=".log" rotatable="false"/' apache-tomcat/conf/server.xml""", user=tomcat_user)
            sudo("""sed -i '/1catalina.org.apache.juli.FileHandler.prefix = catalina/a \
                    1catalina.org.apache.juli.FileHandler.rotatable = false' apache-tomcat/conf/logging.properties""",
                 user=tomcat_user)
            sudo("""sed -i '/2localhost.org.apache.juli.FileHandler.prefix = localhost/a \
                    2localhost.org.apache.juli.FileHandler.rotatable = false' apache-tomcat/conf/logging.properties""",
                 user=tomcat_user)
            sudo("""sed -i '/3manager.org.apache.juli.FileHandler.prefix = manager/a \
                    3manager.org.apache.juli.FileHandler.rotatable = false' apache-tomcat/conf/logging.properties""",
                 user=tomcat_user)
            sudo("""sed -i '/4host-manager.org.apache.juli.FileHandler.prefix = host-manager/a \
                    4host-manager.org.apache.juli.FileHandler.rotatable = false' apache-tomcat/conf/logging.properties""",
                 user=tomcat_user)
            sudo("""sed -i '/5production.org.apache.juli.FileHandler.prefix = production/a \
                    5production.org.apache.juli.FileHandler.rotatable = false' apache-tomcat/conf/logging.properties""",
                 user=tomcat_user)
    else:
        print "   skipping: tomcat path %s/%s already exists." % (tomcat_path, unzipped_ver)
    # add upstart conf file #
    if 'no' == sudo('[ -f /etc/init/tomcat.conf ] || echo "no"'):
        print "   adding tomcat upstart file"
        sudo("cat << 'EOF' >> /etc/init/tomcat.conf\n%s\nEOF" % UPSTART_CONF)
    print "   restarting tomcat service"
    sudo('service tomcat restart')


def tomcat_restart():
    """
    TASK:tomcat_restart - service tomcat restart
    """
    sudo('service tomcat restart')
