from config.autodl import sd_localDeployment as config

class sd_config:
    url = f"http://0.0.0.0:{config.LOCAL_PORT}"
    steps = 23
    cfg_scale = 7
    width = 1024
    height = 1024
    send_images = True
    seed = -1
    self_attention = "yes"