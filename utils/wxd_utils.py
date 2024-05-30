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
        f"presto://{config.user}:{config.password}@{config.host}:{config.lh_port}/{config.lh_catalog}/{config.lh_schema}",
        connect_args={
            'protocol': 'https', 
            'requests_kwargs': {'verify': ssl.CERT_NONE }
            }
        )

    return quick_engine