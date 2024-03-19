import io
import matplotlib.pyplot as plt
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from .dataframes import *


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


def create_figure_weight_base_exp_per_type():
    df = get_weight_base_exp_per_type().sort_values("weight", ascending=False)
    fig = Figure()
    fig.set_size_inches(10, 5)
    axis = fig.add_subplot(1, 1, 1)
    axis.set_ylabel("Weight (kg)")
    axis.set_xlabel("Pokémon Type")

    df.plot(
        kind="scatter",
        x="weight",
        y="base_experience",
        ax=axis,
        c="color",
    )
    axis.legend(df["type"].unique())

    return fig


def create_figure_height_weight_per_type():
    df = get_height_weight_per_type().sort_values("height", ascending=False)
    fig = Figure()
    fig.set_size_inches(10, 5)
    axis = fig.add_subplot(1, 1, 1)
    axis.set_ylabel("Height (m)")
    axis.set_xlabel("Weight (kg)")
    df.plot(
        kind="scatter",
        x="weight",
        y="height",
        ax=axis,
        c="color",
    )
    axis.legend(df["type"].unique())

    return fig
