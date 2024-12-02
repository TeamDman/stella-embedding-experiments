import os
os.environ["XFORMERS_FORCE_DISABLE_TRITON"] = "1"
from transformers import logging
logging.set_verbosity_error()
import psycopg2
from sentence_transformers import SentenceTransformer
import json

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

def get_top_results(prompt, top_n=5):
    try:
        # Generate embedding for the prompt
        prompt_embedding = model.encode([prompt]).tolist()[0]

        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Query to calculate similarity and get the top results
        query = """
        SELECT file, range::text, embedding <-> %s::vector AS similarity
        FROM documents
        ORDER BY similarity ASC
        LIMIT %s;
        """
        cursor.execute(query, (prompt_embedding, top_n))

        # Fetch results
        results = cursor.fetchall()
        return results

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def read_file_segment(file_path, byte_range):
    """
    Reads a specific segment of a file based on a byte range.
    Expands the range to capture complete lines.
    """
    start = byte_range["start"]
    end = byte_range["end"]

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            # Seek to start position
            file.seek(start)

            # Skip incomplete line at the start (if not at the beginning)
            if start > 0:
                file.readline()  # Move to the start of the next line

            # Read until the end position
            content = ""
            while file.tell() < end:
                line = file.readline()
                if not line:  # End of file
                    break
                content += line

            return content
    except Exception as e:
        print(f"Error reading file segment: {e}")
        return "[Error reading file segment]"


def main():
    print("Query System: Enter a prompt to get the top 5 results (type 'exit' to quit).")

    while True:
        # Get user input
        prompt = input("Enter your prompt: ")
        if prompt.lower() == "exit":
            print("Exiting query system.")
            break

        # Get top results
        results = get_top_results(prompt)
        if results:
            print("\nTop Results:")
            for rank, (file_path, byte_range, similarity) in enumerate(results, start=1):
                # Convert range from JSONB (Postgres) to Python dictionary
                byte_range = json.loads(byte_range)  # Parse JSON string into a Python dict
                content = read_file_segment(file_path, byte_range)

                print(f"{rank}. File: {file_path}")
                print(f"   Similarity: {similarity:.4f}")
                print(f"   Content:\n{content.strip()}\n")
        else:
            print("No results found.\n")

if __name__ == "__main__":
    main()
