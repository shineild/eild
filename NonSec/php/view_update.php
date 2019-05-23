<?php
	include "./db.php";
	$num = $_POST['num'];
	$sql = mq("delete from tb where num = " . $num);
	$msg = 'remove sucess';
	$replaceURL = './index.php';
?>
<script>
	alert("<?php echo $msg?>");
	location.replace("<?php echo $replaceURL?>");
</script>

