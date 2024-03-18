import io
from nerdfacts.Database import Database
from flask import Flask, Response, render_template
import requests
import pokebase as pb
from nerdfacts.Pokemon import Pokemon
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)

    
def get_type_counts():
    db = Database()
    db.connect()
    counts = db.get_type_counts()
    return pd.DataFrame(counts, columns=['type', 'count'])

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    df = get_type_counts()
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    df.plot(kind='bar', x='type', y='count', ax=axis)

    return fig

@app.route('/')
def index():
    db = Database()
    db.connect()
    db.create_table()

    # gen = pb.generation(1)
    '''
    i = 1
    while True:
        try:
            pokemon = Pokemon(pb.pokemon(i))
            db.store_pokemon(pokemon)
            if i % 100 == 0:
                print(f"Pokemon {i} stored. Name is {pokemon.name}.", flush=True)
            i += 1
        except(requests.exceptions.HTTPError, AttributeError):
            print(f"Pokemon {i} does not exist. {i} pokemons were stored.", flush=True)
            break

    '''

    avg_height = db.get_average_height()
    poke_max_height = db.get_max_height()
    plot_png()
    return render_template('index.html', avg=avg_height, tallest_name=poke_max_height[0], max_height=poke_max_height[1])



    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    