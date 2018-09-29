from flask import Flask

app = Flask(__name__)

from app import views

app.config['JWT_SECRET_KEY'] = 'sec-def-oscar-zulu-3-zero-niner'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
from flask_jwt_extended import JWTManager
jwt = JWTManager(app)

blacklist = set()
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist        

