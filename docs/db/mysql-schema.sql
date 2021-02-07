-- Create model admin.LogEntry
CREATE TABLE `django_admin_log` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `action_time` datetime(6) NOT NULL,
    `object_id` longtext NULL,
    `object_repr` varchar(200) NOT NULL,
    `action_flag` smallint UNSIGNED NOT NULL,
    `change_message` longtext NOT NULL,
    `content_type_id` integer NULL,
    `user_id` integer NOT NULL
    );
ALTER TABLE `django_admin_log`
    ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co`
    FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
ALTER TABLE `django_admin_log`
    ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_user_id`
    FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);

-- Create model auth.Permission
CREATE TABLE `auth_permission` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(50) NOT NULL,
    `content_type_id` integer NOT NULL,
    `codename` varchar(100) NOT NULL
    );

-- Create model auth.Group
CREATE TABLE `auth_group` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(80) NOT NULL UNIQUE
    );
CREATE TABLE `auth_group_permissions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `group_id` integer NOT NULL,
    `permission_id` integer NOT NULL
    );

-- Create model auth.User
ALTER TABLE `auth_permission`
    ADD `auth_permission_content_type_id_codename_01ab375a_uniq`
    UNIQUE (`content_type_id`, `codename`);
ALTER TABLE `auth_permission`
    ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co`
    FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
ALTER TABLE `auth_group_permissions`
    ADD `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`
    UNIQUE (`group_id`, `permission_id`);
ALTER TABLE `auth_group_permissions`
    ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id`
    FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `auth_group_permissions`
    ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`
    FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

-- Create model contenttypes.ContentType
CREATE TABLE `django_content_type` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(100) NOT NULL,
    `app_label` varchar(100) NOT NULL,
    `model` varchar(100) NOT NULL
    );
ALTER TABLE `django_content_type`
    ADD `django_content_type_app_label_model_76bd3d3b_uniq`
    UNIQUE (`app_label`, `model`);

-- Create model sessions.Session
CREATE TABLE `django_session` (
    `session_key` varchar(40) NOT NULL PRIMARY KEY,
    `session_data` longtext NOT NULL,
    `expire_date` datetime(6) NOT NULL
    );
CREATE INDEX `django_session_expire_date_a5c62663`
    ON `django_session` (`expire_date`);

-- Create model accounts.User
CREATE TABLE `accounts_user` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `password` varchar(128) NOT NULL,
    `last_login` datetime(6) NULL,
    `is_superuser` bool NOT NULL,
    `is_staff` bool NOT NULL,
    `is_active` bool NOT NULL,
    `date_joined` datetime(6) NOT NULL,
    `email` varchar(254) NOT NULL UNIQUE,
    `first_name` varchar(30) NOT NULL,
    `last_name` varchar(30) NOT NULL,
    `phone_number` varchar(20) NOT NULL,
    `bio` longtext NULL,
    `profile_picture` varchar(100) NOT NULL
    );
CREATE TABLE `accounts_user_groups` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `group_id` integer NOT NULL
    );
CREATE TABLE `accounts_user_user_permissions` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `permission_id` integer NOT NULL
    );
ALTER TABLE `accounts_user_groups`
    ADD `accounts_user_groups_user_id_group_id_59c0b32f_uniq`
    UNIQUE (`user_id`, `group_id`);
ALTER TABLE `accounts_user_groups`
    ADD CONSTRAINT `accounts_user_groups_user_id_52b62117_fk_accounts_user_id`
    FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
ALTER TABLE `accounts_user_groups`
    ADD CONSTRAINT `accounts_user_groups_group_id_bd11a704_fk_auth_group_id`
    FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `accounts_user_user_permissions`
    ADD CONSTRAINT `accounts_user_user_p_user_id_e4f0a161_fk_accounts_`
    FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
ALTER TABLE `accounts_user_user_permissions`
    ADD CONSTRAINT `accounts_user_user_p_permission_id_113bb443_fk_auth_perm`
    FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
ALTER TABLE `accounts_user_user_permissions`
    ADD `accounts_user_user_permi_user_id_permission_id_2ab516c2_uniq`
    UNIQUE (`user_id`, `permission_id`);

-- Create model resources.Category
CREATE TABLE `resources_category` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `slug` varchar(50) NOT NULL UNIQUE,
    `last_edit` datetime(6) NOT NULL,
    `name` varchar(30) NOT NULL,
    `description` longtext NULL,
    `date_created` datetime(6) NOT NULL
    );

