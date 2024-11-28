-- 001_create_documents_table.sql

-- Create the "documents" table
CREATE TABLE documents (
    id bigserial PRIMARY KEY,
    model text NOT NULL,
    source_uri text NOT NULL,
    embedding vector(1024) NOT NULL
);
