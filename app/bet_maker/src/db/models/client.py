import uuid

from sqlalchemy import BigInteger, Column, String, Uuid, Numeric
from sqlalchemy.orm import relationship

from db.base import Base


class ClientModel(Base):
    """Таблица с клиентами. """

    __tablename__ = 'client'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String, comment='Имя', nullable=False)
    amount = Column(Numeric(precision=20, scale=2), comment='Сумма денег на счету', default=0)
    auth_key = Column(Uuid, comment='Ключ авторизации', default=uuid.uuid4)

    bets = relationship('BetModel', lazy='subquery', back_populates='client', cascade='all, delete-orphan')
