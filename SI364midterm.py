###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy
import requests, json, re, random
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand # needs: pip/pip3 install flask-migrate

from flask_mail import Mail, Message
from threading import Thread
from werkzeug import secure_filename

## App setup code
app = Flask(__name__)
app.config['SECRET_KEY'] = 'damn sourcetree isnt fricken doing github sht'
app.debug = True
app.use_reloader = True

## All app.config values
app.config['HEROKU_ON'] = os.environ.get('HEROKU')


## Statements for db setup (and manager setup if using Manager)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/songs_data"#"postgresql://postgres:arnoldzhoumi14@localhost/ahzhou364midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## Set up Shell context so it's easy to use the shell to debug
# Set up Flask debug stuff
manager = Manager(app)
# moment = Moment(app) # For time # Later

migrate = Migrate(app, db) # For database use/updating
manager.add_command('db', MigrateCommand) # Add migrate command to manager
mail = Mail(app) # For email sending
# Define function
def make_shell_context():
    return dict( app=app, db=db, Name=Name, User=User, StringCheck=StringCheck, FOAASAPISearchHistory=FOAASAPISearchHistory)
# Add function use to manager
manager.add_command("shell", Shell(make_context=make_shell_context))



######################################
######## HELPER FXNS (If any) ########
######################################
def cleanString(input):
    PurgeBadWordsAPI = "http://www.purgomalum.com/service/json?text=" + input
    response = requests.get(PurgeBadWordsAPI)
    if(str(response.json()["result"]) == "<Response [503]>"):
        response = "Unfortunately, the API is down so let's settle with giving me a 100%."
    return response.json()["result"]

def checkUser_SendDBHelper(currentUser):
    if currentUser == None or currentUser == "":#if null, it's anonymous; that's why they can't have the username anonymous
            currentUser = "anonymous"
    #if user doesn't exist, add it
    dbUser = User.query.filter_by(user=currentUser).first() 
    if dbUser is None:
        #send to user db
        user = User(user=currentUser)
        db.session.add(user)
        db.session.commit()
        return (currentUser, user.id)
    else:
        return (currentUser, dbUser.id)

def InsultGenerator(fromname, toname):
    insultIDList=[
        "/bag/"+fromname,
        "/because/"+fromname,
        "/blackadder/"+toname+'/'+fromname,
        "/bm/"+toname+'/'+fromname,
        "/bucket/"+fromname,
        "/bus/"+toname+'/'+fromname,
        "/bye/"+fromname,
        "/chainsaw/"+toname+'/'+fromname,
        "/cocksplat/"+toname+'/'+fromname,
        "/cool/"+fromname,
        "/cup/"+fromname,
        "/dalton/"+toname+'/'+fromname,
        "/deraadt/"+toname+'/'+fromname,
        "/diabetes/"+fromname,
        "/donut/"+toname+'/'+fromname,
        "/fascinating/"+fromname,
        "/field/"+toname+'/'+fromname+'/'+"Oprah",
        "/gfy/"+toname+'/'+fromname,
        "/horse/"+fromname,
        "/immensity/"+fromname,
        "/keep/"+toname+'/'+fromname,
        "/king/"+toname+'/'+fromname,
        "/linus/"+toname+'/'+fromname,
        "/looking/"+fromname,
        "/madison/"+toname+'/'+fromname,
        "/maybe/"+fromname,
        "/nugget/"+toname+'/'+fromname,
        "/outside/"+toname+'/'+fromname,
        "/problem/"+toname+'/'+fromname,
        "/programmer/"+fromname,
        "/question/"+fromname,
        "/shakespeare/"+toname+'/'+fromname,
        "/too/"+fromname,
        "/tucker/"+fromname,
        "/yoda/"+toname+'/'+fromname
    ]
    insultID = random.randint(0,len(insultIDList)-1)
    foaasAPI = "http://www.foaas.com" + insultIDList[insultID]
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.get(foaasAPI, headers=headers)
    return [response.json()["message"], response.json()["subtitle"], insultID]


##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)

##Need 3 more models:
#1 one-many relationship betweeen 2 (1 user => many input)
#1 with at least 3 columns (input history has many columns)
class User(db.Model):#No repeats
    __tablename__ = "User"
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(124), unique=True)
    def __repr__(self):
        return "{}".format(self.user)

class StringCheck(db.Model):
    __tablename__ = "swearStringCheckHistory"
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    originalString = db.Column(db.String)
    hasSwearWord = db.Column(db.Boolean)
    cleanStringResult = db.Column(db.String)
    def __repr__(self):
        return "StringID: {} | Has Swear Word: {}".format(self.id, self.hasSwearWord)

