<?php

session_start();
$movies = json_encode($_SESSION['movies']);

$command = escapeshellcmd("python3 movies_rating_predictor.py --chosen_movie_idx $movies");
$output = shell_exec($command);
echo $output;
