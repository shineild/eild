<?php
	session_start();
	header('Contest-Type: text/html; charset=utf-8'); // utf-8 인코딩

	$db = new mysqli("localhost", "root", "marvle", "tb");
	$db->set_charset("utf8");

	function mq($sql)
	{
		global $db;
		return $db->query($sql);
	}
?>
