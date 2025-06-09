# 010. SQL Models defined in SQLAlchemy/Alembic

Status: proposed

Authors: Josh Holland

Date: 2025-06-09

## Context and Problem Statement

As we build more components making use of a PostgreSQL database, where
can we store schema definitions so that they are reusable across
projects?  What's the best client library to query the database?

## Decision Drivers

- Standard tools where possible
- Python compatibility
- Avoid manually running `ALTER TABLE` etc commands by hand
- Avoid lock-in: the solution should not be too opinionated so that we
  can use other languages/tools to access the database

## Considered Options

- [SQLAlchemy][] declarative models in centralised repo + [Alembic][]
- SQLAlchemy models defined as part of each application
- SQLAlchemy core with hand-written marshalling to/from model
  classes in each application + Alembic
- [SQLModel][] from Tiangelo

[SQLAlchemy]: https://www.sqlalchemy.org/
[SQLModel]: https://sqlmodel.tiangolo.com/
[Alembic]: https://alembic.sqlalchemy.org/

## Decision Outcome

Chosen option: SQLAlchemy declarative models with Alembic in a
[centralised repo][models repo] because it is a relatively
light-weight solution that still provides many features.  There do not
appear to be any realistic alternatives to Alembic for managing
migrations.

[models repo]: https://github.com/NERC-CEH/dri-database-models

### Positive Consequences

- One repo holds the full source of truth for all the database models
  and configuration
- Database migration is handled by code which can be
  version-controlled

### Negative Consequences

- One more repo to keep track of
- Need to keep central models repo and downstream application repos in
  sync

### Pros and Cons of the Options

#### SQLAlchemy declarative models in central repo

Define the models in a single repo, then import them into client
applications.

```python
# central repo
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class PhenocamTag(Base):
    __tablename__ = "phenocam_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_updated: Mapped[datetime]
    image: Mapped[str]
    site_id: Mapped[str]
    activity: Mapped[str]
    new_land_cover: Mapped[str]

# consuming application
from sqlalchemy import select

from dri_database_models import PhenocamTag

def foo(site_id):
    with Session(engine) as session:
        query = select(PhenocamTag).where(PhenocamTag.site_id == site_id).order_by(PhenocamTag.last_updated)
        tags = session.execute(query).all()
```

- Good, because models which might be used by e.g. both ingestion and
  processing code can be defined independently of them
- Good, because it's a natural home for Alembic migrations to manage
  the database schema
- Good, because we can use the powerful and widely used SQLAlchemy
  query API
- Bad, because client applications using a version of the models older
  than the database could lead to issues
- Bad, because it's another repo to manage


#### SQLAlchemy declarative models in individual repos

Each subcomponent which interfaces with the database defines its own
declarative models.

- Good, because there is no possibility of the application code and
  database schema getting out of sync
- Good, because we can still use the SQLAlchemy API
- Bad, because it gets complicated when multiple components need to
  access the same database tables
- Bad, because no one repo "owns" the code so there is no natural
  place to put migration information

#### SQLAlchemy core with custom marshalling

Models are defined independently of SQLAlchemy and translated into
each component's classes.

```python
# consuming application
from datetime import datetime

from sqlalchemy import select, Table, Column, String, DateTime, MetaData

metadata_obj = MetaData()

class PhenocamTag:
    last_updated: datetime
    image: str
    site_id: str
    activity: str
    new_land_cover: str

def foo(site_id):
    tag_table = Table(
        "phenocam_tags",
        metadata_obj,
        Column("last_updated", DateTime),
        Column("image", String),
        # etc
    )
    with engine.connect() as conn:
        query = select(tag_table).where(tag_table.site_id == site_id).order_by(tag_table.last_updated)
        tags = [PhenocamTag(...) for ... insession.execute(query).all()]

```

- Good, because there is no dependency on an external repo for each
  component
- Bad, because there's a lot of boilerplate and duplication between
  the application-specific model and the SQLAlchemy metadata required
  for the querying code
- Bad, because there is nowhere to put migrations

#### SQLModel

Use Tiangelo's SQLModel library which wraps SQLAlchemy and integrates
it with Pydantic.

- Good, because it is by the same authors as FastAPI and therefore
  integrates well
- Bad, because we'd still have to make the same central repo vs
  distributing ownership across clients
- Bad, because it's still pre-1.0 and much less mature than SQLAlchemy
