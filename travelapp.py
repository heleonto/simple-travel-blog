from flask import Flask, render_template, redirect

from functions import translate_content, translate_when, translate_countries, translate_cities

app = Flask(__name__)


@app.route('/')
def en_home():
    return redirect('/en')


@app.route('/<lang>')
def entry_point(lang):
    return render_template('home.html', lang=lang, home_text=translate_countries(lang))


@app.route('/<lang>/<country>')
def show_country(lang, country):
    return render_template("countries.html", lang=lang, country=country, cities_info=translate_cities(lang, country))


@app.route('/<lang>/<country>/<city>')
def show_when(lang, country, city):
    return render_template("when_visited.html", lang=lang, when_info=translate_when(lang, country, city), city=city,
                           country=country)


@app.route('/<lang>/<country>/<city>/<time>')
def show_content(lang, country, city, time):
    img_dict, img_count = translate_content(lang, country, city, time)
    return render_template("city_content.html", lang=lang, when=time, city=city,
                           country=country, img_dict=img_dict, img_count=img_count)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
