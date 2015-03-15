import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative.declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = sa.Column(Binary(255), primary_key=True)
    funcname = sa.Column(Binary(255))
    arg = sa.Column(LargeBinary)
