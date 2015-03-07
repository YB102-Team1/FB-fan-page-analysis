<?php
date_default_timezone_set("Asia/Taipei");
set_time_limit(0);
include $_SERVER['DOCUMENT_ROOT'].'/_config/system_config.inc';
$fb_User_likes_god_obj = new FbUserLikesGod();
$fb_fan_page_god_obj = new FbFanPageGod();
$length = 1000;
for ($counter = 1; $counter <= 8000; $counter++) {

	$fb_fan_page_id_result = $fb_User_likes_god_obj->getDistinctFanPageId($counter * $length, $length);
	foreach ($fb_fan_page_id_result as $fb_fan_page_id) {

		$param = array("fb_fan_page_id"=>$fb_fan_page_id);
		$fb_fan_page_god_obj->create($param);

	}
	echo $counter.'<br>';

}
unset($fb_fan_page_god_obj);
unset($fb_User_likes_god_obj);
?>