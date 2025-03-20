from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='Home', content='Welcome to the Home Page')

@app.route('/sum-up')
def sum_up():
    return render_template('index.html', title='Sum Up', content='This is the Sum Up Page')

@app.route('/about-us')
def about_us():
    return render_template('index.html', title='About Us', content='Learn more about us on this page.')

if __name__ == '__main__':
    app.run(debug=True)
