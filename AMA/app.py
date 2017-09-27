import gspread
from flask import Flask, render_template, request, flash
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
creds1 = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client1 = gspread.authorize(creds1)
sheet = client.open('test').sheet1
sheet1 = client1.open('Collegiate Roster Fall 2017').sheet1

app = Flask(__name__)
app.secret_key = 'dont tell anyone'

@app.route('/', methods=['GET', 'POST'])
def students_page():
    if request.method == 'POST':
        students = sheet1.get_all_values()
        check_in_students = sheet.get_all_values()
        found = False
        if request.form['action'] == 'check-in':
            check_student_id = request.form.get("student-id", '')
            check_student_name = request.form.get("first-name", '')
            check_student_last_name = request.form.get('last-name', '')
            check_student = [check_student_id, check_student_name, check_student_last_name, '1']

            for student in students:
                if check_student_id in student:
                    for i, lst in enumerate(check_in_students):
                        if check_student_id in lst:
                            found = True
                            break
                    if found:
                        sheet.update_cell(i + 1, 4, int(lst[3]) + 1)
                    else:
                        sheet.append_row(check_student)
                        found = True
                    break

            if not found:
                flash('Student doesn\'t exist, please register first')

        elif request.form['action'] == 'register':
            new_student_id = request.form.get('student-id', '')
            new_student_fname = request.form.get('first-name', '')
            new_student_lname = request.form.get('last-name', '')
            new_student_email = request.form.get('email', '')
            new_student = [new_student_id, new_student_fname, new_student_lname, new_student_email]
            for student in students:
                if new_student_id in student:
                    found = True
            if not found:
                sheet1.append_row(new_student)
            if found:
                flash('This student already exist, go ahead and check in!')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
