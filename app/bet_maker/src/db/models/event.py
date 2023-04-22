import enum

from sqlalchemy import BigInteger, Column, Enum, Numeric, CheckConstraint, TIMESTAMP
from sqlalchemy.orm import relationship

from db.base import Base


class EventState(enum.IntEnum):
    unknown = 0
    loose = 1
    win = 2


class EventModel(Base):
    """Таблица с игровыми событиями. """

    __tablename__ = 'event'
    __table_args__ = (
        CheckConstraint('coefficient > 0'),
    )

    id: Column = Column(BigInteger, primary_key=True, autoincrement=True)
    coefficient: Column = Column(Numeric(precision=5, scale=2), comment='Коэффициент на победу', nullable=False)
    deadline: Column = Column(TIMESTAMP, comment='Время окончания приёма ставок (UTC)', nullable=False)
    state: Column = Column(
        Enum(EventState, native_enum=False),
        default=EventState.unknown,
        comment='Состояние события относительно первой команды',
        nullable=False,
    )

    bets = relationship('BetModel', lazy='subquery', back_populates='event', cascade='all, delete-orphan')
