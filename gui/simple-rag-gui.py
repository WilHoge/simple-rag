# load utils helper functions
import sys
sys.path.append("../utils")
import wxd_utils

# load config
conf=wxd_utils.load_conf()
print(conf)

# initialize Milvus
from pymilvus import(
    Milvus,
    IndexType,
    Status,
    connections,
    FieldSchema,
    DataType,
    Collection,
    CollectionSchema,
)

connections.connect(alias = 'default',
                host = conf["host"],
                port = conf["milvus_port"],
                user = conf["user"],
                password = conf["password"],
                server_pem_path = conf["lh_cert"],
                server_name = conf["host"],
                secure = True)

basic_collection = Collection("wiki_articles")      
basic_collection.load()

# load embedding
embedding = wxd_utils.load_embedding_model(conf, 'ibm/slate-125m-english-rtrvr')



import streamlit as st

def run_gui(deployment, question):
    text_input = st.text_area("Enter your question", value=question, height=100)

    if st.button("Ask LLM"):
        st.write("Asking LLM...")
        prompt = text_input
        result = wxd_utils.ask_llm_prompt(prompt, deployment)
        st.text_area("Result:", value=result, height=200, disabled=True)
        st.text_area("Prompt:", value=prompt, height=100, disabled=True)
        st.write(f"Model: {deployment['name']}")

    st.write("")

def run_gui_with_context(deployment, question, context):
    st.write("Context:")
    context_text = st.text_area("Context", value=context, height=100)

    text_input = st.text_area("Enter your question", value=question, height=100)

    if st.button("Ask LLM"):
        st.write("Asking LLM...")
        prompt = wxd_utils.make_prompt([context_text], text_input)
        st.text_area("Prompt:", value=prompt, height=100, disabled=True)
        result = wxd_utils.ask_llm_prompt(prompt, deployment)
        st.text_area("Result:", value=result, height=200, disabled=True)
        st.write(f"Model: {deployment['name']}")

    st.write("")

def run_gui_with_rag(deployment, embedding, basic_collection, question):
    text_input = st.text_area("Enter your question", value=question, height=100)

    if st.button("Ask LLM"):
        try:
            context = wxd_utils.query_milvus_chunks(text_input, embedding, basic_collection)
            st.text_area("Context", value="\n\n".join(context), height=200, disabled=True)
            st.write("Asking LLM...")
            prompt = wxd_utils.make_prompt(context, text_input)
            st.text_area("Prompt:", value=prompt, height=100, disabled=True)
            result = wxd_utils.ask_llm_prompt(prompt, deployment)
            st.text_area("Result:", value=result, height=200, disabled=True)
            st.write(f"Model: {deployment['name']}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.title("Test App for LLM improvement by using RAG")

col1, col2 = st.columns(2)

with col1:
    model_option = st.radio("Select LLM", ["granite-13b-chat", "llama-2-70b-chat", "llama-3-405b-instruct", "mixtral-8x7b-instruct", "llama3-70b-instruct"])
    deployment = wxd_utils.load_model_deployment(conf, model_option)
    print(deployment)

with col2:
    options = ["Just LLM", "LLM with context", "LLM with RAG"]
    selected_option = st.radio("Select an option", options)

if selected_option == "Just LLM":
    run_gui (deployment, conf["default_query"])
elif selected_option == "LLM with context":
    import wikipedia
    article = wikipedia.page(pageid=72508137)
    run_gui_with_context (deployment, conf["default_query"], article.content)
elif selected_option == "LLM with RAG":
    run_gui_with_rag (deployment, embedding, basic_collection, conf["default_query"])
else:
    st.write("")
