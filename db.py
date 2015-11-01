import model
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_type = 'postgresql'
host = 'localhost'
username = 'datamining'
password = 'datamining'
database = 'datamining'
port = 5432

engine = create_engine('{0}://{1}:{2}@{3}:{4}/{5}'.format(database_type,username,password,host,port,database), echo=True)

Session = sessionmaker(bind=engine)
session = Session()

model.Base.metadata.create_all(engine)


hotel = model.Hotel()
hotel.name = "sample_hotel"
#hotel.address_id = 5

session.add(hotel)
session.commit()