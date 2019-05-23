<?php
	include "./db.php";

	if(isset($_GET['num'])) {
		$num = $_GET['num'];
	}

	if(isset($num)) {
		$sql = mq("select title, contents, name from tb where num = " . $num);
		$row = $sql->fetch_array();
	}
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>Writing</title>
	<link rel="stylesheet" type="text/css" href="./css/style.css" />
</head>
<body>
	<h2>Write</h2>
		<form action="./write_up.php" method="post">
			<?php
				if(isset($num)) {
					echo '<input type="hidden" name="num" value="' . $num . '">';
				}
			?>	
			<table id="boardWrite">
			<tbody>
				<tr>
				<th scope="row" width="130px" height="50px"><label for ="name">nick name</label></th>
				<td class="id">
					<?php
					if(isset($num)) {
						echo $row['name'];
					} else { ?>
						<input type="text" name="name" id="name">
					<?php }?>
				</td>
				</tr>
				<tr>
				<th scope="row" height="50px"><label for="title">title</label></th>
				<td class="title"><input type="text" name="title" id="title" value="<?php echo isset($row['title'])?$row['title']:null?>"></td>
				</tr>
				<tr>
				<th scope="row" height="80px"><label for="contents">write here</th>
				<td class="content"><textarea name="contents" id="contents"><?php echo isset($row['contents'])?$row['contents']:null?></textarea></td>
				</tr>
			</tbody>
			</table>
			<h4></h4>
		<center>
			<div class="btnSet">
				<button size="30px" type="submit" class="btnSubmit btn btn-lg" height="70px" width="100px">
				<?php echo isset($num)?'fix':'write'?>
				</button>
				<h4></h4>
				<a href="./index.php" class="btnList btn" height="70px" width="100px">list</a>
			</div>
		</center>
		</form>
	
</body>
</html>

