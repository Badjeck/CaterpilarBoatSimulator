from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/projet'
db = SQLAlchemy(app)

# Récrupération du compte par ID
@app.route('/user/<username>', methods=['GET'])
def getUser(username):
    user = Users.query.filter_by(username=username).first()
    print("===",user)
    response = {
            "id": user.id,
            "username": user.username
        }
    return {"message": "success", "data": response}

# Récupération de tous les comptes
@app.route('/users', methods=['GET'])
def getUsers():
    res = [{"id": i.id, "username": i.username} for i in Users.query.all()]
    return {"message": 'success', "data": res}

# Création de compte
@app.route('/user', methods=['POST'])
def postUser():
    try:

        db.session.add(Users(request.form['username']))
        db.session.commit()
        return {"message": 'success', "data": f"L'utilisateur {request.form['username']} a été ajouté"}
    except Exception as e:
        if : "<class 'sqlalchemy.exc.IntegrityError'>" == str(type(e)):
            return {"message": 'error', 'data': "Le pseudo existe deja"}
    
# Modification de compte par id
@app.route('/user/<username>', methods=['PUT'])
def putUser(username):
    user = Users.query.filter_by(username=username).first()
    user.username = request.form['username']
    db.session.commit()
    return {"message": 'success', "data": f"L'utilisateur {request.form['username']} a été modifié"}


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username):
        self.username = username
    
    def __repr__(self):
        return f'{self.username}'

if __name__ == '__main__':
    app.run()