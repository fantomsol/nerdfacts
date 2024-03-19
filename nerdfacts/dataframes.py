from nerdfacts.Database import Database
import pandas as pd
import numpy as np

db = Database()
db.connect()

type_color_map = {
    "normal": "#A8A77A",
    "fire": "#EE8130",
    "water": "#6390F0",
    "electric": "#F7D02C",
    "grass": "#7AC74C",
    "ice": "#96D9D6",
    "fighting": "#C22E28",
    "poison": "#A33EA1",
    "ground": "#E2BF65",
    "flying": "#A98FF3",
    "psychic": "#F95587",
    "bug": "#A6B91A",
    "rock": "#B6A136",
    "ghost": "#735797",
    "dragon": "#6F35FC",
    "dark": "#705746",
    "steel": "#B7B7CE",
    "fairy": "#D685AD",
}


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


def get_weight_base_exp_per_type():
    height_base_exp = db.get_weight_base_experience_per_type()
    df = pd.DataFrame(height_base_exp, columns=["type", "weight", "base_experience"])
    df["color"] = df["type"].apply(lambda x: type_color_map[x])
    return df


def get_height_weight_per_type():
    height_weight = db.get_height_weight_per_type()
    df = pd.DataFrame(height_weight, columns=["type", "height", "weight"])
    df["color"] = df["type"].apply(lambda x: type_color_map[x])
    return df
