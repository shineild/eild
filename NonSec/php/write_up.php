<?php
	include "./db.php";
	if(isset($_POST['num'])) {
		$num = $_POST['num'];
	}
	if(empty($num)){
		$name = $_POST['name'];	
	}
	$title = $_POST['title'];
	$contents = $_POST['contents'];
	if(isset($num)){
		$sql = mq("update tb set title='". $title ."', contents='".$contents."' where num ='".$num."'");
	}
	else{
		$sql = mq("insert into tb(title, contents, name) values('".$title."','".$contents."','".$name."')");
	}
		if($sql) {
			$msg = "go! good! god! goid! go!";
			if(empty($num)) {
				$num = $db->insert_id;
		}
			$replaceURL = './index.php';
		} else {
			$msg = "no~now~now~no~";
?>
			<script>
			alert("<?php echo $msg?>");
			history.back();
			</script>
<?php
			exit;
		}

?>
<script>
	alert("<?php echo $msg?>");
	location.replace("<?php echo $replaceURL?>");
</script>
