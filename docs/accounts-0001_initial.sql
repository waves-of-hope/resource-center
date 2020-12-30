--
-- Create model User
--
CREATE TABLE `accounts_user` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `password` varchar(128) NOT NULL, `last_login` datetime(6) NULL, `is_superuser` bool NOT NULL, `is_staff` bool NOT NULL, `is_active` bool NOT NULL, `date_joined` datetime(6) NOT NULL, `email` varchar(254) NOT NULL UNIQUE, `first_name` varchar(30) NOT NULL, `last_name` varchar(30) NOT NULL, `phone_number` varchar(20) NOT NULL, `bio` longtext NULL, `profile_picture` varchar(100) NOT NULL);
CREATE TABLE `accounts_user_groups` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `user_id` integer NOT NULL, `group_id` integer NOT NULL);
CREATE TABLE `accounts_user_user_permissions` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `user_id` integer NOT NULL, `permission_id` integer NOT NULL);
ALTER TABLE `accounts_user_groups` ADD CONSTRAINT `accounts_user_groups_user_id_group_id_59c0b32f_uniq` UNIQUE (`user_id`, `group_id`);
ALTER TABLE `accounts_user_groups` ADD CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
ALTER TABLE `accounts_user_groups` ADD CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `accounts_user_user_permissions` ADD CONSTRAINT `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq` UNIQUE (`user_id`, `permission_id`);
ALTER TABLE `accounts_user_user_permissions` ADD CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
ALTER TABLE `accounts_user_user_permissions` ADD CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
