<?php
session_start();
if(isset($_SESSION['movies'])){
    $data = json_decode(file_get_contents('php://input'), true);
    if(isset($data['mid'])){
        if (($key = array_search($data['mid'], $_SESSION['movies'])) !== false) {
            unset($_SESSION['movies'][$key]);
            echo "This movie was removed from your favorite list";
        }
        else{
            echo "This movie was not in your favorite list";
        }
    }

}
else{
    echo 'error';
}