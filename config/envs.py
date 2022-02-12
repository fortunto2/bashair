from typing import Optional
from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    DEBUG: bool = False

    DOMAIN_API: str = "air.localhost"
    DOMAIN_INFLUX: str = "panel.localhost"

    SENTRY: str = None

    # DJANGO_SETTINGS_MODULE: str = "config.settings"

    TIMEZONE: str = "Europe/Moscow"
    MEASUREMENT_NAME: str = "air"
    TELEGRAM_TOKEN: Optional[str]

    POSTGRES_PORT: int = 5432
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    INFLUXDB_USERNAME: str
    INFLUXDB_PASSWORD: str

    INFLUXDB_V2_URL: str = 'http://localhost:8086'
    INFLUXDB_V2_ORG: str = 'zenpulsar'
    INFLUXDB_V2_TOKEN: str = 'token'

    OWM_KEY: str

    # INFLUXDB_V2_URL - the url to connect to InfluxDB
    # INFLUXDB_V2_ORG - default destination organization for writes and queries
    # INFLUXDB_V2_TOKEN - the token to use for the authorization
    # INFLUXDB_V2_TIMEOUT - socket timeout in ms (default value is 10000)
    # INFLUXDB_V2_VERIFY_SSL - set this to false to skip verifying SSL certificate when calling API from https server
    # INFLUXDB_V2_SSL_CA_CERT - set this to customize the certificate file to verify the peer

    # MONGO_DB: str
    # MONGO_USER: str
    # MONGO_PASSWORD: str
    # MONGO_HOST: str = 'db'
    # MONGO_PORT: Optional[int] = 27017
    # MONGO_DATABASE_URI: Optional[MongoDsn] = None
    #
    # @validator("MONGO_DATABASE_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return MongoDsn.build(
    #         scheme="mongodb",
    #         user=values.get("MONGO_USER"),
    #         password=values.get("MONGO_PASSWORD"),
    #         host=values.get("MONGO_HOST"),
    #         port=str(values.get("MONGO_PORT"))
    #     )


    class Config:
        case_sensitive = True
        env_file = ".env"


envs = EnvSettings()

