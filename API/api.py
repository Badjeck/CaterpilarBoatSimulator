from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/projet'
db = SQLAlchemy(app)

# Récrupération du compte par ID
@app.route('/user/<username>', methods=['GET'])
def getUser(username):
    user = Users.query.filter_by(username=username).first()
    response = {
            "id": user.id,
            "username": user.username,
            "posX": user.posx,
            "posY": user.posy
        }
    # data = request.get_json()
    # res = Users.query.filter_by(username=username, email=email)
    return {"message": "success", "data": response}

# Récupération de tous les comptes
@app.route('/users', methods=['GET'])
def getUsers():
    res = [{"id": i.id, "username": i.username, "posX": i.posx, "posY": i.posy} for i in Users.query.all()]
    return {"message": 'success', "data": res}

# Création de compte
@app.route('/user', methods=['POST'])
def postUser():
    try:
        db.session.add(Users(request.form['username'], request.form['posx'], request.form['posy']))
        db.session.commit()
        user = Users.query.filter_by(username=request.form['username']).first()
        response = {
                "id": user.id,
                "username": user.username,
                "posX": user.posx,
                "posY": user.posy
            }
        return {"message": 'success', "data": response}
    except Exception as e:
        if "<class 'sqlalchemy.exc.IntegrityError'>" == str(type(e)):
            return {"message": 'error', 'data': "Le pseudo existe deja"}
    
# Modification de compte par id
@app.route('/user/<username>', methods=['PUT'])
def putUser(username):
    user = Users.query.filter_by(username=username).first()
    user.username = request.form['username']
    user.posx = int(request.form['posx'])
    user.posy = int(request.form['posy'])
    db.session.commit()

    user = Users.query.filter_by(username=username).first()
    response = {
        "id": user.id,
        "username": user.username,
        "pos": user.posx,
        "posY": user.posy
    }
    return {"message": 'success', "data": response}


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    posx = db.Column(db.Integer(), unique=True)
    posy = db.Column(db.Integer(), unique=True)

    def __init__(self, username, posx, posy):
        self.username = username
        self.posx = posx
        self.posy = posy
    
    def __repr__(self):
        return f'{self.username}'

if __name__ == '__main__':
    app.run()