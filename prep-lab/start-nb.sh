# start jupyter notebooks
. ~labuser/venv/bin/activate
nohub jupyter notebook > ~labuser/simple-rag/logs/jupyter-notebook.log 2>~labuser/simple-rag/logs/jupyter-notebook.err & 