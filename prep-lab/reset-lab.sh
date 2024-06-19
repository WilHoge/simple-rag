# this script initializes the environment and resets the lab

# 1. clean lab directory and reload from git
sudo rm -rf ~labuser/simple-rag
sudo su - labuser -c "git clone https://github.com/WilHoge/simple-rag.git"

# 2. install the required python libraries
sudo su - labuser -c ~labuser/simple-rag/prep-lab/install-python-requirements.sh

# 3. start the jupyter notebooks
sudo su - labuser -c ~labuser/simple-rag/prep-lab/start-nb.sh

# 4. (re-)start the watsonx.data engine
sudo ~labuser/simple-rag/install/stop-wxd.sh
sudo ~labuser/simple-rag/install/start-wxd.sh

# 5. delete data from Presto tables and Milvus collection
sudo su - labuser -c ~labuser/simple-rag/prep-lab/remove-data.sh

# 6. delete data in Minio
/usr/local/bin/mc rm --recursive --force myminio/iceberg-bucket/simple_rag