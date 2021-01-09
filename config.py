# File to store the config of the project
# Ideally, this is what we would do:

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or '06d80eb0c50b49a509b49f2424e8c805'
#     SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
#     MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
#     FROM_EMAIL = os.environ.get('FROM_EMAIL')
#     TO_EMAIL = os.environ.get('TO_EMAIL')
#     FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     @staticmethod
#     def init_app(app):
#         pass