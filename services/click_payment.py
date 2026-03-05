import hashlib
from config import CLICK_SECRET_KEY

def generate_click_signature(data: dict):
    sign_string = f"{data['click_trans_id']}{data['service_id']}{CLICK_SECRET_KEY}"
    return hashlib.md5(sign_string.encode()).hexdigest()