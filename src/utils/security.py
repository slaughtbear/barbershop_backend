from typing import Annotated

import jwt
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.db.config import config
from src.db.users import users_db
# from src.schemas.users import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encode_token(payload: dict) -> str:
    """ Genera un token a partir de la información del usuario.
    
    Argumentos:
        payload (Dict): Diccionario con los datos del usuario.

    Retorna:
        str: El token generado para el usuario.
    """
    token: str = jwt.encode(payload, config.SECRET_KEY, config.ALGORITHM)
    return token


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    """ Decodifica un token y retorna la información del usuario.
    
    Argumentos
        token (str): El token del usuario.

    Retorna:
        Dict: Diccionario con la información del usuario.
    """
    data: dict = jwt.decode(token, config.SECRET_KEY, algorithms = [config.ALGORITHM])
    user: dict = users_db.search_by_username(data["username"])
    return user


def get_password_hash(password: str) -> str:
    """ Recibe una contraseña en texto plano y la encripta.

    Argumentos:
        password (str): Contraseña en texto plano.

    Retorna:
        str: La contraseña encriptada.

    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Compara una contraseña en texto plano con la contraseña con hash, verifica que coincidan, si es así se retorna True.

    Argumentos:
        plain_password (str): Contraseña en texto plano.
        hashed_password (str): Contraseña con hash.

    Retorna:
        bool: True si coinciden, False si no coinciden.
    """
    return pwd_context.verify(plain_password, hashed_password)