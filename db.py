import datetime
from sqlalchemy import create_engine, Column, Integer, Text, FLOAT, BOOLEAN, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload

from config import Config

Base = declarative_base()

class Items(Base):
    __tablename__ = 'parsed_items'
    id = Column(Integer, autoincrement="auto", primary_key=True)
    code_item = Column(Integer, unique=True, nullable=False)
    price_item = Column(FLOAT, nullable=False)
    status_item = Column(Text, unique=False, nullable=False)
    manufacturer_item = Column(Text, unique=False, nullable=False)
    category_item = Column(Text, unique=False, nullable=False)
    image_item = Column(Text, unique=False, nullable=False)


class Titles(Base):
    __tablename__ = 'item_titles'
    id = Column(Integer, autoincrement="auto", primary_key=True)
    code_item = Column(Integer, unique=True, nullable=False)
    eng_title = Column(Text, unique=False, nullable=True)
    lv_title = Column(Text, unique=False, nullable=True)
    ru_title = Column(Text, unique=False, nullable=True)


class Database():
    def __init__(self):
        self.db_url = 'sqlite:///database.db'
        self.engine = create_engine(self.db_url)


    def create_database(self):
        Base.metadata.create_all(self.engine)


    def add_new_item(self, item_data, item_lang):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            new_item = Items(code_item=item_data[0], price_item=item_data[2], status_item=item_data[3], manufacturer_item=item_data[4], category_item=item_data[5], image_item=item_data[6])
            if item_lang == 'English':
                new_titles = Titles(code_item=item_data[0], eng_title=item_data[1])
            elif item_lang == 'Latviešu':
                new_titles = Titles(code_item=item_data[0], lv_title=item_data[1])
            elif item_lang == 'Русский':
                new_titles = Titles(code_item=item_data[0], ru_title=item_data[1])
            session.add(new_item)
            session.add(new_titles)
            
            session.commit()

        except Exception as e:
            print(f"DB ERROR:\n{str(e)}")
        finally:
            session.close()


    def check_availability_item(self, item_code):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()

            item = session.query(Items).filter(Items.code_item == item_code).first()

            if not item:
                return False
            session.commit()

        except Exception as e:
            print(f"DB ERROR:\n{str(e)}")
        finally:
            session.close()


    def check_uniqueness_item_values(self, item_code, new_item_data, item_lang):
        try:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            
            item = session.query(Items).filter(Items.code_item == item_code).first()
            title = session.query(Titles).filter(Titles.code_item == item_code).first()
            if item_lang == 'English':
                db_item_data = [title.eng_title, item.price_item, item.status_item]
            elif item_lang == 'Latviešu':
                db_item_data = [title.lv_title, item.price_item, item.status_item]
            elif item_lang == 'Русский':
                db_item_data = [title.ru_title, item.price_item, item.status_item]

            if new_item_data != db_item_data:
                new_item_data.pop(0)
                new_item_data.pop(3)
                new_item_data.pop(3)

                for i in range(len(db_item_data)):
                    if db_item_data[i] != new_item_data[i]:
                        db_item_data.pop(i)
                        db_item_data.insert(i, new_item_data[i])
                self.update_item_values(db_item_data, item_lang, item, title)
                print('Edited!')
            
            session.commit()

        except Exception as e:
            print(f"DB ERROR:\n{str(e)}")
        
        finally:
            session.close()


    def update_item_values(self, db_item_data, item_lang, item, title):
        if item_lang == 'English':
                title.eng_title = db_item_data[0]
                item.price_item = db_item_data[1]
                item.status_item = db_item_data[2]
        elif item_lang == 'Latviešu':
            title.lv_title = db_item_data[0]
            item.price_item = db_item_data[1]
            item.status_item = db_item_data[2]
        elif item_lang == 'Русский':
            title.ru_title = db_item_data[0]
            item.price_item = db_item_data[1]
            item.status_item = db_item_data[2]