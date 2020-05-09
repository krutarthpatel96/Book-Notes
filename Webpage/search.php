<!DOCTYPE>
<?php
   ob_start();
   session_start();
?>
<html>
<head>
<style>
#vis {
  display:none;
}
#vis2 {
  display:none;
}
#vis3 {
  display:none;
}
</style>
<meta charset="ISO-8859-1">
<title>Insert title here</title>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"></script>
</head>
<body>
<center>
<div class="jumbotron text-center">
  <h1>Welcome to the portal</h1>
  <p>Cloud Computing Assignment 3</p>
  <p>Krutarth Patel (B00835794)</p>
</div>

<form  method="POST" action="">
<input type = "text" name = 'keyword' placeholder="Search keyword" />
<button class="btn btn-primary active" name="btn_search_book">Book Search</button>
<button class="btn btn-primary active" name="btn_search_author">Author Search</button>
<br><br>
<input id="vis" type = "text" name = 'note' placeholder="Note" style="display: none;"/>
<button id="vis2" class="btn btn-primary active" name="btn_submit_note" style="display: none;">Note Submision</button>
<button id="vis3" class="btn btn-primary active" name="btn_retrieve_note" style="display: none;">Note Retrieval</button>
</form>
</center>
</body>
</html>

<?php
error_reporting(0);

$ipAdd = file_get_contents('http://169.254.169.254/latest/meta-data/public-ipv4');
#print($ipAdd);

if (isset($_POST['btn_search_book'])){

 	$author = urlencode($_POST['keyword']);
 	$_SESSION['keyword'] = $author;

 	if(strlen($author) == 0){
 		echo "<script type='text/javascript'>alert('Please enter a valid keyword!');</script>";
 	}else{

	 	$response = file_get_contents("http://".$ipAdd.":5000/searchBook?author=".$author);
		$str = json_decode($response, true);
		
		 if(empty($str)){
		 	echo "<script type='text/javascript'>alert('Keyword not found!');</script>";
		 }else{

			echo "<script type='text/javascript'>
				document.getElementById('vis').style.display='inline';
				document.getElementById('vis2').style.display='inline';
				document.getElementById('vis3').style.display='inline';
				</script>";

			$tab = "<table class=table border=1px  style = 'position: absolute; top: 420'>";
			$tab .= "<tr><th bgcolor='#A9A9A9'>Author</th>";
			$tab .= "<th bgcolor='#A9A9A9'>Book</th></tr>";

			for($i = 0; $i < sizeof($str); $i++)
			{
				$tab .= "<tr>";
				$tab .= "<td>".$str[$i]["author"]."</td>";
				$tab .= "<td>".$str[$i]["book"]."</td>";
				$tab .= "</tr>";
			}
			 
			$tab .= "</table>";
			echo $tab;
		}
	}

}else if (isset($_POST['btn_search_author'])){
 	
	$book = urlencode($_POST['keyword']);
	$_SESSION['keyword'] = $book;

	if(strlen($book) == 0){
 		echo "<script type='text/javascript'>alert('Please enter a valid keyword!');</script>";
 	}else{

		$response = file_get_contents("http://".$ipAdd.":5000/searchAuthor?book=".$book);
		$str = json_decode($response, true);

 		if(empty($str)){
			echo "<script type='text/javascript'>alert('Keyword not found!');</script>";
		}else{

			echo "<script type='text/javascript'>
				document.getElementById('vis').style.display='inline';
				document.getElementById('vis2').style.display='inline';
				document.getElementById('vis3').style.display='inline';
				</script>";
			
			$tab = "<table class=table border=1px  style = 'position: absolute; top: 420'>";
			$tab .= "<tr><th bgcolor='#A9A9A9'>Author</th>";
			$tab .= "<th bgcolor='#A9A9A9'>Book</th></tr>";

			for($i = 0; $i < sizeof($str); $i++)
			{
				$tab .= "<tr>";
				$tab .= "<td>".$str[$i]["author"]."</td>";
				$tab .= "<td>".$str[$i]["book"]."</td>";
				$tab .= "</tr>";
			}
			 
			$tab .= "</table>";
			echo $tab;
		}

	}
	
}

if (isset($_POST['btn_submit_note'])){	 	
	
	$keyword = $_SESSION['keyword'];
	$note = urlencode($_POST['note']);

	if(strlen($keyword) == 0 || strlen($note) == 0){
 		echo "<script type='text/javascript'>alert('Please enter a valid keyword/note!');</script>";
 	}else{
		$response = file_get_contents("http://".$ipAdd.":5000/submitNote?keyword=".$keyword."&note=".$note);
		echo "$response";
	}
}
else if (isset($_POST['btn_retrieve_note'])){
	
	$keyword = $_SESSION['keyword'];

 	if(strlen($keyword) == 0){
		echo "<script type='text/javascript'>alert('Please enter a valid keyword/note!');</script>";
 	}else{
	 	$response = file_get_contents("http://".$ipAdd.":5000/retrieveNote?keyword=".$keyword);
		$str = json_decode($response, true);
		
		$tab = "<table class=table border=1px  style = 'position: absolute; top: 420'>";
		$tab .= "<tr><th bgcolor='#A9A9A9'>Keyword</th>";
		$tab .= "<th bgcolor='#A9A9A9'>Note</th></tr>";

		for($i = 0; $i < sizeof($str); $i++)
		{
			$tab .= "<tr>";
			$tab .= "<td>".$str[$i]["keyword"]."</td>";
			$tab .= "<td>".$str[$i]["note"]."</td>";
			$tab .= "</tr>";
		}
		 
		$tab .= "</table>";
		echo $tab;
	}
}


?>

