CREATE TABLE IF NOT EXISTS `fb_user_likes` (
    `id` int(11) unsigned NOT NULL,
    `segment` int(10) NOT NULL,
    `fb_user_id` varchar(30) NOT NULL,
    `fb_fan_page_id` varchar(30) NOT NULL,
    `is_deleted` tinyint(1) unsigned NOT NULL DEFAULT '0',
    `create_time` datetime NOT NULL,
    `modify_time` datetime NOT NULL,
    `delete_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;