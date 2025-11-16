# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import os

import pandas as pd
import matplotlib.pyplot as plt

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    # Asegurar carpeta de salida
    os.makedirs("docs", exist_ok=True)

    # Cargar información de envíos
    df = pd.read_csv("files/input/shipping-data.csv")

    # --- Gráfico 1: cantidad de envíos por bodega ---
    plt.figure(figsize=(8, 6))
    (
        df["Warehouse_block"]
        .value_counts()
        .plot.bar(
            title="Shipping per Warehouse",
            xlabel="Warehouse_block",
            ylabel="Record count",
            color="tab:blue",
            fontsize=8,
        )
    )
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("docs/shipping_per_warehouse.png")
    plt.close()

    # --- Gráfico 2: distribución de modos de envío ---
    plt.figure(figsize=(8, 6))
    df["Mode_of_Shipment"].value_counts().plot.pie(
        title="Mode of Shipment",
        wedgeprops={"width": 0.35},
        ylabel="",
        colors=["tab:blue", "tab:orange", "tab:green"],
    )
    plt.savefig("docs/mode_of_shipment.png")
    plt.close()

    # --- Gráfico 3: rating promedio por modo de envío ---
    plt.figure(figsize=(8, 6))

    resumen_rating = (
        df[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    resumen_rating.columns = resumen_rating.columns.droplevel()
    resumen_rating = resumen_rating[["mean", "min", "max"]]

    # Rango completo de rating por modo
    plt.barh(
        y=resumen_rating.index.values,
        width=resumen_rating["max"] - 1,
        left=resumen_rating["min"],
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )

    # Barra interna con el promedio, coloreada según el nivel
    colores = [
        "tab:green" if valor >= 3.0 else "tab:orange"
        for valor in resumen_rating["mean"].values
    ]
    plt.barh(
        y=resumen_rating.index.values,
        width=resumen_rating["mean"] - 1,
        left=resumen_rating["min"],
        height=0.5,
        color=colores,
        alpha=1.0,
    )

    plt.title("Average Customer Rating")
    ax = plt.gca()
    ax.spines["left"].set_color("gray")
    ax.spines["bottom"].set_color("gray")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("docs/average_customer_rating.png")
    plt.close()

    # --- Gráfico 4: histograma del peso enviado ---
    plt.figure(figsize=(8, 6))
    plt.hist(
        df["Weight_in_gms"],
        bins=30,
        color="tab:blue",
        alpha=0.7,
        edgecolor="white",
    )
    plt.title("Shipped Weight Distribution")
    plt.xlabel("Weight in gms")
    plt.ylabel("Record count")
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("docs/weight_distribution.png")
    plt.close()

    # --- HTML del dashboard ---
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Shipping Data Dashboard Example</title>
</head>
<body>
    <h1>Shipping Data Dashboard</h1>

    <h2>Shipping per Warehouse</h2>
    <img src="shipping_per_warehouse.png" alt="Shipping per Warehouse">

    <h2>Mode of Shipment</h2>
    <img src="mode_of_shipment.png" alt="Mode of Shipment">

    <h2>Average Customer Rating</h2>
    <img src="average_customer_rating.png" alt="Average Customer Rating">

    <h2>Weight Distribution</h2>
    <img src="weight_distribution.png" alt="Weight Distribution">
</body>
</html>
"""
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)