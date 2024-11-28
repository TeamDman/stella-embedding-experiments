-- Migration: Rename source_uri to file, make it nullable, and clean up invalid entries

-- Step 1: Rename the column from source_uri to file
ALTER TABLE documents RENAME COLUMN source_uri TO file;

-- Step 2: Make the file column nullable
ALTER TABLE documents ALTER COLUMN file DROP NOT NULL;

-- Step 3: Remove rows where file does not start with 'file://'
DELETE FROM documents WHERE file NOT LIKE 'file://%';

-- Step 4: Remove the 'file://' prefix from the file column
UPDATE documents
SET file = REGEXP_REPLACE(file, '^file://', '');
