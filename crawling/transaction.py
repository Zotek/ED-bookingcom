import ed.model
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
        hotel = ed.model.Hotel()
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
        grade = ed.model.HotelGrade()
        grade.grade = self.hotel_grade.get('main',0)
        grade.cleanliness = self.hotel_grade.get('clean',0)
        grade.comfort = self.hotel_grade.get('comfort',0)
        grade.location = self.hotel_grade.get('location',0)
        grade.features = self.hotel_grade.get('services',0)
        grade.price_to_quality_ratio = self.hotel_grade.get('value',0)
        grade.staff = self.hotel_grade.get('staff',0)
        grade.wifi = self.hotel_grade.get('wifi',0)
        self.session.add(grade)
        self.session.flush()
        return grade

    def _getOrCreateAddress(self):
        street,city,country = self.address
        countryObj = self._getOrCreateCountry(country)
        cityObj = self.session.query(ed.model.City).filter(ed.model.City.name == city).first()
        if cityObj==None:
            cityObj = ed.model.City()
            cityObj.name=city
            cityObj.country = countryObj.id
            self.session.add(cityObj)
            self.session.flush()
        streetObj = ed.model.Address()
        streetObj.street = street
        streetObj.city_id = cityObj.id
        self.session.add(streetObj)
        self.session.flush()
        return streetObj

    def _getOrCreateCountry(self,country):
        countryObj = self.session.query(ed.model.Country).filter(ed.model.Country.id == country).first()
        if countryObj==None:
            countryObj = ed.model.Country()
            countryObj.id=country
            self.session.add(countryObj)
            self.session.flush()
        return countryObj

    def _createOpinions(self, hotel_id):
        for opinion in self.opinions:
            opinionObj = ed.model.Opinion()
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
            optags = map(lambda tag: ed.model.OpinionTag(tag=tag.id,opinion=opinionObj.id),tags)
            self.session.add_all(optags)
            self.session.flush()


    def _getOrCreateAgeRange(self,arange):
        arObj = self.session.query(ed.model.AgeRange).filter(ed.model.AgeRange.id==arange).first()
        if arObj == None:
            arObj = ed.model.AgeRange()
            arObj.id = arange
            self.session.add(arObj)
            self.session.flush()

    def _getOrCreateTags(self,tag):
        tagObj = self.session.query(ed.model.Tag).filter(ed.model.Tag.id==tag).first()
        if tagObj == None:
            tagObj = ed.model.Tag()
            tagObj.id = tag
            self.session.add(tagObj)
            self.session.flush()
        return tagObj


    def _createFeatures(self,hotel_id):
        for category,fs in self.features.iteritems():
            catObj = self._getOrCreateCategory(category)
            features = map(lambda f: self._getOrCreateFeature(f,catObj.id),fs)
            hotelFeatures = map(lambda f: ed.model.HotelFeature(hotel_id=hotel_id,feature_id=f.id),features)
            self.session.add_all(hotelFeatures)
            self.session.commit()


    def _getOrCreateFeature(self,feature,category_id):
        featureObj = self.session.query(ed.model.Feature).filter(ed.model.Feature.id==feature).first()
        if featureObj == None:
            featureObj = ed.model.Feature()
            featureObj.id = feature
            featureObj.category=category_id
            self.session.add(featureObj)
            self.session.flush()
        return featureObj

    def _getOrCreateCategory(self,category):
        categoryObj = self.session.query(ed.model.FeatureCategory).filter(ed.model.FeatureCategory.id==category).first()
        if categoryObj == None:
            categoryObj = ed.model.FeatureCategory()
            categoryObj.id = category
            self.session.add(categoryObj)
            self.session.flush()
        return categoryObj



