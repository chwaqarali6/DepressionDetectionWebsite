from flask import Flask, render_template, json, request, session, redirect, url_for
import os, psycopg2, urllib.parse as urlparse

app = Flask(__name__)
app.secret_key = 'xcexc3x80x92xbbxd2x07x86Axe0Xxaax1e5qxb9xb8x82x941cx15xf5'

url = urlparse.urlparse(os.environ.get('DATABASE_URL'))
db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)
conn = psycopg2.connect(db)
cursor = conn.cursor()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/SignIn")
def SignIn():
    return render_template('SignIn.html')

@app.route('/LogIn', methods=['POST'])
def LogIn():
    P_DoctorEmail = request.form['DoctorEmail']
    P_DoctorPassword = request.form['DoctorPassword']
    if P_DoctorEmail and P_DoctorPassword:
        cursor.callproc('SignIn', (P_DoctorEmail, P_DoctorPassword))
        data = cursor.fetchall()
        if len(data) is not 0:
            session['user'] = data[0][0];
            return redirect(url_for('Admin'))
        else:
            return render_template('404.html', text='Invalid Login Credentials')


@app.route('/Admin')
def Admin():
    # cursor.callproc('PatientData', ())
    # data = cursor.fetchall()
    cursor.execute("Select * From Patient")
    data =cursor.fetchall()
    if session.get('user'):
        return render_template('admin.html', data=data)
    else:
        return render_template('404.html',  text = 'Unauthorized Access')


@app.route('/LogOut')
def LogOut():
    session.pop('user',None)
    return redirect('/')


@app.route("/AddPatient")
def AddPatient():
    if session.get('user'):
        return render_template('AddPatient.html')
    else:
        return render_template('404.html',  text = 'Unauthorized Access')

@app.route('/AddPatientFunction', methods=['POST'])
def AddPatientFunction():
    P_PatientName = request.form['PatientName']
    P_CNIC = request.form['PatientCNIC']
    P_Email = request.form['PatientEmail']
    P_Contact = request.form['PatientNumber']
    P_Address = request.form['PatientAddress']
    P_CheckInDate = request.form['PatientDate']
    P_Comments = request.form['PatientComments']
    if P_PatientName and P_CNIC and P_Email and P_Contact and P_Address and P_CheckInDate and P_Comments:
        cursor.execute("SELECT * FROM AddPatient(%s,%s,%s,%s,%s,%s,%s);",(P_PatientName, P_CNIC, P_Email, P_Contact, P_Address, P_CheckInDate, P_Comments))
        data = cursor.fetchall()
        if data[0][0]=='Added':
            conn.commit()
            return redirect(url_for('Admin'))
        else:
            return render_template('404.html',  text = data[0][0])


@app.route("/CheckPatientDepression")
def CheckPatientDepression():
    if session.get('user'):
        return render_template('CheckPatientDepression.html')
    else:
        return render_template('404.html',  text = 'Unauthorized Access')

@app.route("/CheckPatientDepressionFunction", methods=['GET', 'POST'])
def CheckPatientDepressionFunction():
    if 'file' in request.files:
        file = request.files['file']
        target = os.path.join(APP_ROOT, 'PatientProcessedData/')
        destination = "/".join([target, file.filename])
        file.save(destination)
    P_PatientID = request.form['PatientID']
    P_PatientStatus = open(destination, 'r').read()
    if(P_PatientStatus=='1'):
        cursor.execute("SELECT * FROM DepressionStatus(%s,%s);",(P_PatientID, 'Depressed'))
    else:
        cursor.execute("SELECT * FROM DepressionStatus(%s,%s);",(P_PatientID, 'Not Depressed'))
    conn.commit()
    return redirect(url_for('ViewAllPatients'))


@app.route('/ViewAllPatients')
def ViewAllPatients():
    if session.get('user'):
        cursor.execute("Select * From Patient")
        data = cursor.fetchall()
        return render_template('ViewAllPatients.html', data=data)
    else:
        return render_template('404.html',  text = 'Unauthorized Access')


@app.route("/SearchPatientByName")
def SearchByName():
    if session.get('user'):
        return render_template('SearchByName.html')
    else:
        return render_template('404.html',  text = 'Unauthorized Access')

@app.route('/SearchByNameResults', methods=['POST'])
def SearchByNameResults():
    P_SearchingName = request.form['SearchingName']
    cursor.execute("SELECT * FROM SearchByName(%s);",(P_SearchingName,))
    data = cursor.fetchall()
    return render_template('SearchResults.html', data=data)


@app.route("/SearchByDate")
def SearchByDate():
    if session.get('user'):
        return render_template('SearchByDate.html')
    else:
        return render_template('404.html',  text = 'Unauthorized Access')

@app.route('/SearchByDateResults', methods=['POST'])
def SearchByDateResults():
    P_SearchingDate = request.form['SearchingDate']
    print(P_SearchingDate)
    cursor.execute("SELECT * FROM SearchByDate(%s);",(P_SearchingDate,))
    data = cursor.fetchall()
    return render_template('SearchResults.html', data=data)


@app.route("/DeletePatient")
def DeletePatient():
    if session.get('user'):
        return render_template('DeletePatient.html')
    else:
        return render_template('404.html',  text = 'Unauthorized Access')

@app.route('/DeletePatientFunction', methods=['POST'])
def DeletePatientFunction():
    P_PatientID = request.form['PatientID']
    if P_PatientID:
        cursor.execute("Select * FROM DeletePatient(%s);",(P_PatientID))
        data = cursor.fetchall()
        if data[0][0]=='Deleted':
            conn.commit()
            return redirect(url_for('ViewAllPatients'))
        else:
            return render_template('404.html',  text = data[0][0])


if __name__ == "__main__":
    app.run()
