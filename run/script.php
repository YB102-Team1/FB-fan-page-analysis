<?php
date_default_timezone_set("Asia/Taipei");
set_time_limit(0);

// fan list 
// $link = new mysqli('localhost', 'team1', 'yb102', 'YB102_Team1');
// $link->query("SET NAMES UTF8");
// for ($segment = 1; $segment <= 487; $segment++) {
//     $file_path = $_SERVER['DOCUMENT_ROOT'].'/_asset/data/fan_list/purified/fan_list_57613404340_'.sprintf('%05d', $segment).'.csv';
//     $file = @fopen($file_path, "r");
//     $is_first = true;
//     while (!feof($file)) {
//         $data_string = fgets($file);
//         str_replace("\n", "", $data_string);
//         $data_array = explode(',', $data_string);
//         $column1 = $data_array[0];
//         $column2 = $data_array[1];
//         $column3 = $data_array[2];
//         $now = date('Y-m-d H:i:s');
//         if ($column1) {
//             if ($is_first) {
//                 $insert_sql = "INSERT INTO `fb_user` (`segment`, `fb_user_id`, `name`, `path`, `create_time`, `modify_time`) VALUES (\"$segment\", \"$column1\", \"$column2\", \"$column3\", \"$now\", \"$now\")";
//                 $is_first = false;
//             } else {
//                 $insert_sql .= ", (\"$segment\", \"$column1\", \"$column2\", \"$column3\", \"$now\", \"$now\")";
//             }
//         }
//     }
//     $link->query($insert_sql);
//     fclose($file);
// }
// $link->close();
// echo "Table fb_user data imported.<br>";

// user likes
// function user_likes($start = 0, $end = 0) {
//     $file_prefix = 'user_likes_57613404340_';
//     $link = new mysqli('localhost', 'team1', 'yb102', 'YB102_Team1');
//     $link->query("SET NAMES UTF8");
//     for ($segment = $start; $segment <= $end; $segment++) {
//         $file_path = $_SERVER['DOCUMENT_ROOT'].'/_asset/data/user_likes/'.$file_prefix.sprintf('%05d', $segment).'.csv';
//         $file = @fopen($file_path, "r");
//         $data_counter = 1;
//         while (!feof($file)) {
//             $data_string = fgets($file);
//             str_replace("\n", "", $data_string);
//             $data_array = explode(',', $data_string);
//             if (   count($data_array) >= 2
//                 && strpos($data_string, 'l.facebook.com') === FALSE
//                 && strpos($data_string, 'apps.facebook.com') === FALSE
//             ) {
//                 $fb_user_id = $data_array[0];
//                 $fb_fan_page_id = $data_array[count($data_array) - 1];
//                 $now = date('Y-m-d H:i:s');
//                 if ($fb_fan_page_id && $data_counter == 1) {
//                     $insert_sql = "INSERT INTO `fb_user_likes` (`segment`, `fb_user_id`, `fb_fan_page_id`, `create_time`, `modify_time`) VALUES ('$segment', '$fb_user_id', \"$fb_fan_page_id\", '$now', '$now')";
//                 } else {
//                 	$insert_sql .= ", ('$segment', '$fb_user_id', \"$fb_fan_page_id\", '$now', '$now')";
//                 }
//             }
//             if ($data_counter == 1000) {
//             	$data_counter = 1;
//             	$link->query($insert_sql);
//             } else {
//             	$data_counter++;
//             }
//         }
//         $link->query($insert_sql);
//         fclose($file);
//         echo "Table fb_user_likes data of segment $segment imported.<br>";
//     }
//     $link->close();
// }
// user_likes(1, 13);
// user_likes(81, 82);
// user_likes(161, 162);
// user_likes(241, 241);
// user_likes(321, 321);
// user_likes(401, 403);

// fan page
$counter = 0; 
for ($i = 1; $i <= 1000; $i++) {

	$link = new mysqli('localhost', 'team1', 'yb102', 'YB102_Team1');
	$link->query("SET NAMES UTF8");
	$start = $counter * 1000;
	$query_instance = $link->query("SELECT DISTINCT fb_fan_page_id FROM fb_user_likes ORDER BY fb_fan_page_id ASC LIMIT $start, 1000");
	$data_counter = 1;
	$now = date('Y-m-d H:i:s');
	foreach ($query_instance as $instance_data) {

		$fb_fan_page_id = $instance_data['fb_fan_page_id'];
		if ($data_counter == 1) {
            $insert_sql = "INSERT INTO `fb_fan_page` (`fb_fan_page_id`, `create_time`, `modify_time`) VALUES (\"$fb_fan_page_id\", '$now', '$now')";
        } else {
        	$insert_sql .= ", (\"$fb_fan_page_id\", '$now', '$now')";
        }
		$data_counter++;

	}
	$link->query($insert_sql);
	$link->close();

	if ($data_counter < 1000) {
		break;
	}

	echo "Table fb_user_likes data since $start imported.<br>";
	$counter++;

}
?>