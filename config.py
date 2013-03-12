#-*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'Just-for-test'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'train.ticket.archie'
MAIL_PASSWORD = 'ticketticket'

ADMINS = ['train.ticket.archie@gmail.com']

# pagination
POSTS_PER_PAGE = 3

WHOOSE_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50

#available language
LANGUAGES = {
	'en':'English',
	'zh':'中文'
}

