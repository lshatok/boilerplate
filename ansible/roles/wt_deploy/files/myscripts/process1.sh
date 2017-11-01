cat 2buttons.txt| while read line
	do
		name=$line
		text=`echo $line | cut -d"_" -f 2,3,4 | cut -d"." -f1 | sed 's/_/+/g'`
#		echo $text
#		echo "$name,$text"


   echo ">>>>>>>>>>>>>>>>>>>>>>>>";
    echo "Executing wget $i ......";
    echo ">>>>>>>>>>>>>>>>>>>>>>>>";
    
    #random sleep time 1-10 sec
    sleep_time=$[ ( $RANDOM % 10 ) + 1 ];
    echo "Sleep time: $sleep_time seconds";
    sleep $sleep_time

    #random user-agent header 1-13 line
    user_agent_number=$[ ( $RANDOM % 13 ) + 1 ];
    #echo $user_agent_number;
    user_agent=`awk -v r=$user_agent_number ' NR==r {print} ' user_agent.list`;
    
    echo ">>>>>>>>>>>>>>>>>>>>>>>";
    echo "User agent: $user_agent";
    echo ">>>>>>>>>>>>>>>>>>>>>>>>";

    #random http proxy 1-21 line
    proxy_number=$[ ( $RANDOM % 21 ) + 1 ];
    use_proxy=`awk -v r=$proxy_number ' NR==r {print} ' proxy.list`;
    
    echo ">>>>>>>>>>>>>>>>>>>>>>>";
    echo "Using proxy: $use_proxy";
    echo ">>>>>>>>>>>>>>>>>>>>>>>";
    export http_proxy=`$use_proxy`;


wget  -O $name http://dabuttonfactory.com/button.gif&t=$text&f=Calibri&ts=14&tc=fff&hp=20&vp=2&c=5&bgt=unicolored&bgc=000000&fgc=FFFFFF
break
done

