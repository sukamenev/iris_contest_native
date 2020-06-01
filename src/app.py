from flask import Flask, render_template, flash, request
from wtforms import Form, IntegerField, RadioField, validators, StringField, SubmitField

import testing

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    count = IntegerField(u'Count of goods for testing: ', validators=[validators.required()])
    test_select = RadioField(u'Type of test', validators=[validators.required()], choices=[('adding', 'Adding goods in DBs'), ('reading', 'Reading goods from DBs')])

    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)

        print(form.errors)
        if request.method == 'POST' and form.validate():
          count = int(request.form['count'])

          sTest=request.form['test_select']
          sTest=form.test_select.data

          if sTest=='adding':

            fIris = testing.runIrisAddTest(count)
            fEAX  = testing.runEAXAddTest(count)

            flash("IRIS native globals: adding of {0} goods - {1:.4f} sec.".format(count, fIris))
            flash("EAV (MySql backend): adding of {0} goods - {1:.4f} sec.".format(count, fEAX))
            flash('ADDING: IRIS Native API x{:.2f} faster!'.format(fEAX/fIris))
          else:
            fIris = testing.runIrisReadTest(count)
            fEAX  = testing.runEAXReadTest(count)

            flash("IRIS native globals: reading of {0} goods - {1:.4f} sec.".format(count, fIris))
            flash("EAV (MySql backend): reading of {0} goods - {1:.4f} sec.".format(count, fEAX))

            flash('READING: IRIS Native API x{:.2f} faster!'.format(fEAX/fIris))
        else:
          flash('Error: All the form fields are required. ')

        return render_template('hello.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
