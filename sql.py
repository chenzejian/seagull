CREATE TABLE `project` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `name` varchar(100) NOT NULL,
 `client_id` varchar(16) NOT NULL,
 `client_secret` varchar(32) NOT NULL,
 `success_emails` int(11) NOT NULL,
 `fail_emails` int(11) NOT NULL,
 `status` smallint(6) NOT NULL,
 `created_at` datetime(6) NOT NULL,
 `updated_at` datetime(6) NOT NULL,
 `creator_id` int(11) NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE `email` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `title` varchar(1024) NOT NULL,
 `content` longtext NOT NULL,
 `from_user` varchar(255) NOT NULL DEFAULT '''''' COMMENT '寄件人',
 `receive_user` varchar(255) NOT NULL DEFAULT '''''' COMMENT '接收人email',
 `cc_user` varchar(255) NOT NULL DEFAULT '''''' COMMENT '抄送邮件',
 `send_type` tinyint(2) unsigned NOT NULL DEFAULT '0' COMMENT '发送方式：1=>mailgun，2=>自建服务，3=>qqsmtp',
 `send_times` int(11) NOT NULL,
 `created_at` datetime(6) NOT NULL,
 `updated_at` datetime(6) NOT NULL,
 `project_id` int(11) NOT NULL,
 `task_id` varchar(255) NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `task_id` (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8


