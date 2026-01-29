from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(String, unique=True, nullable=False)
	monthly_budget = Column(Float, default=0.0)

	# Relationship: One user can have many expenses
	expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")

	def __repr__(self):
		return f"<User(username='{self.username}', budget={self.monthly_budget})>"


class Expense(Base):
	__tablename__ = 'expenses'

	id = Column(Integer, primary_key=True)
	amount = Column(Float, nullable=False)
	category = Column(String, nullable=False)  # e.g., 'Groceries', 'Dining Out'
	description = Column(String)
	date = Column(DateTime, default=datetime.utcnow)

	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship("User", back_populates="expenses")

	def __repr__(self):
		return f"<Expense(amount={self.amount}, category='{self.category}')>"