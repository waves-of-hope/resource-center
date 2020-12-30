--
-- Create model Category
--
CREATE TABLE `resources_category` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `slug` varchar(50) NOT NULL UNIQUE, `last_edit` datetime(6) NOT NULL, `name` varchar(30) NOT NULL, `description` longtext NULL, `date_created` datetime(6) NOT NULL);
--
-- Create model Tag
--
CREATE TABLE `resources_tag` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `slug` varchar(50) NOT NULL UNIQUE, `last_edit` datetime(6) NOT NULL, `name` varchar(30) NOT NULL, `date_created` datetime(6) NOT NULL);
--
-- Create model Video
--
CREATE TABLE `resources_video` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `slug` varchar(50) NOT NULL UNIQUE, `last_edit` datetime(6) NOT NULL, `title` varchar(50) NOT NULL, `summary` longtext NULL, `date_posted` datetime(6) NOT NULL, `url` varchar(200) NOT NULL, `category_id` integer NOT NULL);
CREATE TABLE `resources_video_authors` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `video_id` integer NOT NULL, `user_id` integer NOT NULL);
CREATE TABLE `resources_video_tags` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `video_id` integer NOT NULL, `tag_id` integer NOT NULL);
--
-- Create model Book
--
CREATE TABLE `resources_book` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `slug` varchar(50) NOT NULL UNIQUE, `last_edit` datetime(6) NOT NULL, `title` varchar(50) NOT NULL, `summary` longtext NULL, `date_posted` datetime(6) NOT NULL, `cover_image` varchar(100) NOT NULL, `file_upload` varchar(100) NOT NULL, `category_id` integer NOT NULL);
CREATE TABLE `resources_book_authors` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `book_id` integer NOT NULL, `user_id` integer NOT NULL);
CREATE TABLE `resources_book_tags` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `book_id` integer NOT NULL, `tag_id` integer NOT NULL);
ALTER TABLE `resources_video` ADD CONSTRAINT `resources_video_category_id_741cd71d_fk_resources_category_id` FOREIGN KEY (`category_id`) REFERENCES `resources_category` (`id`);
ALTER TABLE `resources_video_authors` ADD CONSTRAINT `resources_video_authors_video_id_user_id_3d91712a_uniq` UNIQUE (`video_id`, `user_id`);
ALTER TABLE `resources_video_authors` ADD CONSTRAINT `resources_video_authors_video_id_941380cb_fk_resources_video_id` FOREIGN KEY (`video_id`) REFERENCES `resources_video` (`id`);
ALTER TABLE `resources_video_authors` ADD CONSTRAINT `resources_video_authors_user_id_36b8d107_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
ALTER TABLE `resources_video_tags` ADD CONSTRAINT `resources_video_tags_video_id_tag_id_82a53c83_uniq` UNIQUE (`video_id`, `tag_id`);
ALTER TABLE `resources_video_tags` ADD CONSTRAINT `resources_video_tags_video_id_00379813_fk_resources_video_id` FOREIGN KEY (`video_id`) REFERENCES `resources_video` (`id`);
ALTER TABLE `resources_video_tags` ADD CONSTRAINT `resources_video_tags_tag_id_2f214763_fk_resources_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `resources_tag` (`id`);
ALTER TABLE `resources_book` ADD CONSTRAINT `resources_book_category_id_5c0ecec3_fk_resources_category_id` FOREIGN KEY (`category_id`) REFERENCES `resources_category` (`id`);
ALTER TABLE `resources_book_authors` ADD CONSTRAINT `resources_book_authors_book_id_user_id_2bc6be29_uniq` UNIQUE (`book_id`, `user_id`);
ALTER TABLE `resources_book_authors` ADD CONSTRAINT `resources_book_authors_book_id_ff263faf_fk_resources_book_id` FOREIGN KEY (`book_id`) REFERENCES `resources_book` (`id`);
ALTER TABLE `resources_book_authors` ADD CONSTRAINT `resources_book_authors_user_id_746d8c18_fk_accounts_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_user` (`id`);
ALTER TABLE `resources_book_tags` ADD CONSTRAINT `resources_book_tags_book_id_tag_id_9cc81e0a_uniq` UNIQUE (`book_id`, `tag_id`);
ALTER TABLE `resources_book_tags` ADD CONSTRAINT `resources_book_tags_book_id_af5350ab_fk_resources_book_id` FOREIGN KEY (`book_id`) REFERENCES `resources_book` (`id`);
ALTER TABLE `resources_book_tags` ADD CONSTRAINT `resources_book_tags_tag_id_79151059_fk_resources_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `resources_tag` (`id`);
