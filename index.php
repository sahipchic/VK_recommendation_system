<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
session_start();
if (!isset($_SESSION['movies'])) {
	$_SESSION['movies'] = array();
}

?>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
          integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
     <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
            integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
            crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js"
            integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6"
            crossorigin="anonymous"></script>

<script>
    function recommendMovies(){
        var btn = document.getElementById("rec-btn");
        btn.disabled=true;
        var result = $.ajax( {
                url: 'recommendMovies.php'
              } )
              .done(function(response) {
                document.getElementById("main").innerHTML = response;
                btn.disabled=false;
              })
              .fail(function() {
                alert( "error" );
              });

    }

    function searchMovies() {
            var input, filter;
            input = document.getElementById("myInput");
            filter = input.value;
            var btn = document.getElementById("search-btn");
            btn.disabled=true;


            var result = $.ajax( {
                url: 'getMovies.php',
                type: 'post',
                contentType: 'application/json',
                data: JSON.stringify({"title": filter})
              } )
              .done(function(response) {
                document.getElementById("main").innerHTML = response;
                btn.disabled=false;
              })
              .fail(function() {
                alert( "error" );
              });
        }
    function addMovie(mid){
        var result = $.ajax( {
            url: 'addMovie.php',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify({"mid": mid}),
              } )
              .done(function(response) {
                alert(response);
              })
              .fail(function() {
                alert( "error" );
              });

    }
    function removeMovie(mid){
        var result = $.ajax( {
            url: 'removeMovie.php',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify({"mid": mid}),
              } )
              .done(function(response) {
                alert(response);
              })
              .fail(function() {
                alert( "error" );
              });
    }
</script>

<style>
* {
  box-sizing: border-box;
}

#myInput {
  background-position: 10px 12px;
  background-repeat: no-repeat;
  width: 100%;
  font-size: 16px;
  padding: 12px 20px 12px 40px;
  border: 1px solid #ddd;
  margin-bottom: 12px;
}

#myUL {

  padding: 12px;
  margin: 0;
}

#myUL li div {
    width: 100%;
  border: 1px solid #ddd;
  margin-top: -1px;
  background-color: #f6f6f6;
  padding: 12px;
  text-decoration: none;
  font-size: 18px;
  color: black;
  display: inline-block;
}

#myUL li a:hover:not(.header) {
  background-color: #eee;
}
</style>
</head>
<body>
<div style="margin:100px;">
<h2 align="center">Recommendation System</h2>

<input type="text" id="myInput" onkeyup="" placeholder="Search for names.." title="Type in a name">
<div align="center">
<button class="btn btn-success" onclick="searchMovies()" id="search-btn">Search</button>
<button class="btn btn-warning" onclick="recommendMovies()" id="rec-btn">Recommend</button>
</div>
</div>
<div id="main">

</div>

</body>
</html>
