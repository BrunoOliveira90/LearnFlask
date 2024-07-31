from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from forms import ProdutoForm, EditarProdutoForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produtos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=10)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.String(20), nullable=False)
    imagem = db.Column(db.String(200), nullable=False)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/test2")
def test2():
    return render_template("test2.html")


@app.route("/test3")
def test3():
    produtos = Produto.query.all()
    return render_template('test3.html', produtos=produtos)

@app.route("/test4")
def test4():
    return render_template("test4.html")

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = ProdutoForm()
    if form.validate_on_submit():
        novo_produto = Produto(
            nome=form.nome.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            imagem=form.imagem.data
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('test3'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:produto_id>', methods=['GET', 'POST'])
def edit(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    form = EditarProdutoForm()

    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.descricao = form.descricao.data
        produto.preco = form.preco.data
        produto.imagem = form.imagem.data

        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('index'))

    elif request.method == 'GET':
        form.nome.data = produto.nome
        form.descricao.data = produto.descricao
        form.preco.data = produto.preco
        form.imagem.data = produto.imagem

    return render_template('edit.html', form=form, produto=produto)

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent=True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email

        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()

        flash("Login succesful!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!", "info")
            return redirect(url_for("user"))    
        return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        #flash("You're logged in", "info")

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!", "info")
        return redirect(url_for("login"))

@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have been logged out!", "info")
    session.pop("user", None)    
    session.pop("email", None) 
    return redirect(url_for("login"))
 
if __name__ == "__main__":
    #with app.app_context():
    #    db.create_all()
    app.run(debug=True)