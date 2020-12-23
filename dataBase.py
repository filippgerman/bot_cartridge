from sqlalchemy import create_engine, Table, MetaData, Column, BIGINT, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pymysql

pymysql.install_as_MySQLdb()
engine = create_engine("mysql://root:fil@localhost/cartridg", encoding="utf8")

Base = declarative_base()
Session = sessionmaker(bind=engine)


class Cart(Base):
    __tablename__ = 'Cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    printer = Column(String(500, collation='utf8mb4_unicode_ci'), index=True)
    cartridge = Column(String(500, collation='utf8mb4_unicode_ci'))

    def __init__(self, printer, cartridge):
        self.printer = printer
        self.cartridge = cartridge


Base.metadata.create_all(engine)
session = Session()



# res = 'HL 4140'
# result = session.query(Cart).filter(Cart.printer.like(f'%{res}%')).count()
# result_too = session.query(Cart).filter(Cart.printer.like(f'%{res}%'))
# # res = 'HL 4140'
# # data = session.query(Cart).filter(Cart.printer.like(f'%{res}%'))
# # # data = session.query(Cart).filter(Cart.id == 2)
# #
# print(result)
# for i in result_too:
#     print(i.printer)
#     print(i.cartridge)
