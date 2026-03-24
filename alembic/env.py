import os
import json
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ============================
# Load Azure local.settings.json
# ============================
def load_local_settings():
    """
    Load Azure Functions local.settings.json into environment variables
    so Alembic (CLI) can access them.
    """
    path = Path("local.settings.json")

    if path.exists():
        with open(path) as f:
            data = json.load(f)
            values = data.get("Values", {})

            for key, value in values.items():
                os.environ.setdefault(key, value)


# MUST run before importing app config
load_local_settings()


from app.core.database import Base
from app.models import content, cleaned_content
from app.core.config import settings


config = context.config

# Inject DB URL dynamically
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata



def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()



def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================
# Entry point
# ============================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()