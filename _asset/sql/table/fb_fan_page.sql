CREATE TABLE IF NOT EXISTS `fb_fan_page` (
    `id` int(11) unsigned NOT NULL,
    `fb_fan_page_id` int(128) NOT NULL,
    `name` varchar(128) NOT NULL,
    `path` varchar(255) NOT NULL,
    `category_id` int(128) NOT NULL,
    `description` text NOT NULL,
    `likes` int(128) NOT NULL,
    `is_deleted` tinyint(1) unsigned NOT NULL DEFAULT '0',
    `create_time` datetime NOT NULL,
    `modify_time` datetime NOT NULL,
    `delete_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;