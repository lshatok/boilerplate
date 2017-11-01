cat templateA | while read line;
	 do
	    	BASE=`echo $line | cut -d"." -f1`
	        #echo $BASE
		SPACED=`echo $BASE | sed 's/_/ /g' | cut -d" " -f2-10 | sed -r 's/\<./\U&/g'|  sed 's/ /+/g'`
		echo "$line,$SPACED" >> all_my_sons.my
		#echo $SPACED
	 done
