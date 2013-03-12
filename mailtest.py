from flask.ext.mail import Message
from app import mail
from config import ADMINS
print 'start'
msg = Message('test subject', sender=ADMINS[0], recipients=['yangyxcn@gmail.com'])
msg.body = 'text body'
msg.html = '<b>html</b>'
mail.send(msg)

print 'end'
