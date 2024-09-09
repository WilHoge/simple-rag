
import sys
sys.path.append("../utils")
import wxd_utils

conf=wxd_utils.load_conf()
print(conf)

# call without a model_id to learn what models are available
# wxd_utils.load_model_deployment(conf, '')

deployment = wxd_utils.load_model_deployment(conf, 'granite-13b-chat')
print(deployment)

import streamlit as st

def run_gui(deployment, question):
    text_input = st.text_area("Enter your question", value=question, height=100)

    if st.button("Ask LLM"):
        st.write("Asking LLM...")
        prompt = text_input
        result = wxd_utils.ask_llm_prompt(prompt, deployment)
        st.write("Answer:")
        st.text_area("Result", value=result, height=200, disabled=True)
        st.write("Prompt:")
        st.text_area("Prompt", value=prompt, height=100, disabled=True)
        st.write(f"Model: {deployment['name']}")

    st.write("")


st.title("Test App for LLM improvement by using and RAG")

options = ["Just LLM", "LLM with context", "LLM with RAG"]
selected_option = st.radio("Select an option", options)

if selected_option == "Just LLM":
    st.write("You selected Option 1!")
    run_gui (deployment, conf["default_query"])
elif selected_option == "LLM with context":
    st.write("You selected Option 2!")
elif selected_option == "LLM with RAG":
    st.write("option3")
else:
    st.write("You selected Option 3!")



