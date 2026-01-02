from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#write you id and password there for crud
DATABASE_URL = "mysql+pymysql://root:password@localhost/ems"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
