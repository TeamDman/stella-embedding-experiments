import sys
import psycopg2
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
model = SentenceTransformer("dunzhang/stella_en_400M_v5", trust_remote_code=True).cuda()

# Function to read the file and extract URLs
def extract_urls(file_path):
    urls = []
    with open(file_path, "r", encoding="utf-8") as file:  # Specify UTF-8 encoding
        for line in file:
            if "http" in line:  # Basic heuristic to detect URLs
                url = line.strip()
                urls.append(url)
    return urls


# Function to insert embeddings into the database
def insert_embeddings(urls, source_uri):
    try:
        # Generate embeddings
        embeddings = model.encode(urls).tolist()

        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Insert each embedding
        model_name = "dunzhang/stella_en_400M_v5"
        for url, embedding in zip(urls, embeddings):
            cursor.execute(
                """
                INSERT INTO documents (model, source_uri, embedding)
                VALUES (%s, %s, %s)
                """,
                (model_name, source_uri, embedding),
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
    source_uri = f"file://{file_path}"  # Convert file path to URI

    # Extract URLs and insert embeddings
    urls = extract_urls(file_path)
    if urls:
        print(f"Found {len(urls)} URLs in the file. Processing...")
        insert_embeddings(urls, source_uri)
    else:
        print("No URLs found in the file.")

if __name__ == "__main__":
    main()
