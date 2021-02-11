-- rename tables 
ALTER TABLE database_name.`resources_category`
RENAME TO database_name.`core_category`;

ALTER TABLE database_name.`resources_tag`
RENAME TO database_name.`core_tag`;

ALTER TABLE database_name.`resources_book`
RENAME TO database_name.`core_book`;

ALTER TABLE database_name.`resources_video`
RENAME TO database_name.`core_video`;

ALTER TABLE database_name.`resources_book_authors`
RENAME TO database_name.`core_book_authors`;

ALTER TABLE database_name.`resources_book_tags`
RENAME TO database_name.`core_book_tags`;

ALTER TABLE database_name.`resources_video_authors`
RENAME TO database_name.`core_video_authors`;

ALTER TABLE database_name.`resources_video_tags`
RENAME TO database_name.`core_video_tags`;

-- set the id value to the rows with the information about
-- when `resources` migrations were run
SELECT *
FROM database_name.`django_migrations`
WHERE app='resources';

UPDATE database_name.`django_migrations`
SET app='core'
WHERE id IN (list_ids_of_resources_migrations);
