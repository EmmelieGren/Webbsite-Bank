from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.fields import IntegerField, SelectField, DateField, DecimalField, EmailField
from datetime import datetime
from datetime import timedelta  
import re

#if not field.data.endswith('.[AZ]|[az]{2,3}'):

def emailContains(form, field):
    if not field.data.endswith('.se'):
        raise ValidationError('Have to end with ex: .se')

# def emailContains(form, field):
#     valid = r'\b[A-Za-z]+@[A-Za-z]+\.[A-Z|a-z]{2,7}\b'
#     if not field.data(re.fullmatch(valid)):
#         raise ValidationError('Invalid Email')


def stringContains(form, field):
    if field.data() == IntegerField:
        raise ValidationError('Can not be Numbers')

class NewCustomerForm(FlaskForm):
    givenName = StringField('givenname', validators=[validators.DataRequired()])
    surname = StringField('surname', validators=[validators.DataRequired()])
    streetaddress = StringField('streetaddress', validators=[validators.DataRequired()])
    city = StringField('city', validators=[validators.DataRequired()])
    zipcode = IntegerField('zipcode', validators=[validators.DataRequired()])
    country = StringField('country', validators=[validators.DataRequired()])
    countryCode = StringField('countrycode', validators=[validators.DataRequired()])
    birthday = DateField('birthday', validators=[validators.DataRequired()])                 
    nationalId = IntegerField('nationalId', validators=[validators.DataRequired()])
    telephoneCountryCode = IntegerField('telephoneCountryCode', validators=[validators.DataRequired()])
    telephone = IntegerField('telephone', validators=[validators.DataRequired()])
    emailAddress = EmailField('emailadress', validators=[validators.DataRequired(),emailContains])

class NewAccountForm(FlaskForm):
    AccountType = SelectField('AccountType',choices=[('Personal', 'Personal'),('Checking', 'Checking'),('Savings', 'Savings')])

class TransactionForm(FlaskForm): 
    Amount = DecimalField('Amount',validators=[validators.DataRequired()])


class Transfer(FlaskForm):
    Date = DateField(label='Date', validators=[validators.DataRequired()], default= datetime.utcnow )
    Amount = DecimalField('Amount',validators=[validators.DataRequired()])
    AccountId = IntegerField('Account', validators=[validators.DataRequired()])
    AccountId = IntegerField('Account', validators=[validators.DataRequired()])