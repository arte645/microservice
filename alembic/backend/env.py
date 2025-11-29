import asyncio
import sys
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import pool
from alembic import context

# ------------------ Пути ------------------
ROOT = Path(__file__).resolve().parents[3]
BACKEND_MODELS = ROOT / "src" / "backend" / "models"
sys.path.append(str(BACKEND_MODELS))

# ------------------ Импорты моделей ------------------
from src.backend.models import *

# ------------------ Alembic config ------------------
config = context.config
fileConfig(config.config_file_name)

import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("BACKEND_DATABASE_URL")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ------------------ Миграции ------------------
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable: AsyncEngine = create_async_engine(
        DATABASE_URL, poolclass=pool.NullPool
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
