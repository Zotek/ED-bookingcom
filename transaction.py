import model

class Transaction:

    def __init__(self,session):
        self.session = session

        self.hotel_name = ""
        self.hotel_description = ""
        self.hotel_stars = -1
        self.hotel_price = -1
        self.hotel_grade = {}
        self.address=("","","")

    def commit(self):
        hotel = model.Hotel
        hotel.name = self.hotel_name
        hotel.description = self.hotel_description
        hotel.stars = self.hotel_stars
        hotel.price = self.hotel_price

        grade = self._createGrade()
        hotel.hotel_grade_id = grade.id

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
        cityObj = self.session.query(model.Cities).filter(model.Cities.name == city)
        if cityObj==None:
            cityObj = model.Cities
            cityObj.name=city
            cityObj.country = countryObj.id
        streetObj = model.Address
        streetObj.street = street
        streetObj.city_id = cityObj.id



