<?php
session_start();

if(isset($_SESSION['movies'])){
    $data = json_decode(file_get_contents('php://input'), true);
    if(isset($data['mid'])){
        if(!in_array($data['mid'], $_SESSION['movies'])){
            array_push($_SESSION['movies'], $data['mid']);
            echo "This movie was added to your favorite list";
        }
        else{
            echo "This movie has been already added to your favorite list before!";
        }
    }
    else{
        echo "Data is not set!";
    }

}
else{
    echo 'error';
}