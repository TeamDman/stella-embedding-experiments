import os
os.environ["XFORMERS_FORCE_DISABLE_TRITON"] = "1"
from transformers import logging
logging.set_verbosity_error()

import sys
import psycopg2
from psycopg2.extras import Json  # Import Json adapter
from sentence_transformers import SentenceTransformer

# Database connection settings
DB_CONFIG = {
    "dbname": "mydb",
    "user": "Teamy",  # Replace with your PostgreSQL username
    "password": "",  # Replace with your password
    "host": "localhost",
    "port": 5432,
}

# Initialize the model
print("Loading model, please be patient...")
model = SentenceTransformer("dunzhang/stella_en_400M_v5", trust_remote_code=True).cuda()

# Function to read the file and extract URLs with byte ranges
def extract_urls_with_ranges(file_path):
    urls = []
    ranges = []
    current_pos = 0

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line_length = len(line.encode("utf-8"))  # Ensure consistent byte length
            if "http" in line:  # Basic heuristic to detect URLs
                url = line.strip()
                start_pos = current_pos  # Byte position of the start
                end_pos = current_pos + line_length  # Byte position of the end
                urls.append(url)
                ranges.append({"start": start_pos, "end": end_pos})  # JSON-friendly range
            current_pos += line_length  # Update current position

    return urls, ranges

# Function to insert embeddings into the database
def insert_embeddings(urls, ranges, source_uri):
    try:
        # Generate embeddings
        embeddings = model.encode(urls).tolist()

        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert each embedding
        model_name = "dunzhang/stella_en_400M_v5"
        modality = "text"  # Set modality to text
        for (url, embedding, byte_range) in zip(urls, embeddings, ranges):
            cursor.execute(
                """
                INSERT INTO documents (model, modality, file, range, embedding)
                VALUES (%s, %s, %s, %s::jsonb, %s)
                """,
                (model_name, modality, source_uri, Json(byte_range), embedding),
            )

        # Commit the transaction
        conn.commit()
        print(f"Inserted {len(urls)} URLs into the database.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage: python insert_browser_tabs.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Extract URLs and byte ranges
    urls, ranges = extract_urls_with_ranges(file_path)
    if urls:
        print(f"Found {len(urls)} URLs in the file. Processing...")
        insert_embeddings(urls, ranges, file_path)
    else:
        print("No URLs found in the file.")

if __name__ == "__main__":
    main()
