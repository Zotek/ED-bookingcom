from db import Db
from model import *
from sqlalchemy.orm import sessionmaker
import re

def cleanup_tags():

    db = Db()
    engine = db.getEngine()
    Session = sessionmaker(bind=engine)
    session = Session()

    tags = session.query(Tag).all()
    cleaned_up_dict = {}

    for t in tags:

        cleaned_up = _cleanup_tag(t.id)
        opinions = session.query(OpinionTag.opinion).filter_by(tag=t.id).all()
        opinions = map(lambda x: x[0], opinions)

        updated_tag = Tag(id = cleaned_up)

        if cleaned_up not in cleaned_up_dict:
            cleaned_up_dict[cleaned_up] = True
            session.add(updated_tag)

        session.query(OpinionTag).filter_by(tag = t.id).delete()

        for opinion in opinions:
            op = OpinionTag(tag = cleaned_up, opinion = opinion)
            session.add(op)

        session.delete(t)

    session.commit()



#returns cleaned up tag
def _cleanup_tag(tag):
    tag = re.sub(r"[^\w ]+","",tag, flags=re.UNICODE)
    return tag


if __name__ == "__main__":
    cleanup_tags()