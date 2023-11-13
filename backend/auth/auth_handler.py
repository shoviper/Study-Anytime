import time
import jwt

SECRET_KEY = "4cb39b4e3b4034b4ad19c8d5dec5293a"
ALGORITHM = "HS256"

def token_response(token: str):
    return{
        "access_token" : token
    }
    
def signJWT(id: str, role: str):
    payload = {
        "id" : id,
        "role" : role,
        "exp" : time.time() + 2628000
    }
    
    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return decode_token if decode_token["exp"] >= time.time() else None
    except:
        return None