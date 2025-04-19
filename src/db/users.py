from src.db.config import supabase
from src.schemas.users import UserCreate

class UsersDB:
    def search_by_username(self, username: str) -> dict | None:
        response: dict = (
            supabase.table("users")
            .select("*")
            .eq("username", username)
            .execute()
        )
        return response.data[0] if response.data else None
    
    def search_by_email(self, email: str) -> dict | None:
        response: dict = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )
        return response.data[0] if response.data else None
    
    def create(self, user_data: UserCreate) -> dict:
        return (
            supabase.table("users")
            .insert(user_data.model_dump())
            .execute()
        )

users_db = UsersDB()