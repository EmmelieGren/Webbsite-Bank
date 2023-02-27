from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, ValidationError
from wtforms.fields import IntegerField, SelectField, DateField, DecimalField, EmailField

def emailContains(form, field):
    if not field.data.endswith('.com'):
        raise ValidationError('Have to end with ex: .se')


def stringContains(form, field):
    if field.data() == IntegerField:
        raise ValidationError('Can not be Numbers')

class NewCustomerForm(FlaskForm):
    givenName = StringField('givenname', validators=[validators.DataRequired(), validators.Length(max= 50)])
    surname = StringField('surname', validators=[validators.DataRequired(), validators.Length(max= 50)])
    streetaddress = StringField('streetaddress', validators=[validators.DataRequired()])
    city = StringField('city', validators=[validators.DataRequired()])
    zipcode = IntegerField('zipcode', validators=[validators.DataRequired()])
    country = SelectField('country',choices=[('SWEDEN', 'Sweden'),('NORWAY', 'Norway'),('USA', 'USA')])
    countryCode = SelectField('countryCode',choices=[('SE', 'SE'),('NO', 'NO'),('US', 'US')])
    birthday = DateField('birthday', validators=[validators.DataRequired()])                 
    nationalId = StringField('telephoneCountryCode', validators=[validators.DataRequired()])
    telephoneCountryCode = SelectField('AccountType',choices=[('46', '46'),('47', '47'),('55', '55')])
    telephone = StringField('telephone', validators=[validators.DataRequired()])
    emailAddress = EmailField('emailadress', validators=[validators.DataRequired(),emailContains])

class NewAccountForm(FlaskForm):
    AccountType = SelectField('AccountType',choices=[('Personal', 'Personal'),('Checking', 'Checking'),('Savings', 'Savings')])

class TransactionForm(FlaskForm): 
    Amount = DecimalField('Amount',validators=[validators.DataRequired(), validators.NumberRange(min=1,max=10000)])

class TransferForm(FlaskForm):
    Amount = DecimalField('Amount', validators=[validators.DataRequired(), validators.NumberRange(min=1,max=10000)])
    Id = IntegerField('Id', validators=[validators.DataRequired()])
