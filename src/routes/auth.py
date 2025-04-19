from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from src.db.users import users_db
from src.schemas.users import UserCreate
from src.utils.security import get_password_hash, verify_password, encode_token


auth_router = APIRouter()


@auth_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> JSONResponse:
    """ Endpoint para que un usuario inicie sesión.
    
    Argumento:
        form_data: Dependencia de FastAPI que extrae el "username" y "password" de un formulario enviado por el frontend.
    
    Retorno:
        JSONResponse: JSON con el status code y el Token con la información del usuario.
    """
    try: 
        user = users_db.search_by_username(form_data.username) # buscar al usuario en bd
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error en el servidor..."
        )
    
    if not user: # Si el usuario no se encuentra en bd:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "El usuario no existe en la base de datos."
        )

    # Validación de contraseñas:
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Las contraseñas no coinciden."
        )

    # Si todos los datos de usuario son correctos:    
    token = encode_token({"username": user["username"], "email": user["email"]}) # generar token
    return JSONResponse(
        status_code = status.HTTP_202_ACCEPTED,
        content = {"access_token": token}
    )


@auth_router.post("/register")
async def register(user_data: UserCreate) -> JSONResponse:
    """Endpoint para que un usuario se registre.

    Argumentos:
        user_data (UserCreate): Datos del usuario tipados bajo el esquema Pydantic
        para realizar validaciones antes de registrar el usuario.

    Retorna:
        JSONResponse: JSON con el status code y un mensaje para el frontend.
    """
    # Validaciones:
    if users_db.search_by_username(user_data.username): 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Ya existe un usuario con ese nombre en la base de datos."
        )
    elif users_db.search_by_email(user_data.email):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Ya existe un usuario con ese email en la base de datos."
        )
    
    hashed_password = get_password_hash(user_data.password) # hashear a la contraseña
    user_data.password = hashed_password # reasignar la contraseña con la encriptada

    try:
        users_db.create(user_data) # crear el usuario en la base de datos
        return JSONResponse(
            status_code = status.HTTP_201_CREATED,
            content = {"detail": "Usuario registrado correctamente."}
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Ha ocurrido un error al momento de registrar el usuario..."
        )