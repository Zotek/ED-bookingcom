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


hotel_opinion_url = model.HotelOpinionUrl(hotel_name="Mariott", hotel_opinion_url="http://mariott.pl/opinie")
hotel_opinion_url1 = model.HotelOpinionUrl(hotel_name="Sheraton", hotel_opinion_url="http://sheraton.pl/opinie")

#hotel = model.Hotel()
#hotel.name = "sample_hotel"
#hotel.address_id = 5

session.add_all([hotel_opinion_url, hotel_opinion_url1])
session.commit()