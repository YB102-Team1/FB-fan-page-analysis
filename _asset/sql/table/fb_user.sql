CREATE TABLE IF NOT EXISTS `fb_user` (
    `id` int(11) unsigned NOT NULL,
    `segment` int(10) unsigned NOT NULL,
    `fb_user_id` varchar(30) NOT NULL,
    `name` varchar(16) NOT NULL,
    `path` varchar(255) NOT NULL,
    `is_deleted` tinyint(1) unsigned NOT NULL DEFAULT '0',
    `create_time` datetime NOT NULL,
    `modify_time` datetime NOT NULL,
    `delete_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;