-- Create model resources.Tag
CREATE TABLE `resources_tag` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `slug` varchar(50) NOT NULL UNIQUE,
    `last_edit` datetime(6) NOT NULL,
    `name` varchar(30) NOT NULL,
    `date_created` datetime(6) NOT NULL
    );

-- Create model resources.Video
CREATE TABLE `resources_video` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `slug` varchar(50) NOT NULL UNIQUE,
    `last_edit` datetime(6) NOT NULL,
    `title` varchar(50) NOT NULL,
    `summary` longtext NULL,
    `date_posted` datetime(6) NOT NULL,
    `url` varchar(200) NOT NULL,
    `category_id` integer NOT NULL
    );
CREATE TABLE `resources_video_authors` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `video_id` integer NOT NULL,
    `user_id` integer NOT NULL
    );
CREATE TABLE `resources_video_tags` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `video_id` integer NOT NULL,
    `tag_id` integer NOT NULL
    );

-- Create model resources.Book
CREATE TABLE `resources_book` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `slug` varchar(50) NOT NULL UNIQUE,
    `last_edit` datetime(6) NOT NULL,
    `title` varchar(50) NOT NULL,
    `summary` longtext NULL,
    `date_posted` datetime(6) NOT NULL,
    `cover_image` varchar(100) NOT NULL,
    `file_upload` varchar(100) NOT NULL,
    `category_id` integer NOT NULL
    );
CREATE TABLE `resources_book_authors` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `book_id` integer NOT NULL,
    `user_id` integer NOT NULL
    );
CREATE TABLE `resources_book_tags` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `book_id` integer NOT NULL,
    `tag_id` integer NOT NULL
    );

ALTER TABLE `resources_video`
    ADD CONSTRAINT `resources_video_category_id_741cd71d_fk_resources_category_id`
    FOREIGN KEY (`category_id`) REFERENCES `resources_category` (`id`);
ALTER TABLE `resources_video_authors`
    ADD `resources_video_authors_video_id_user_id_3d91712a_uniq`
    UNIQUE (`video_id`, `user_id`);
ALTER TABLE `resources_video_authors`
    ADD CONSTRAINT `resources_video_authors_video_id_941380cb_fk_resources_video_id`
    FOREIGN KEY (`video_id`) REFERENCES `resources_video` (`id`);
ALTER TABLE `resources_video_authors`
    ADD CONSTRAINT `resources_video_authors_user_id_36b8d107_fk_accounts_user_id`
    FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
ALTER TABLE `resources_video_tags`
    ADD `resources_video_tags_video_id_tag_id_82a53c83_uniq`
    UNIQUE (`video_id`, `tag_id`);
ALTER TABLE `resources_video_tags`
    ADD CONSTRAINT `resources_video_tags_video_id_00379813_fk_resources_video_id`
    FOREIGN KEY (`video_id`) REFERENCES `resources_video` (`id`);
ALTER TABLE `resources_video_tags`
    ADD CONSTRAINT `resources_video_tags_tag_id_2f214763_fk_resources_tag_id`
    FOREIGN KEY (`tag_id`) REFERENCES `resources_tag` (`id`);
ALTER TABLE `resources_book`
    ADD CONSTRAINT `resources_book_category_id_5c0ecec3_fk_resources_category_id`
    FOREIGN KEY (`category_id`) REFERENCES `resources_category` (`id`);
ALTER TABLE `resources_book_authors`
    ADD `resources_book_authors_book_id_user_id_2bc6be29_uniq`
    UNIQUE (`book_id`, `user_id`);
ALTER TABLE `resources_book_authors`
    ADD CONSTRAINT `resources_book_authors_book_id_ff263faf_fk_resources_book_id`
    FOREIGN KEY (`book_id`) REFERENCES `resources_book` (`id`);
ALTER TABLE `resources_book_authors`
    ADD CONSTRAINT `resources_book_authors_user_id_746d8c18_fk_accounts_user_id`
    FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
ALTER TABLE `resources_book_tags`
    ADD `resources_book_tags_book_id_tag_id_9cc81e0a_uniq`
    UNIQUE (`book_id`, `tag_id`);
ALTER TABLE `resources_book_tags`
    ADD CONSTRAINT `resources_book_tags_book_id_af5350ab_fk_resources_book_id`
    FOREIGN KEY (`book_id`) REFERENCES `resources_book` (`id`);
ALTER TABLE `resources_book_tags`
    ADD CONSTRAINT `resources_book_tags_tag_id_79151059_fk_resources_tag_id`
    FOREIGN KEY (`tag_id`) REFERENCES `resources_tag` (`id`);
