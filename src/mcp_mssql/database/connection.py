from sqlalchemy import create_engine, event
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import sessionmaker
import structlog
from mcp_mssql.config import settings

log = structlog.get_logger(__name__)

def build_connection_url() -> str:
    driver = settings.MSSQL_DRIVER.replace(" ", "+")
    encrypt = "yes" if settings.MSSQL_ENCRYPT else "no"
    trust = "yes" if settings.MSSQL_TRUST_SERVER_CERT else "no"
    return (
        f"mssql+pyodbc://{settings.MSSQL_USERNAME}:{settings.MSSQL_PASSWORD}"
        f"@{settings.MSSQL_SERVER},{settings.MSSQL_PORT}/{settings.MSSQL_DATABASE}"
        f"?driver={driver}&Encrypt={encrypt}&TrustServerCertificate={trust}"
    )

engine = create_engine(
    build_connection_url(),
    poolclass=QueuePool,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.POOL_MAX_OVERFLOW,
    pool_timeout=settings.POOL_TIMEOUT,
    pool_recycle=settings.POOL_RECYCLE,
    pool_pre_ping=True,
    echo=False,
    connect_args={"timeout": settings.QUERY_TIMEOUT},
)

@event.listens_for(engine, "connect")
def on_connect(dbapi_conn, _):
    log.info("db.connection.established")

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)