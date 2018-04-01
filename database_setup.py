from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import sys


Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))

	@property
	def serialize(self):

		return {
		'id' : self.id,
		'name' : self.name,
		'email' :self.email,
		'picture' : self.picture,
		}

class Categories(Base):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	image = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):

		return {
		'name': self.name,
		'id' : self.id,
		}

class Items(Base):
	__tablename__ = 'items'

	name = Column(String(100), nullable=False)
	id = Column(Integer, primary_key=True)
	description = Column(String(250))
	price = Column(String(8))
	image = Column(String(300))
	seller_name = Column(String(30), nullable=False)
	seller_address = Column(String(200), nullable=False)
	seller_phoneno = Column(Integer, nullable=False)
	categories_id = Column(Integer, ForeignKey('categories.id'))
	categories = relationship(Categories)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)


	@property
	def serialize(self):

		return {
		'name' : self.name,
		'description' : self.description,
		'id' : self.id,
		'price' : self.price,
		'seller_name' : self.seller_name,
		'seller_address' : self.seller_address,
		'seller_phoneno' : self.seller_phoneno,

		}
		
engine = create_engine(
	'sqlite:///shopdata.db')

Base.metadata.create_all(engine)