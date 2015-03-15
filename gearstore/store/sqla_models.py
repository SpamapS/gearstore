import sqlalchemy as sa
from sqlalchemy.ext import declarative

Base = declarative.declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = sa.Column(sa.Binary(255), primary_key=True)
    funcname = sa.Column(sa.Binary(255))
    arg = sa.Column(sa.LargeBinary)
