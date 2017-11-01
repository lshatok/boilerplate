cat 2buttons.my | while read line
  do

name=`echo $line | cut -d"," -f1`
mytxt=`echo $line | cut -d"," -f2`

 #random http proxy 1-21 line
  proxy_number=$[ ( $RANDOM % 21 ) + 1 ];
  use_proxy=`awk -v r=$proxy_number ' NR==r {print} ' proxy.list`;



# curl http://dabuttonfactory.com/button.gif?t\=Acknowledge&f\=Open+Sans-Bold&ts\=14&tc\=fff&hp\=22&vp\=2&c=5&bgt=unicolored&bgc=81959d

# wget -O $name "http://dabuttonfactory.com/button.gif?t=$mytxt&f=Open+Sans-Bold&ts=14&tc=fff&hp=22&vp=2&c=5&bgt=unicolored&bgc=81959d"

# New Blue
# wget -O $name "http://dabuttonfactory.com/button.gif?t=$mytxt&f=Open+Sans-Bold&ts=14&tc=fff&hp=22&vp=2&c=5&bgt=unicolored&bgc=19485b"

# Rust Orange
# wget -O $name "http://dabuttonfactory.com/button.gif?t=$mytxt&f=Open+Sans-Bold&ts=14&tc=fff&hp=22&vp=2&c=5&bgt=unicolored&bgc=cc6600 "

# SEGA MASTER SYSTEM
wget -O $name "http://dabuttonfactory.com/button.gif?t=$mytxt&f=Open+Sans-Bold&ts=14&tc=fff&hp=22&vp=2&c=5&bgt=unicolored&bgc=738389"
# LOGO LEFT 

#wget -O $name --random-wait  "http://dabuttonfactory.com/button.gif?t=$mytxt&f=Open+Sans-Bold&ts=14&tc=fff&hp=22&vp=2&c=5&bgt=unicolored&bgc=032B3B"


# sleep 1

done

cp -Rp *.gif /WT/appserver/webapps/wt-portal/images/buttons/
