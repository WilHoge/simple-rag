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
        "milvus_port": os.getenv("MILVUS_PORT", "19530")
    }

    return(config)

def connect_wxd(config):
    return