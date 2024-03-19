from threading import Thread, Lock
from .Database import Database
from .Pokemon import Pokemon
import pokebase as pb

mutex = Lock()
db = Database()
db.connect()
GEN = 1


def download_all_pokemon_gen(gen, db):
    all_poke = pb.APIResourceList("pokemon", gen)
    all_in_db = db.get_all_pokemon_names()
    to_download = [
        (i, name) for (i, name) in enumerate(all_poke.names) if name not in all_in_db
    ]
    for i, name in to_download:
        with mutex:
            pokemon = Pokemon(pb.pokemon(name))
            db.store_pokemon(pokemon)
            if i % 12 == 0:
                print(f"Pokemon {i} stored. Name is {pokemon.name}.", flush=True)


class DownloadThread(Thread):
    def run(self):
        print(
            "Starting download of pokémon, printing every 12'th for progress",
            flush=True,
        )
        total_pokemon = db.get_total_count()
        download_all_pokemon_gen(GEN, db)
        total_pokemon = db.get_total_count()
        print(f"Total pokemon in database: {total_pokemon}", flush=True)
