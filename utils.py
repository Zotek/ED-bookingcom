# -*- coding: utf-8 -*-
import datetime
import re

odm = [u"stycznia",u"lutego",u"marca",u"kwietnia",u"maja",u"czerwca",u"lipca",u"sierpnia",u"września",u"października",u"listopada",u"grudnia"]
def extract_date(strdate):
    d,m,r = strdate.split()
    m = odm.index(m)+1
    return datetime.date(int(r),m,int(d))

def extract_address(straddress):
    street,city,country = re.search("([\S ]+), \d{2}-\d{3} (\S+), (\S+)",straddress,re.UNICODE).groups()
    return street.strip(),city.strip(),country.strip()
