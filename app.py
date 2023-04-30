import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv
from werkzeug.utils import secure_filename
from datetime import datetime
# importz plotly.express as px
# import pandas as pd

app = Flask(__name__)

# Set the path to the database and the folder to store the uploaded images
DB_PATH = 'students.db'
IMAGE_FOLDER = 'static/image_folder'

# Add the IMAGE_FOLDER variable to the app.config dictionary
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

# Create a connection to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the table to store the student data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        reg_num TEXT NOT NULL,
        programme TEXT NOT NULL,
        course TEXT NOT NULL,
        year TEXT NOT NULL,
        image TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    with open('students.csv', 'r') as f:
        reader = csv.DictReader(f)
        students = [row for row in reader]
        
    current_time = datetime.now().strftime('%H:%M:%S')
    current_date = datetime.now().strftime('%Y-%m-%d')

    return render_template('index.html', students=students, now=datetime.now,current_time=current_time, current_date=current_date)

# Add a route for the add student form
@app.route('/addstudent', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        reg_num = request.form['reg_num']
        programme = request.form['programme']
        course = request.form['course']
        year = request.form['year']
        image = request.files['image']

        # Save the image to the IMAGE_FOLDER
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['IMAGE_FOLDER'], filename))

        # Add the student data to the database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, reg_num, programme, course, year, image) VALUES (?, ?, ?, ?, ?, ?)',
                       (name, reg_num, programme, course, year, os.path.join(IMAGE_FOLDER, filename)))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    else:
        return render_template('addstudent.html')

# df = pd.read_csv('students.csv')

# # define a function to create a pie chart using plotly
# def create_pie_chart(df, filter_col, filter_val):
#     # create a filtered dataframe based on the chosen filter
#     filtered_df = df[df[filter_col] == filter_val]
    
#     # group the filtered dataframe by Course, Batch, and Year
#     grouped_df = filtered_df.groupby(['Course', 'Batch', 'Year']).size().reset_index(name='count')
    
#     # create a pie chart using plotly
#     fig = px.pie(grouped_df, values='count', names=['Course', 'Batch', 'Year'], 
#                  title=f"Student Count for {filter_col} {filter_val}")
    
#     # return the plotly chart as a div to be rendered in the HTML template
#     return fig.to_html(full_html=False)

# @app.route('/analytics/', methods=['GET', 'POST'])
# def analytics():
#     if request.method == 'POST':
#         filter_col = request.form['filter_col']
#         filter_val = request.form['filter_val']
#     else:
#         filter_col = 'programme'
#         filter_val = 'B.Tech'

#     pie_chart = create_pie_chart(df, filter_col, filter_val)
    
#     return render_template('analytics.html', pie_chart=pie_chart, filter_col=filter_col, filter_val=filter_val)

if __name__ == '__main__':
    app.run(debug=True)
