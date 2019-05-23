<?php
        include "./db.php";
?>
<!doctype html>
<head>
<meta charset="utf-8">
<title>Board</title>
<link rel="stylesheet" type="text/css" href="./css/style.css" />
</head>
<body>
	<article class="boardArticle">
		<h2>Notice Board</h2>
		<h4 >List</h4>
			<table width="800" height="160">
                       		<thead>
					<tr>
						<th>no.</th>
						<th>title</th>
						<th>name</th>
						<th>view</th>
					</tr>
				</thead>
				<tbody>
					<?php
						$sql = mq("select * from tb order by num desc");

						while($row = $sql->fetch_array())
						{	
					
					?>
					<tr>
						<td align="center" valign="middle" class="no"><?php echo $row['num']?></td>
						<td align="center" valign="middle" class="title">
							<a href="./view.php?num=<?php echo $row['num']?>"><?php echo $row['title']?></a>
						</td>
						<td align="center" valign="middle" class="author"><?php echo $row['name']?></td>
						<td align="center" valign="middle" class="hit"><?php echo $row['view']?></td>
					</tr>
					<?php
					}
					?>
				</tbody>
			</table>
		<h4></h4>
		<center>
		<div class="btnSet">  
			<h4></h4>
			
               		<a href="./write.php" class="btnList btn" height="70px" width="200px">&#160;&#160;write&#160;&#160;</a>
       		 </div>
		</center>
</body>
</html>

