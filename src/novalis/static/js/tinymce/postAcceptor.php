<?php
	// Allowed the origins to upload
	$accepted_origins = array("http://localhost", "https://techarise.com/");
	// Images upload dir path
	$imgFolder = "test/";
	reset($_FILES);
	$tmp = current($_FILES);
	if(is_uploaded_file($tmp['tmp_name'])){
	    if(isset($_SERVER['HTTP_ORIGIN'])){
	        if(in_array($_SERVER['HTTP_ORIGIN'], $accepted_origins)){
	            header('Access-Control-Allow-Origin: ' . $_SERVER['HTTP_ORIGIN']);
	        }else{
	            header("HTTP/1.1 403 Origin Denied");
	            return;
	        }
	    }
	    // check valid file name
	    if(preg_match("/([^\w\s\d\-_~,;:\[\]\(\).])|([\.]{2,})/", $tmp['name'])){
	        header("HTTP/1.1 400 Invalid file name.");
	        return;
	    }
	    // check and Verify extension
	    if(!in_array(strtolower(pathinfo($tmp['name'], PATHINFO_EXTENSION)), array("gif", "jpg", "png"))){
	        header("HTTP/1.1 400 Invalid extension.");
	        return;
	    }

	    // Accept upload if there was no origin, or if it is an accepted origin
	    $filePath = $imgFolder . $tmp['name'];
	    move_uploaded_file($tmp['tmp_name'], $filePath);
	    // return successful JSON.
	    echo json_encode(array('location' => $filePath));
	} else {
	    header("HTTP/1.1 500 Server Error");
	}
	?>