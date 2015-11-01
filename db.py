import model
from sqlalchemy import create_engine


database_type = 'postgresql'
host = 'localhost'
username = 'datamining'
password = 'datamining'
database = 'datamining'
port = 5432

engine = create_engine('{0}://{1}:{2}@{3}:{4}/{5}'.format(database_type,username,password,host,port,database), echo=True)
model.Base.metadata.create_all(engine)



