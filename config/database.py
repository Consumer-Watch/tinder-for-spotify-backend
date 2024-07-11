from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.app import app



app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fortunealebiosu710:unGlLBvUt76I@ep-empty-wood-a5yfcpvw-pooler.us-east-2.aws.neon.tech/spotinder?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


##app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fortunealebiosu710:unGlLBvUt76I@ep-empty-wood-a5yfcpvw-pooler.us-east-2.aws.neon.tech/spotinder?sslmode=require'
##app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)