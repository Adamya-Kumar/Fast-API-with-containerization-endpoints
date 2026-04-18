from sqlalchemy  import create_engine 
from sqlalchemy.orm import sessionmaker
# Change this line:
from sqlalchemy.orm import declarative_base


MYSQL_USER='root'
MYSQL_PASSWORD='0000'
MYSQL_PORT='3306'
MYSQL_HOST='localhost'
MYSQL_DATABASE='fast_api'


DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
print(DATABASE_URL)


## connection
engine = create_engine(DATABASE_URL)

##session
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
        
Base = declarative_base()