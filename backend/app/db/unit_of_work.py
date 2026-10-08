from types import TracebackType

from sqlalchemy.orm import Session


class UnitOfWork:
    def __init__(self, session: Session):
        self.session = session

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.rollback()
            return
        try:
            self.commit()
        except Exception:
            self.rollback()
            raise

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
