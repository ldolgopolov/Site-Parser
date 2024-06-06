import datetime
from sqlalchemy import create_engine, Column, Integer, Text, FLOAT, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

Base = declarative_base()

class Items(Base):
    __tablename__ = 'parsed_items'
    id = Column(Integer, autoincrement="auto", primary_key=True)
    title_item = Column(Text, unique=False, nullable=False)
    price_item = Column(Integer, nullable=False)
    code_item = Column(Integer, unique=True, nullable=False)
    status_item = Column(Text, unique=False, nullable=False)
    manufacturer_item = Column(Text, unique=False, nullable=False)
    photo_item = Column(Text, unique=False, nullable=False)


class Database():
    def __init__(self):
        self.db_url = 'sqlite:///database.db'
        self.engine = create_engine(self.db_url)


    def create_database(self):
        Base.metadata.create_all(self.engine)


    def add_new_item(self, item_data):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            new_item = Items(code_item=item_data[0], title_item=item_data[1], price_item=item_data[2], status_item=item_data[3], manufacturer_item=item_data[4], photo_item=item_data[5])
            session.add(new_item)
            session.commit()

        except Exception as e:
            print(f"DB ERROR:\n{str(e)}")
        finally:
            session.close()


    def check_availability_item(self, item_data):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            item = session.query(Items).filter_by(code_item=item_data[0]).first()
            if not item:
                return True

        except Exception as e:
            print(f"DB ERROR:\n{str(e)}")
        finally:
            session.close()


    def check_uniqueness_item_values(self, db_element, new_item_data):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            db_item_data = [db_element[0], db_element[1], db_element[2], db_element[3], db_element[4], db_element[5]]

            if db_item_data != new_item_data:
                for i in range(len(db_item_data)):
                    if db_item_data[i] != new_item_data[i]:
                        db_item_data[i] = new_item_data[i]

                db_element.code_item=db_item_data[0]
                db_element.title_item=db_item_data[1]
                db_element.price_item=db_item_data[2]
                db_element.status_item=db_item_data[3]
                db_element.manufacturer_item=db_item_data[4]
                db_element.photo_item=db_item_data[5]

        except Exception as e:
            print(f"DB ERROR:\n{str(e)}")
        
        finally:
            session.close()