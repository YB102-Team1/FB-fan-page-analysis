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

/*
$sql = "CREATE TABLE IF NOT EXISTS `???` (
            `id` int(11) unsigned NOT NULL,
            ...
            `is_deleted` tinyint(1) unsigned NOT NULL DEFAULT '0',
            `create_time` datetime NOT NULL,
            `modify_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
            `delete_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;";
mysqli_query($connection, $sql);
$sql = "ALTER TABLE `test_table` ADD PRIMARY KEY (`id`);";
mysqli_query($connection, $sql);
$sql = "ALTER TABLE `test_table` MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;";
mysqli_query($connection, $sql);
*/

// create table
$sql = "CREATE TABLE IF NOT EXISTS `test_table` (
            `id` int(11) unsigned NOT NULL,
            `test_column` varchar(255) NOT NULL,
            `is_deleted` tinyint(1) unsigned NOT NULL DEFAULT '0',
            `create_time` datetime NOT NULL,
            `modify_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
            `delete_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;";
mysqli_query($connection, $sql);
$sql = "ALTER TABLE `test_table` ADD PRIMARY KEY (`id`);";
mysqli_query($connection, $sql);
$sql = "ALTER TABLE `test_table` MODIFY `id` int(11) unsigned NOT NULL AUTO_INCREMENT;";
mysqli_query($connection, $sql);
?>