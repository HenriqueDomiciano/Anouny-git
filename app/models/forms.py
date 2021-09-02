from flask_wtf import FlaskForm,RecaptchaField
from wtforms import TextAreaField,StringField
from wtforms.validators import DataRequired
import wtforms.validators as validators
from flask_wtf.file import FileField, FileAllowed
from werkzeug.utils import secure_filename

class Formulario(FlaskForm):
    text = TextAreaField('Your anounymous Tweet',validators=[DataRequired(),validators.length(max=255)])
    image = FileField('Select an Image File',validators=[FileAllowed(['jpg','png','jpeg','bmp','gif','raw'], 'Images only!')])
    cap = RecaptchaField()
    