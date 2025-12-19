DROP SCHEMA IF EXISTS pg CASCADE;
CREATE SCHEMA pg;
SET search_path = pg;

-- Create table
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    book_data xml
);

-- Insert more complex XML data
INSERT INTO books (book_data) VALUES
(xmlparse(DOCUMENT '<?xml version="1.0"?><book><title>Python Programming</title><author>John Doe</author><year>2023</year><publisher>O''Reilly Media</publisher><isbn>978-1-4919-4529-4</isbn></book>')),
(xmlparse(DOCUMENT '<?xml version="1.0"?><book><title>Java Programming</title><author>Jane Smith</author><year>2022</year><publisher>Addison-Wesley</publisher><isbn>978-0-13-468599-1</isbn></book>'));

-- Query more complex XML data with a condition
SELECT 
    (xpath('/book/title/text()', book_data))[1]::text AS title,
    (xpath('/book/author/text()', book_data))[1]::text AS author,
    (xpath('/book/year/text()', book_data))[1]::text AS year,
    (xpath('/book/publisher/text()', book_data))[1]::text AS publisher,
    (xpath('/book/isbn/text()', book_data))[1]::text AS isbn
FROM books
WHERE (xpath('/book/year/text()', book_data))[1]::text = '2023';

-- Clean up data (optional)
-- DELETE FROM books;
-- DROP TABLE books;
