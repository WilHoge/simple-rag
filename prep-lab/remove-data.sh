# initialize Python
. ~labuser/venv/bin/activate

cd ~labuser/simple-rag/prep-labs

# delete data from Presto and Milvus
python ~labuser/prep-lab/remove-data.py