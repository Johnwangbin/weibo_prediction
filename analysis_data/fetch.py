from connect_db import *

def fetch_blog_by_id(id):
    with open_session() as s:
        result = s.query(WeiboProfile).filter(WeiboProfile.id==id).first()
    return result

