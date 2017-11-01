*******************************
* CITTIO SNMP Agent for Linux *
*******************************

------------------------------------------------------------------------------
Copyright(c) 2006, CITTIO, Inc. (www.cittio.com)
Product names used in this document are trademarks of their respective owners.
------------------------------------------------------------------------------


I.  README.TXT CONTENTS
=================================
 1)  INTRODUCTION
 2)  LIMITED WARRANTY
 3)  GENERAL
 4)  SUPPORT
 5)  STANDARDS
 6)  WATCHTOWER



1.  INTRODUCTION
=================================
Thank you for using (or trying) the CITTIO, Inc. SNMP Agent for Linux
distributions.

This SNMP Agent for Linux operating systems is a software program built on
the industry standard Net-SNMP Agent along with AgentX extensions.  This
"agent" provides low level hardware statistics, OS level information, and
application performance and operational data to any SNMPv1, SNMPv2c & SNMPv3
compliant network management system (NMS) such as WatchTower.

The CITTIO SNMP Agent should be installed on Linux servers, which an
administrator wishes to monitor, using any SNMP tool (e.g. walk utility) or
NMS application.  Thus, the statistics provided by this SNMP agent allows
administrators to proactively monitor their Linux infrastructure and plan
for capacity peaks based on real metrics.

NOTE:  This SNMP Agent is an extension of the Net-SNMP AgentX framework and
       packaged as a bunch of executables along with supporting Shared Objects
       (.SO's) and configuration files.  The CITTIO SNMP Agent does not
       require any master SNMP agent to be installed prior to installing this
       SNMP Agent.


2.  LIMITED WARRANTY
=================================
Please refer to the License text file, which has also been installed in this
CITTIO SNMP Agent bundle.


3.  GENERAL
=================================
Should you have any questions concerning our product suite, its capabilities,
or require any marketing literature or technical specifications, please
contact CITTIO Sales at sales@cittio.com.


4.  SUPPORT
=================================
A few important facts to consider:
 1)  The CITTIO SNMP Agent must be compiled & built natively for a particular
     Linux distribution.  CITTIO has taken care to build support & test our
     CITTIO SNMP Agent on ONLY the following flavors & version of Linux:

       - RedHat Enterprise Linux 3.0/4.0/5.0
       - SuSE Enterprise Linux 10
     
     Added support for other flavors & versions of Linux will be added over
     time.  Please check with CITTIO Technical Support for details of the
     latest Agent releases available for your use.

 2)  The CITTIO SNMP Agent is NOT a Linux product and is NOT supported by
     any of the major vendors (i.e. RedHat, SuSE, Debian, etc.)  However, we
     leverage the open-source Net-SNMP Agent project & provide support in
     accordance to the license agreement found in this install.

To restart the CITTIO SNMP Agents, run the following at any command
line prompt:

    /etc/init.d/snmpd restart

Should you have any questions concerning this SNMP Agent and you have PAID for
technical product support, please contact CITTIO, Inc. by sending an e-mail to
support@cittio.com.  Please include:
 A.  Your customer ID
 B.  Organizational contact information (name, email, phone)
 C.  A brief description of the problem

You are also advised to check the CITTIO Knowledge Base for solutions and/or
TANs which have been posted on our Technical Support website.


5.  STANDARDS
=================================
The CITTIO SNMP Agent is written to comply with RFC standards, and has been
compiled and tested on several different MIB compilers.  CITTIO has also taken
best efforts to test data collection against Linux/UNIX applications in order
to ensure maximum compatibility.  Nonetheless, CITTIO makes NO guarantees to
work with any other NMS product other than with WatchTower.


6.  WATCHTOWER
=================================
CITTIO's flagship product WatchTower is an enterprise monitoring & management
software application which enables companies to increase IT productivity,
efficiently manage distributed systems, reduce downtime, and generate business
value from the network.  WatchTower is deeply integrated and optimized to work
with the CITTIO SNMP Agent for Linux.  Please contact sales@cittio.com if you
are interested in seeing how WatchTower can help your organization.

Thank you very much for your download, time and business!!!

Sincerely,
CITTIO, Inc.

