from flask.ext.wtf import Form, TextField, BooleanField, Required
class LoginForm(Form):
	oid = TextField('openid, validators = [Required()]')
	remember_me = BooleanField('remember_me', default = False)