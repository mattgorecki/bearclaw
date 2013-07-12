from couchdbkit import *
import datetime
import random

s = Server()
db = s.get_or_create_db("bearclaw")

class AccessMethod(Document):
  key_type = StringProperty()
  key_id = StringProperty()
  valid_from = DateTimeProperty()
  valid_to = DateTimeProperty()

class Member(Document):
  name = StringProperty()
  access_methods = ListProperty()
  signup_date = DateTimeProperty()
  expiration_date = DateTimeProperty()

AccessMethod.set_db(db)
Member.set_db(db)

"""
designer.pushapps('_design', db)

access = AccessMethod(
  key_type = 'rfid',
  key_id = str(random.randint(1000000000, 9999999999)),
  valid_from = datetime.datetime.now(),
  valid_to = datetime.datetime.now() + datetime.timedelta(days=1)
)

#access.save()

member = Member(
  name = "Bob",
  signup_date = datetime.datetime.now(),
  valid_to = datetime.datetime.now() + datetime.timedelta(days=1)
)

member.access_methods.append(access._id)

#member.save()

#key = AccessMethod.view('accessmethod/by_id')

#keys = AccessMethod.view('accessmethod/all')
#for k in keys.all():
#  print k.to_json()
"""
