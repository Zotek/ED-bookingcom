# -*- coding: utf-8 -*-
import datetime

odm = [u"stycznia",u"lutego",u"marca",u"kwietnia",u"maja",u"czerwca",u"lipca",u"sierpnia",u"września",u"października",u"listopada",u"grudnia"]
def extract_date(strdate):
    d,m,r = strdate.split()
    m = odm.index(m)+1
    return datetime.date(int(r),m,int(d))

def extract_address(straddress):
    street,postal,country = straddress.split(",")
    _,city = postal.split()
    return street.strip(),city.strip(),country.strip()
