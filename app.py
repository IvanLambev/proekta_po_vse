from configparser import ConfigParser
from datetime import timedelta
import datetime

import psycopg2
from flask import *
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import URL, DataRequired

import scraper
from login_blueprint import login_bp
from register_blueprint import register_bp

config = ConfigParser()
config.read('config.ini')

db_host = config.get('database', 'host')
db_port = config.get('database', 'port')
db_name = config.get('database', 'database')
db_user = config.get('database', 'user')
db_password = config.get('database', 'password')

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)

cur = conn.cursor()

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'HI_MOM!'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
csrf = CSRFProtect(app)

app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(register_bp, url_prefix='/register')


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        form = ScrapeForm()

        if form.validate_on_submit():
            url = form.url.data

            if not scraper.is_valid_url(url):
                flash('Invalid URL', 'danger')
                print("Invalid URL")
                return redirect(url_for('index'))

            # scrape the url
            scraped_text = scraper.get_text(url)
            session['scraped_urls'] = url

            if scraped_text and 'user' in session:
                user = session['user']
                current_date = datetime.date.today()
                formatted_date = current_date.strftime("%Y-%m-%d")
                print("Adding scraped url to database...")
                try:
                    # get the user id
                    cur.execute("SELECT id FROM users WHERE username = %s", (user,))
                    user_id = cur.fetchone()[0]
                    cur.execute("INSERT INTO scraped_urls (url, user_id, date_searched) VALUES (%s, %s, %s)",
                                (url, user_id, formatted_date))
                    conn.commit()
                    print("Scraped url added to database")
                except Exception as e:
                    flash('Error: ' + str(e), 'danger')
                    print("Error: " + str(e))
                    conn.rollback()
                return render_template('scrape_url.html', form=form, scraped_text=scraped_text)

            return render_template('scrape_url.html', form=form, scraped_text=scraped_text)
    except Exception as e:
        flash('Error: ' + str(e), 'danger')
        print("Error: " + str(e))
        return redirect(url_for('index'))
    return render_template('scrape_url.html', form=form)


# Route to handle the form submission
class ScrapeForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Scrape')


@app.route('/summarize', methods=['GET'])
def summarize_url():
    url_to_scrape = session.get('scraped_urls', None)
    print(url_to_scrape)
    if url_to_scrape == "" or url_to_scrape is None:
        flash('Error: URL not found', 'danger')
        print("Error: URL not found")
        return redirect(url_for('index'))
    print(url_to_scrape)
    scraped_text = scraper.get_text(url_to_scrape)
    try:
        if scraped_text:
            summarized_text = scraper.summarize_text(scraped_text)
        else:
            summarized_text = 'No scraped text found.'

        session['summarized_text'] = summarized_text

        return render_template('summary.html', summarized_text=summarized_text)
    except Exception as e:
        flash('Error: ' + str(e), 'danger')
        print("Error: " + str(e))
        return redirect(url_for('index'))


@app.route('/<username>_dashboard')
def user(username):
    if 'user' in session:
        scraped_urls = get_scraped_urls(username)

        # make a list of the urls but make them cleaner
        cleaned_urls = [url[0].strip('()') for url in scraped_urls]
        time_scraped = [url[1] for url in scraped_urls]

        urls = [f'{url} {date}' for url, date in zip(cleaned_urls, time_scraped)]
        print(urls)

        # make a list of the urls but make them cleaner

        return render_template('dashboard.html', username=username, scraped_urls=urls)
    else:
        flash('You are not logged in', 'danger')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login.login'))


def get_scraped_urls(username):
    query = """
        SELECT url, date_searched
        FROM scraped_urls
        WHERE user_id = (
            SELECT id
            FROM users
            WHERE username = %s
        );
    """
    try:
        cur.execute(query, (username,))
        urls = cur.fetchall()
        print(urls)
    except Exception as e:
        print(e)
        urls = []
        conn.rollback()

    return urls


if __name__ == '__main__':
    app.run(debug=True)
