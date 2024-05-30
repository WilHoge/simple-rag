def load_conf():
    import os
    from dotenv import load_dotenv

    load_dotenv('../utils/config.env')

    # Load config from environment
    config = {
        "api_key" : os.getenv("API_KEY", None),
        "ibm_cloud_url" : os.getenv("IBM_CLOUD_URL", None),
        "project_id" : os.getenv("PROJECT_ID", None),
        "host" : os.getenv("LH_HOST_NAME", "localhost"),
        "user" : os.getenv("LH_USER", "ibmlhadmin"),
        "password" : os.getenv("LH_PW", "password"),
        "lh_port": os.getenv("LH_PORT", "8443"),
        "lh_cert": os.getenv("LH_CERT", "/wxd-install/ibm-lh-dev/localstorage/volumes/infra/tls/cert.crt"),
        "lh_schema": os.getenv("LH_SCHEMA", "tiny"),
        "lh_catalog": os.getenv("LH_CATALOG", "tpch"),
        "milvus_port": os.getenv("MILVUS_PORT", "19530")
    }

    return(config)

def connect_wxd(config):

    import ssl
    import urllib3
    import os
    from sqlalchemy import create_engine
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # disable https warning

    quick_engine = create_engine(
        f'presto://{config["user"]}:{config["password"]}@{config["host"]}:{config["lh_port"]}/{config["lh_catalog"]}/{config["lh_schema"]}',
        connect_args={
            'protocol': 'https', 
            'requests_kwargs': {'verify': ssl.CERT_NONE }
            }
        )

    return quick_engine

def get_token(conf):

    from ibm_cloud_sdk_core import IAMTokenManager

    access_token = IAMTokenManager(
        apikey = api_key,
        url = "https://iam.cloud.ibm.com/identity/token"
    ).get_token()

    return access_token

def load_model(model_id)
    #        model_id='meta-llama/llama-2-70b-chat'
    #        model_id='mistralai/mixtral-8x7b-instruct-v01'

    from ibm_watson_machine_learning.foundation_models import Model
    from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

    creds = {
        "url": conf["ibm_cloud_url"],
        "apikey": conf["api_key"] 
    }

    # Model Parameters
    params = {
        GenParams.DECODING_METHOD: "greedy",
        GenParams.MIN_NEW_TOKENS: 1,
        GenParams.MAX_NEW_TOKENS: 500,
        GenParams.TEMPERATURE: 0,
    }

    model = Model(model_id=model_id, 
        params=params, credentials=creds, 
        project_id=project_id
    )

    return model

# Prompt LLM
def ask_llm(prompt, model):
        response = model.generate_text(prompt)
        #print(f"Question: {question_text}{response}")
        return response

def make_prompt(context, question_text):
    context = "\n\n".join(context)
    return (f"{context}\n\nPlease answer a question using this text. "
          + f"If the question is unanswerable, say \"unanswerable\"."
          + f"\n\nQuestion: {question_text}")