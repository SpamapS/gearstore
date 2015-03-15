import sqlalchemy
from sqlalchemy import orm

from gearstore.store import sqlalchemy_models as models


_session = None


class Store(object):
    def __init__(self, details):
        self._engine = sqlalchemy.create_engine(details)
        self._session = orm.sessionmaker(bind=engine)

    def initialize_schema(self):
        models.Base.metadata.create_all(self._session)

    def save(self, job):
        j = models.Job(id=job.get('unique'), funcname=job.get('funcname'),
                       arg=job.get('arg'))
        self._session.add(j)
        # TODO: allow commit in batches
        self._session.commit()


    def consume(self, batchlimit=1000):
        for j in self._session.query(models.Job).limit(batchlimit):
            yield {'unique': j.id, 'funcname': j.funcname, 'arg': j.arg}
            self._session.delete(j)
            # TODO: allow committing deletes in batches
            self._session.commit()
