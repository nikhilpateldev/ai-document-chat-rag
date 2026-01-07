from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Document Chat RAG"
    OLLAMA_URL: str = "http://localhost:11434"
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 100

    class Config:
        env_file = ".env"

settings = Settings()
