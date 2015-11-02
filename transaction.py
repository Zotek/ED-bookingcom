import model

class Transaction:

    # hotel_url - object as in model.HotelUrl
    # address - tuple (street,city,country)
    # hotel_grade - dictionary 
    # description - string
    # opinions - opinions scrapped in opinion_scrap.py

    def __init__(self,session, hotel_url, address, hotel_grade, description, opinions, features):
        self.session = session

        self.hotel_name = hotel_url.hotel_name
        self.hotel_stars = hotel_url.hotel_stars
        self.hotel_price = hotel_url.hotel_price
        self.hotel_grade = hotel_grade
        self.hotel_description = description
        self.address = address
        self.opinions = opinions
        self.features = features

    def commit(self):
        hotel = model.Hotel()
        hotel.name = self.hotel_name
        hotel.description = self.hotel_description
        hotel.stars = self.hotel_stars
        hotel.price = self.hotel_price
        
        hotel.address = self._getOrCreateAddress()
        grade = self._createGrade()
        

        hotel.hotel_grade_id = grade.id
        
        
        session.add(hotel)
        session.commit()


    def _createGrade(self):
        grade = model.HotelGrade
        grade.grade = self.hotel_grade['main']
        grade.cleanliness = self.hotel_grade['clean']
        grade.comfort = self.hotel_grade['comfort']
        grade.location = self.hotel_grade['location']
        grade.features = self.hotel_grade['features']
        grade.price_to_quality_ratio = self.hotel_grade['value']
        grade.wifi = self.hotel_grade['wifi']
        return grade

    def _getOrCreateAddress(self):
        street,city,country = self.address
        countryObj = self.session.query(model.Country).filter(model.Country.id == country).first()
        if countryObj==None:
            countryObj = model.Country
            countryObj.id=country
            self.session.add(countryObj)
        cityObj = self.session.query(model.Cities).filter(model.Cities.name == city)
        if cityObj==None:
            cityObj = model.City
            cityObj.name=city
            cityObj.country = countryObj.id
            self.session.add(cityObj)
        streetObj = model.Address
        streetObj.street = street
        streetObj.city_id = cityObj.id
        return streetObj

    def _createOpinions(self):
        pass


    def _getOrCreateTags(self):
        pass


    def _getOrCreateFeatures(self):
        pass



