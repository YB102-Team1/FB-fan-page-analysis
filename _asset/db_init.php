<?php
include $_SERVER['DOCUMENT_ROOT'].'/_config/system_config.inc';
include DB_CONFIG_FILE;

$connection = mysqli_connect($database_host, $database_user, $database_password);

// check connection
if (mysqli_connect_errno()) {

    echo 'Failed to connect to MySQL: '.mysqli_connect_error();
    throw new RuntimeException();

}

// create database
$database_selected = mysqli_select_db($connection, $database_name);
if (!$database_selected) {

    $sql = "CREATE DATABASE $database_name";
    if (!mysqli_query($connection, $sql)) {

        echo "Error when creating database `$database_name`: ".mysql_error()."<br>";
        exit;

    }

}
?>