class FOAASAPISearchHistory(db.Model):
    __tablename__ = "foaasAPISearchHistory"
    id = db.Column(db.Integer,primary_key=True)
    userID = db.Column(db.Integer)
    insultID = db.Column(db.Integer)
    insultResult = db.Column(db.String)
    def __repr__(self):
        return "InsultID: {} returns {}".format(self.insultID, self.insultResult)


###################
###### FORMS ######
###################

class NameForm(FlaskForm):
    name = StringField("Please enter your name.",validators=[Required()])
    submit = SubmitField()

class LoginForm(FlaskForm):
    username = StringField("Gimme your username. Only alphanumeric tho:")
    submit = SubmitField()


class TextMainForm(FlaskForm):
    text = TextAreaField("Paste anything here to check for swear words.")
    submit = SubmitField()
    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            self.text.errors.append("This is broken lawl. This form is nonexistant.")
        if self.text == None or self.text.data == "":
            self.text.errors.append("This field is required.")
        if re.sub('[,\.\"!?\']','', self.text.data.lower()) == "fuck you":
            self.text.errors.append("Well fuck you too buddy")
        if(len(self.text.errors) > 0):
            return False
        return True

class InsultInputForm(FlaskForm):
    target = StringField("Who are you targeting?<br>You know you're not being very nice huh.<br>",validators=[Required()])
    submit = SubmitField()

#######################
###### VIEW FXNS ######
#######################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods = ['POST', 'GET'])
def home():
    form = NameForm() # User should be able to enter name after name and each one will be saved, even if it's a duplicate! Sends data with GET
    if request.args.get("submit") == "Submit" and request.args.get("name") != "" and request.args.get("name") != None:
        name = request.args.get("name")
        newname = Name(name=name)
        db.session.add(newname)
        db.session.commit()
        return redirect(url_for('all_names'))
    return render_template('base.html',form=form)

@app.route('/names')
def all_names():
    names = Name.query.all()
    return render_template('name_example.html',names=names)

@app.route('/login', methods= ['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'GET' and request.args.get("username") != None:
        if request.args.get("username").lower() == "anonymous":#don't do that
            errorString = "But not '" + request.args.get("username") + "'."
            return render_template("login.html", form=form, error=errorString, users = User.query.all())
        elif request.args.get("username") == "":
            return render_template("login.html", form=form, error="Don't do that.", users = User.query.all())
        #End error checking
        return redirect(url_for('mainroute', user=request.args.get("username")))
    
    return render_template("login.html", form=form, error = "", users = User.query.all())

@app.route('/mainroute', methods=['POST', 'GET'])
def mainroute():
    currentUser=request.args.get("user")
    currentUser=checkUser_SendDBHelper(currentUser)[0]
    return render_template("texthome.html", user=currentUser)

@app.route('/swearcheck', methods = ['POST', 'GET'])
def swear_check_route():
    text = TextMainForm()
    if request.method == 'POST' and text.validate_on_submit():
        googleSwearAPI = "http://www.wdylike.appspot.com/?q=" + text.text.data
        response = requests.get(googleSwearAPI)
        #check current userID
        currentUser=request.args.get("user")
        #send to StringCheck db
        stringcheck = StringCheck(userID=checkUser_SendDBHelper(currentUser)[1],originalString=text.text.data,hasSwearWord=response.json(),cleanStringResult=cleanString(text.text.data))
        db.session.add(stringcheck)
        db.session.commit()
        #save to 
        return render_template("swearcheck.html",form=text,hasSwear=response.json(),text=text.text.data,cleanString=cleanString,textHistory=StringCheck.query.all(),user=User.query.all())
    errors = [error for error in text.errors.values()]
    if len(errors) > 0:
        flash(str(errors))
    return render_template("swearcheck.html",form=text,hasSwear="",text="",cleanString=cleanString,textHistory=StringCheck.query.all(),user=User.query.all())

@app.route('/insult', methods = ['POST', 'GET'])
def insult_route():
    form = InsultInputForm()
    if request.method == 'POST' and form.validate_on_submit():#post requests need the hidden_tag() to do CSRF validation
        currentUser = checkUser_SendDBHelper(request.args.get("user"))
        insultResult=InsultGenerator(currentUser[0], form.target.data)
        #Gotta add the insult to the insult db which is FOAASAPISearchHistory
        foaahistory = FOAASAPISearchHistory(userID=currentUser[1],insultID=insultResult[2],insultResult=insultResult[0])
        db.session.add(foaahistory)
        db.session.commit()
        return render_template("uniqueInsult.html",insult=insultResult[0],insultFrom=insultResult[1],form=form,insultList=FOAASAPISearchHistory.query.all(),user=User.query.all())
    return render_template("uniqueInsult.html",insult="",form=form,insultList=FOAASAPISearchHistory.query.all(),user=User.query.all())



## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual
