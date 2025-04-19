import os
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()


class Config:
    """
    Clase de configuración global que sirve para almacenar variables de entorno como atributos y acceder a ellas mediante un objeto.
    """
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")


config = Config()


if not all ([config.SUPABASE_URL, config.SUPABASE_KEY]):
    raise EnvironmentError("No se ha detectado una o más variables de entorno...")


supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)