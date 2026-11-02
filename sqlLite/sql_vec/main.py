import sqlite3
import sqlite_vec
import ollama

db = sqlite3.connect(":memory:")
db.enable_load_extension(True)


sqlite_vec.load(db)

db.execute("CREATE VIRTUAL TABLE data USING vec0(embedding float[1024], +text TEXT)")


def embed_text(text):
    return ollama.embed(model="mxbai-embed-large:latest", input=text)["embeddings"]


texts = [
    "Python is aesome!",
    "SQLite is aesome!",
    "Oranges are aesome!",
    "Apples are great!",
    "I like Linux",
]

for text in texts:
    db.execute(
        "INSERT INTO data(text, embedding) VALUES (?, ?)",
        (text, sqlite_vec.serialize_float32(embed_text(text))),
    )

query = "I like Bananas!"

for row in db.execute(
    "SELECT text, distance FROM data WHERE embedding MATCH ? AND k = 2",
    (sqlite_vec.serialize_float32(embed_text(query))),
):
    print(row)
