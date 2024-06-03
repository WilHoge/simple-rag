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
        "milvus_port": os.getenv("MILVUS_PORT", "19530"),
        "default_query": os.getenv("DEFAULT_QUERY", "Who is Jon Fosse?")
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

def load_model(conf, model_id):
    #        model_id='meta-llama/llama-2-70b-chat'
    #        model_id='mistralai/mixtral-8x7b-instruct-v01'

    logger.info(f"load_model> model_id: {model_id}")

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

    try:
        model = Model(model_id=model_id, 
            params=params, credentials=creds, 
            project_id=conf["project_id"]
        )
        return model
    except Exception as e:
        logger.error(f"load_model> error loading model: {str(e)}")
        print(f"load_model> error loading model: {str(e)}")

    return None

# Prompt LLM
def ask_llm(prompt, model):
    logger.info(f"ask_llm> Call model with {prompt}")
    response = model.generate_text(prompt)
    logger.info(f"ask_llm>\nQuestion: {prompt}\nResponse: {response}")
    return response

def make_prompt(context, question_text):
    logger.info(f"make_prompt>\ncontext: {context}\nquestion: {question}")
    context = "\n\n".join(context)
    prompt = (f"{context}\n\nPlease answer a question using this text. "
          + f"If the question is unanswerable, say \"unanswerable\"."
          + f"\n\nQuestion: {question_text}")
    logger.info(f"make_prompt>\nprompt: {prompt}")
    return prompt

def run_gui(model, question):
    from ipywidgets import widgets

    text_input = widgets.Textarea(value=question, disabled=False)
    result_text = widgets.Textarea(value='', disabled=True)
    prompt_text = widgets.Textarea(value='', disabled=True)

    def on_click(b):
        logger.info(f"run_gui/on_click> You clicked the button! {text_input.value}")
        result_text.value = "asking LLM ..."
        prompt = text_input.value
        prompt_text.value = prompt
        result_text.value = ask_llm(prompt, model)

    button = widgets.Button(description='Ask LLM');
    button.on_click(on_click)

    input_box  = widgets.Box([widgets.Label('Your question!'), text_input, button, widgets.Label(f"model: {model.model_id}")])
    result_box = widgets.Box([widgets.Label('Answer:'), result_text])
    prompt_box = widgets.Box([widgets.Label('Prompt:'), prompt_text])

    box = widgets.VBox(children=[input_box , prompt_box, result_box])

    result_text.layout.width = '100%'
    result_text.layout.height = '200px'
    prompt_text.layout.width = '100%'

    display(box)

def write_log(level, text):
    if level == 'INFO':
        logger.info(text)
    elif level == 'ERROR':
        logger.error(text)
    else:
        logger.info(text)

# initialize logging
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('../logs/simple-rag.log', mode='a', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)