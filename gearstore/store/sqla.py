import sqlalchemy as sa
from sqlalchemy import orm

from gearstore.store import sqla_models as models

_session = None


class Store(object):
    def __init__(self, details):
        self._engine = sa.create_engine(details)
        self._sessionmaker = orm.sessionmaker(bind=self._engine)

    def initialize_schema(self):
        models.Base.metadata.create_all(self._engine)

    def save(self, job):
        # Storing as binary for more efficient usage in MySQL particularly
        for k in ('unique', 'funcname', 'arg'):
            if job.get(k) is not None and (isinstance(job.get(k), str) or
                                           isinstance(job.get(k), unicode)):
                job[k] = job[k].encode('utf-8')
        j = models.Job(id=job.get('unique'), funcname=job.get('funcname'),
                       arg=job.get('arg'))
        sess = self._sessionmaker()
        sess.add(j)
        # TODO: allow commit in batches
        sess.commit()

    def consume(self, batchlimit=1000):
        sess = self._sessionmaker()
        for j in sess.query(models.Job).limit(batchlimit):
            yield {'unique': j.id, 'funcname': j.funcname, 'arg': j.arg}
            sess.delete(j)
            # TODO: allow committing deletes in batches
            sess.commit()
