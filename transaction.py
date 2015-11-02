import model
from utils import extract_date

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
        self.hotel_url = hotel_url
        self.hotel_description = description
        self.address = address
        self.opinions = opinions
        self.features = features

    def commit(self):
        hotel = model.Hotel()
        hotel.name = self.hotel_name
        hotel.description = self.hotel_description
        hotel.stars = self.hotel_stars
        hotel.price_level = self.hotel_price
        
        hotel.address_id = self._getOrCreateAddress().id
        grade = self._createGrade()
        

        hotel.hotel_grade_id = grade.id
        
        
        self.session.add(hotel)
        self.session.flush()
        self._createOpinions(hotel.id)
        self._createFeatures(hotel.id)
        self.hotel_url.crawled = True
        self.session.commit()


    def _createGrade(self):
        grade = model.HotelGrade()
        grade.grade = self.hotel_grade['main']
        grade.cleanliness = self.hotel_grade['clean']
        grade.comfort = self.hotel_grade['comfort']
        grade.location = self.hotel_grade['location']
        grade.features = self.hotel_grade['services']
        grade.price_to_quality_ratio = self.hotel_grade['value']
        grade.staff = self.hotel_grade['staff']
        grade.wifi = self.hotel_grade['wifi']
        self.session.add(grade)
        self.session.flush()
        return grade

    def _getOrCreateAddress(self):
        street,city,country = self.address
        countryObj = self._getOrCreateCountry(country)
        cityObj = self.session.query(model.City).filter(model.City.name == city).first()
        if cityObj==None:
            cityObj = model.City()
            cityObj.name=city
            cityObj.country = countryObj.id
            self.session.add(cityObj)
            self.session.flush()
        streetObj = model.Address()
        streetObj.street = street
        streetObj.city_id = cityObj.id
        self.session.add(streetObj)
        self.session.flush()
        return streetObj

    def _getOrCreateCountry(self,country):
        countryObj = self.session.query(model.Country).filter(model.Country.id == country).first()
        if countryObj==None:
            countryObj = model.Country()
            countryObj.id=country
            self.session.add(countryObj)
            self.session.flush()
        return countryObj

    def _createOpinions(self, hotel_id):
        for opinion in self.opinions:
            opinionObj = model.Opinion()
            opinionObj.user = opinion['name']
            opinionObj.country = self._getOrCreateCountry(opinion['country']).id if opinion['country']!=None else None
            opinionObj.age_range = self._getOrCreateAgeRange(opinion['age_range'])
            opinionObj.date = extract_date(opinion['date'])
            opinionObj.hotel_id = hotel_id
            opinionObj.positive = opinion['positive']
            opinionObj.negative = opinion['negative']
            opinionObj.grade = opinion['grade'].replace(",",".")
            opinionObj.title = opinion['title']
            opinionObj.user_opinions = opinion['visits']
            self.session.add(opinionObj)
            self.session.flush()
            tags = map(lambda tag: self._getOrCreateTags(tag), opinion['tags'])
            optags = map(lambda tag: model.OpinionTag(tag=tag.id,opinion=opinionObj.id),tags)
            self.session.add_all(optags)
            self.session.flush()


    def _getOrCreateAgeRange(self,arange):
        arObj = self.session.query(model.AgeRange).filter(model.AgeRange.id==arange).first()
        if arObj == None:
            arObj = model.AgeRange()
            arObj.id = arange
            self.session.add(arObj)
            self.session.flush()

    def _getOrCreateTags(self,tag):
        tagObj = self.session.query(model.Tag).filter(model.Tag.id==tag).first()
        if tagObj == None:
            tagObj = model.Tag()
            tagObj.id = tag
            self.session.add(tagObj)
            self.session.flush()
        return tagObj


    def _createFeatures(self,hotel_id):
        for category,fs in self.features.iteritems():
            catObj = self._getOrCreateCategory(category)
            features = map(lambda f: self._getOrCreateFeature(f,catObj.id),fs)
            hotelFeatures = map(lambda f: model.HotelFeature(hotel_id=hotel_id,feature_id=f.id),features)
            self.session.add_all(hotelFeatures)
            self.session.commit()


    def _getOrCreateFeature(self,feature,category_id):
        featureObj = self.session.query(model.Feature).filter(model.Feature.id==feature).first()
        if featureObj == None:
            featureObj = model.Feature()
            featureObj.id = feature
            featureObj.category=category_id
            self.session.add(featureObj)
            self.session.flush()
        return featureObj

    def _getOrCreateCategory(self,category):
        categoryObj = self.session.query(model.FeatureCategory).filter(model.FeatureCategory.id==category).first()
        if categoryObj == None:
            categoryObj = model.FeatureCategory()
            categoryObj.id = category
            self.session.add(categoryObj)
            self.session.flush()
        return categoryObj



