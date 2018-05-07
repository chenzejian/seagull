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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE `email` (
 `id` int(11) NOT NULL AUTO_INCREMENT,
 `title` varchar(1024) NOT NULL,
 `content` longtext NOT NULL,
 `send_times` int(11) NOT NULL,
 `created_at` datetime(6) NOT NULL,
 `updated_at` datetime(6) NOT NULL,
 `project_id` int(11) NOT NULL,
 `task_id` varchar(255) NOT NULL,
 PRIMARY KEY (`id`),
 UNIQUE KEY `task_id` (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8


