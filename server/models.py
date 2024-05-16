from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


# USER MODEL

class User(db.Model, SerializerMixin):
    
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    address = db.Column(db.String)
    phone_number = db.Column(db.String)
    age = db.Column(db.Integer)
    vip = db.Column(db.Boolean)
    year_joined = db.Column(db.Integer)

    # removed non-exercise validations to make this easier to read

    # NUMBER 1:
    @validates('year_joined')
    def validate_year(self, key, value):
        if value < 1970 or value > 2024:
            raise ValueError('Invalid year, must be between 1970 and 2024')
        return value

    # NUMBER 2:
    @validates('username')
    def validate_username(self, key, value):
        import re # re is regex, ideally would import at the top of file
        naughty_words = re.findall('bish|frack|heck', value)
        # findall uses regex rules to find everything that follows a pattern
        if len( naughty_words ) > 0:
            raise ValueError('You used naughty words! Watch your language!')
        return value
    
    # NUMBER 3
    @validates('phone_number')
    def validate_phone(self, key, value):
        # removed dashes to just get the other characters
        formatted_num = value.replace('-','')
        if not len(formatted_num) == 10:
            raise ValueError('Phone number must be proper length')
        
        # for getting alphabet characters we'll use regex again
        import re
        alpha_chars = re.findall('[a-zA-Z]', formatted_num)
        if len( alpha_chars ) > 0:
            raise ValueError('Invalid characters used in phone number')
        
        return formatted_num
    
    # NUMBER 4
    @validates('address')
    def validate_address(self, key, value):
        # as usual we can use regex for this
        import re
        road_words = re.findall('Street|Avenue|Road', value)
        if len(road_words) == 0:
            raise ValueError('Address must include the word Street, Avenue, or Road')

        # slice to get last 5 characters
        last_five_chars = value[-5:]
        # look for anything that isn't a digit
        non_digits = re.findall('\D', last_five_chars)
        if len( non_digits ) > 0:
            raise ValueError('The last five characters must be a zip code!')
        return value