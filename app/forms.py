from flask.ext.wtf import Form, TextField, BooleanField, PasswordField, TextAreaField, Required, Length
from models import User


class SignUpForm(Form):
    email = TextField('email', validators=[Required()])
    nname = TextField('nickname', validators=[Required()])
    pwd = PasswordField('pwd', validators=[Required()])


class LoginForm(Form):
    email = TextField('openid', validators=[Required()])
    pwd = PasswordField('pwd', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class EditProfileForm(Form):
    about_me = TextAreaField('about', validators=[Length(min=0, max=140)])
    nickname = TextField('nickname')

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user is not None:
            self.nickname.errors.append("This name is already taken. Please choose another one:)")
            return False
        return True


class PostForm(Form):
    post = TextField('post', validators=[Required()])


class SearchForm(Form):
    search = TextField('search', validators=[Required()])
