###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required, Length # Here, too
from flask_sqlalchemy import SQLAlchemy

## App setup code
app = Flask(__name__)
app.config['SECRET_KEY'] = 'damn sourcetree isnt fricken doing github sht'
app.debug = True
app.use_reloader = True

## All app.config values


## Statements for db setup (and manager setup if using Manager)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:arnoldzhoumi14@localhost/ahzhou364midterm"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


######################################
######## HELPER FXNS (If any) ########
######################################




##################
##### MODELS #####
##################

class Name(db.Model):
    __tablename__ = "names"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name, self.id)



###################
###### FORMS ######
###################

class NameForm(FlaskForm):
    name = StringField("Please enter your name.",validators=[Required()])
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
        print(newname)
        db.session.add(newname)
        db.session.commit()
        print("COMMITTED?")
        return redirect(url_for('all_names'))
    return render_template('base.html',form=form)

@app.route('/names', methods=['GET', 'POST'])
def all_names():
    names = Name.query.all()
    return render_template('name_example.html',names=names)






## Code to run the application...

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
if __name__ == '__main__':
    db.create_all() # Will create any defined models when you run the application
    app.run(use_reloader=True,debug=True) # The usual
