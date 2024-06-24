from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ProdutoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    descricao = StringField('Descrição', validators=[DataRequired()])
    preco = StringField('Preço', validators=[DataRequired()])
    imagem = StringField('URL da Imagem', validators=[DataRequired()])
    submit = SubmitField('Adicionar Produto')