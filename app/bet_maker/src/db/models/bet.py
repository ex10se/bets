import enum
from decimal import Decimal

from sqlalchemy import BigInteger, Column, Enum, Numeric, func, DateTime, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from db.base import Base


class BetState(enum.IntEnum):
    unknown = 0
    lost = 1
    earned = 2


class BetModel(Base):
    """
    Таблица со ставками.

    - принимаем ставки только на выигрыш первой команды
    - система с одной валютой
    """

    __tablename__ = 'bet'

    id: Column = Column(BigInteger, primary_key=True, autoincrement=True)
    state = Column(Enum(BetState, native_enum=False), default=BetState.unknown, comment='Результат ставки')
    client_id = Column(ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    event_id = Column(ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    bet_amount = Column(Numeric(precision=20, scale=2), comment='Поставленная сумма денег', nullable=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    date_updated = Column(DateTime(timezone=True), onupdate=func.now())

    client = relationship('ClientModel', lazy='subquery', back_populates='bets')
    event = relationship('EventModel', lazy='subquery', back_populates='bets')

    @hybrid_property
    def result_amount(self) -> Decimal:
        """Изменение суммы денег в результате завершения события."""
        return self.bet_amount * self.event.coefficient
