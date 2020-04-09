<?php
$mysqli = new mysqli('remotemysql.com', 'AmLB63D4F9', 'ARsY8WGMUO', 'AmLB63D4F9');
$data = json_decode(file_get_contents('php://input'), true);
if (isset($data['title'])){
    $title = $data['title'];
    $out = '<div class="tab-pane active" id="searched">
    <div class="container" style="text-align: center"><ul id="myUL">';
    $res = $mysqli->query("select * from movies where title LIKE '%$title%'");
    while($row = $res->fetch_assoc()){
        $title = $row['title'];
        $mid = $row['movieId'];
        $out .= "<li id='$mid'>
        <div style='display: inline-block;vertical-align: middle;margin:10px 0;'>
        $title
        <div style='display: inline-block;vertical-align: middle; border:0;'>
        <button class='btn btn-success' onclick='addMovie($mid)'>Добавить</button>
        <button class='btn btn-danger' onclick='removeMovie($mid)'>Удалить</button>
        </div>
        </div>
        </li>";
    }
    $out .= "</ul>
        </div>
        </div>";
    echo $out;
}
else{
    echo 'data is not set!';
}
$mysqli->close();