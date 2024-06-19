# kill previous instances of jupyter notebooks
kill $(ps aux|fgrep bin/jupyter-notebook|awk '{print $2}')

# start jupyter notebooks
. ~labuser/venv/bin/activate
nohup jupyter notebook 1>~labuser/simple-rag/logs/jupyter-notebook.log 2>&1 & 