from nerdfacts.Database import Database
from flask import Flask, render_template
from flask_crontab import Crontab
from nerdfacts.figures import *
from nerdfacts.DownloadThread import DownloadThread
import time

app = Flask(__name__)
crontab = Crontab(app)
db = Database()
db.connect()
db.create_table()
DownloadThread().start()
time.sleep(4)


@app.route("/plot_count_type.png")
def plot_a_png():
    fig = create_figure_count_type()
    return create_plot(fig)


@app.route("/plot_avg_height_type.png")
def plot_png():
    fig = create_figure_avg_height_per_type()
    return create_plot(fig)


@app.route("/plot_avg_weight_type.png")
def plot_avg_weight_png():
    fig = create_figure_avg_weight_per_type()
    return create_plot(fig)


@app.route("/plot_weight_exp_type.png")
def plot_weight_exp_png():
    fig = create_figure_weight_base_exp_per_type()
    return create_plot(fig)


@app.route("/plot_height_weight_type.png")
def plot_height_weight_png():
    fig = create_figure_height_weight_per_type()
    return create_plot(fig)


@crontab.job(minute="1")  # corresponds to '04 * * * *' in cron syntax
@app.route("/")
def index():
    avg_height = db.get_average_height()
    tallest = db.get_tallest()
    shortest = db.get_shortest()
    avg_weight = db.get_average_weight()
    heaviest = db.get_heaviest()
    lightest = db.get_lightest()
    return render_template(
        "index.html",
        avg=avg_height,
        tallest_name=tallest[0],
        max_height=tallest[1],
        shortest_name=shortest[0],
        min_height=shortest[1],
        avg_weight=avg_weight,
        heaviest_name=heaviest[0],
        max_weight=heaviest[1],
        lightest_name=lightest[0],
        min_weight=lightest[1],
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
