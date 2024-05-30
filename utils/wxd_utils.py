def load_conf():
    import os
    from dotenv import load_dotenv

    load_dotenv('../utils/config.env')

    # Load config from environment
    config = {
        api_key : os.getenv("API_KEY", None),
        ibm_cloud_url : os.getenv("IBM_CLOUD_URL", None),
        project_id : os.getenv("PROJECT_ID", None),
    }
    
    return(config)

def connect_wxd(config):
    return