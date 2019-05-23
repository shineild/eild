<?php
	include "./db.php";
	$num = $_GET['num'];
	$sql = mq("update tb set view = view + 1 where num = " . $num);
	$sql = mq("select title, contents, name, view from tb where num = ". $num);
	$row = $sql->fetch_array();
?>
<!DOCTYPE html>
<html>
	<head>
	<meta charset="utf-8" />
	<title>Board View</title>
	<link rel="stylesheet" type="text/css" href="./css/style.css" />
	</head>
	<body>
	<article class="boardArticle">
	<h2>View</h2>
	<div id="boardView">
	<form action="./view_update.php" method="post">
		<input type="hidden" name="num" value="<?php echo $num?>">
		<h4 id="boardTitle"><?php echo $row['title']?></h4>
		<center>
		<div id="boardInfo">
		<h5>
			<span id="boardID">writer:&#160;<?php echo $row['name']?></span>
			<pre></pre>
		</h5>
		<h5>
			<span id="boardHit">view:&#160;<?php echo $row['view']?></span>
		</h5>
		</div>
		<h5></h5>
		<div id="boardContent"><?php echo $row['contents']?></div>
		</center>
	</div>
	<h5></h5>
	<div class="btnSet">
		<center>
		<a href="./write.php?num=<?php echo $num?>">fix</a><?php echo '&#160;&#160;&#160;&#160;&#160;'?>
		<a href="./index.php">list</a>
		<button type="submit" class="btnSubmit btn">delete</button>
	</div>
	</article>
</body>
</html>
