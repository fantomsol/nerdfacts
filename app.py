import io
from nerdfacts.Database import Database
from flask import Flask, Response, render_template
from flask_crontab import Crontab
import pokebase as pb
from nerdfacts.Pokemon import Pokemon
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)
crontab = Crontab(app)
db = Database()
db.connect()
db.create_table()


def get_type_counts():
    counts = db.get_type_counts()
    return pd.DataFrame(counts, columns=["type", "count"])


def get_avg_height_per_type():
    avg_heights = db.get_avg_height_per_type()
    df = pd.DataFrame(avg_heights, columns=["type", "avg_height"])
    df["avg_height"] = df["avg_height"].astype(float).round(2)
    return df


def get_avg_weight_per_type():
    avg_weights = db.get_avg_weight_per_type()
    df = pd.DataFrame(avg_weights, columns=["type", "avg_weight"])
    df["avg_weight"] = df["avg_weight"].astype(float).round(2)
    return df


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


def create_plot(fig):
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


def create_figure_count_type():
    df = get_type_counts().sort_values("count", ascending=False)
    fig = Figure()
    fig.set_size_inches(10, 5)
    axis = fig.add_subplot(1, 1, 1)
    axis.set_ylabel("Count")
    axis.set_xlabel("Pokémon Type")
    df.plot(kind="bar", x="type", y="count", ax=axis, width=0.8)
    for p in axis.patches:
        axis.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        axis.set_xticklabels(df["type"], rotation=45)

    return fig


def create_figure_avg_height_per_type():
    df = get_avg_height_per_type().sort_values("avg_height", ascending=False)
    fig = Figure()
    fig.set_size_inches(10, 5)
    axis = fig.add_subplot(1, 1, 1)
    axis.set_ylabel("Average Height (m)")
    axis.set_xlabel("Pokémon Type")
    df.plot(kind="bar", x="type", y="avg_height", ax=axis, width=0.8, color="orange")
    for p in axis.patches:
        axis.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        axis.set_xticklabels(df["type"], rotation=45)

    return fig


def create_figure_avg_weight_per_type():
    df = get_avg_weight_per_type().sort_values("avg_weight", ascending=False)
    fig = Figure()
    fig.set_size_inches(10, 5)
    axis = fig.add_subplot(1, 1, 1)
    axis.set_ylabel("Average Weight (kg)")
    axis.set_xlabel("Pokémon Type")
    df.plot(kind="bar", x="type", y="avg_weight", ax=axis, width=0.8, color="green")
    for p in axis.patches:
        axis.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        axis.set_xticklabels(df["type"], rotation=45)

    return fig


def download_all_pokemon_gen(gen, db):
    all_poke = pb.APIResourceList("pokemon", gen)
    for i, name in enumerate(all_poke.names):
        pokemon = Pokemon(pb.pokemon(name))
        db.store_pokemon(pokemon)
        if i % 12 == 0:
            print(f"Pokemon {i} stored. Name is {pokemon.name}.", flush=True)


@crontab.job(minute="1")  # corresponds to '04 * * * *' in cron syntax
@app.route("/")
def index():
    total_pokemon = db.get_total_count()
    if total_pokemon == 0:
        download_all_pokemon_gen(1, db)
        total_pokemon = db.get_total_count()

    print(f"Total pokemon in database: {total_pokemon}", flush=True)
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
    app.run(debug=True, host="0.0.0.0")
