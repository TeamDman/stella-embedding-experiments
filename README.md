
https://www.reddit.com/r/singularity/comments/1gyu5ud/help_fastest_reliable_embedding_model_for_300gb/lyv1jic/

https://huggingface.co/dunzhang/stella_en_400M_v5

https://github.com/pgvector/pgvector#conda-forge

# env

```pwsh
conda create -n hf python=3.10 -y
conda activate hf
conda install pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
pip install transformers
pip install numpy scipy scikit-learn
pip install sentence-transformers
pip3 install -U xformers --index-url https://download.pytorch.org/whl/cu124
conda install -c conda-forge pgvector
conda install -c conda-forge postgresql
pip install psycopg2

```

```
$Env:XFORMERS_FORCE_DISABLE_TRITON=1
```

# pgvector

```sql
postgres=# \c mydb
You are now connected to database "mydb" as user "Teamy".
mydb=# CREATE EXTENSION vector;
CREATE EXTENSION
mydb=# CREATE TABLE items (id bigserial PRIMARY KEY, embedding vector(3));
CREATE TABLE
mydb=# INSERT INTO items (embedding) VALUES ('[1,2,3]'),('[4,5,6]');       
INSERT 0 2
mydb=# SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;       
 id | embedding
----+-----------
  1 | [1,2,3]
  2 | [4,5,6]
(2 rows)

```