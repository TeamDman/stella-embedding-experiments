import os
os.environ["XFORMERS_FORCE_DISABLE_TRITON"] = "1"
from transformers import logging
logging.set_verbosity_error()
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
        SELECT source_uri, embedding <-> %s::vector AS similarity
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
            for rank, (source_uri, similarity) in enumerate(results, start=1):
                print(f"{rank}. {source_uri} (similarity: {similarity:.4f})")
            print()
        else:
            print("No results found.\n")

if __name__ == "__main__":
    main()
