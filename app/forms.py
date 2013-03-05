from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, TextAreaField, Required, Length
class SignUpForm(Form):
	email = TextField('email', validators = [Required()])
	nname = TextField('nickname', validators = [Required()])
	pwd = PasswordField('pwd', validators = [Required()])

class LoginForm(Form):
	email = TextField('openid', validators = [Required()])
	pwd = PasswordField('pwd', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)

class EditProfileForm(Form):
	about_me = TextAreaField('about_me', validators= [Length(min = 0, max = 140)])
		
