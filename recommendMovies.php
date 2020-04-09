<?php

session_start();

ini_set('error_reporting', E_ALL);
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);

$mysqli = new mysqli('remotemysql.com', 'AmLB63D4F9', 'ARsY8WGMUO', 'AmLB63D4F9');

$out = '<div class="tab-pane active" id="rec">
    <div class="container">
  <h2>Recommendations</h2>

  <table class="table table-striped">
    <thead>
      <tr>';
      $content = file_get_contents("http://104.154.69.181/recommendation/getRecommendations.php?movies=" . json_encode($_SESSION['movies']));


            $pairs = explode(' ', $content);
            $names = array();
            foreach ($pairs as $value) {
                $arr = explode(':', $value);

		if (count($arr) != 2) {
			continue;
		}
                $name = $arr[0];
                $mid = $arr[1];
                $keys = array_keys($names);
                if (!in_array($name, $keys)){
                    $names[$name] = array();

                }
                array_push($names[$name], $mid);
            }

            arsort($names);

            $names = array_slice($names, 0, 4);  // Оставляем топ-3 жанров

            foreach ($names as $key=>$value){
                $out .= "<th>$key</th>";
            }


            $out .= " </tr></thead><tbody><tr>";
            $genre2Titles = array();
            foreach($names as $key=>$value){

                foreach($value as $mid){
                    $title = mysqli_fetch_row($mysqli->query("select title from movies where movieId='$mid' limit 1"))[0];
                    $keys = array_keys($genre2Titles);
                    if (!in_array($key, $keys)){
                        $genre2Titles[$key] = $title;
                    }
                    else{
                        $genre2Titles[$key] .= "<br>$title";
                    }
                }
            }
            foreach($genre2Titles as $key=>$ans){
                $out .= "<td>$ans</td>";
            }
            $out .= "</tr></tbody></table></div></div>";
            $mysqli->close();
            echo $out;
