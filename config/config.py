from pydantic_settings import BaseSettings, SettingsConfigDict

# To use the settings, you can import the `settings` object from this module.
# It will automatically load the environment variables from the .env file.

class Settings(BaseSettings):

    # Database settings
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DATABASE_URL: str

    # API settings
    DB_USAGE: bool
    API_VERSION: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=True,
        env_file_required=True
    )

settings = Settings()
if __name__ == "__main__":
    print(settings.model_dump())