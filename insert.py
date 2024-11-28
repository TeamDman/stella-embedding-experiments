from sentence_transformers import SentenceTransformer
import psycopg2

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

# Documents to encode
docs = [
    {
        "text": "There are many effective ways to reduce stress. Some common techniques include deep breathing, meditation, and physical activity. Engaging in hobbies, spending time in nature, and connecting with loved ones can also help alleviate stress. Additionally, setting boundaries, practicing self-care, and learning to say no can prevent stress from building up.",
        "source_uri": "https://example.com/stress-reduction",
    },
    {
        "text": "Green tea has been consumed for centuries and is known for its potential health benefits. It contains antioxidants that may help protect the body against damage caused by free radicals. Regular consumption of green tea has been associated with improved heart health, enhanced cognitive function, and a reduced risk of certain types of cancer. The polyphenols in green tea may also have anti-inflammatory and weight loss properties.",
        "source_uri": "https://example.com/green-tea-benefits",
    },
    {
        "text": "penis",
        "source_uri": "https://example.com/placeholder",
    },
]

# Model used for embedding generation
model_name = "dunzhang/stella_en_400M_v5"

# Generate embeddings
texts = [doc["text"] for doc in docs]
embeddings = model.encode(texts).tolist()  # Convert to Python list for psycopg2

# Insert embeddings into PostgreSQL
try:
    # Connect to the database
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Insert each embedding
    for doc, embedding in zip(docs, embeddings):
        cursor.execute(
            """
            INSERT INTO documents (model, source_uri, embedding)
            VALUES (%s, %s, %s)
            """,
            (model_name, doc["source_uri"], embedding),
        )

    # Commit the transaction
    conn.commit()
    print("Embeddings inserted successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Clean up
    if cursor:
        cursor.close()
    if conn:
        conn.close()
