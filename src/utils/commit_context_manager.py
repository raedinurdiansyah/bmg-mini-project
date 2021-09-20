from contextlib import contextmanager

from src import db


@contextmanager
def commit_session():
    """
    commit_session is a context manager that will commit database session that
     is executed inside the statement clause.

    Example usage:
        with commit_session():
            obj = Model(`**params`)
            db.session.add(obj)
    """

    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
