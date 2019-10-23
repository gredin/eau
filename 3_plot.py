import pickle

import dateparser
import plotly.graph_objects as go
from pint import UnitRegistry

with open("pages.pickle", "rb") as f:
    pages = pickle.load(f)

ureg = UnitRegistry()
Q_ = ureg.Quantity
ureg.define("degreeC = 1 degC")
ureg.define("pH = 1")


def get_value(lines, field):
    try:
        v = lines[field][0]

        v = v.replace(",", ".")
        v = v.replace("unité pH", "pH")
        v = v.replace("mg(Cl2)/L", "mg/L")
        v = v.replace("mg(CO3)/L", "mg/L")
    except:
        v = None

    return v


values_dates = {}

count_values = {}
for i, lines in pages:
    values = {}
    values["carbonates"] = get_value(lines, "CARBONATES")
    values["calcium"] = get_value(lines, "CALCIUM")
    values["chlore_libre"] = get_value(lines, "CHLORE LIBRE *")
    values["chlore_total"] = get_value(lines, "CHLORE TOTAL *")
    values["chlorures"] = get_value(lines, "CHLORURES")
    values["hydrogenocarbonates"] = get_value(lines, "HYDROGÉNOCARBONATES")
    values["magnesium"] = get_value(lines, "MAGNÉSIUM")
    values["ph"] = get_value(lines, "PH")
    values["ph_star"] = get_value(lines, "PH *")
    values["potassium"] = get_value(lines, "POTASSIUM")
    values["sodium"] = get_value(lines, "SODIUM")
    values["sulfates"] = get_value(lines, "SULFATES")
    values["temperature"] = get_value(lines, "TEMPÉRATURE DE L'EAU *")

    dt = dateparser.parse(get_value(lines, "Date du prélèvement"))

    for field, value in values.items():
        if values[field] is not None:
            parsed_val = Q_(values[field]).m

            if field not in values_dates:
                values_dates[field] = []
            values_dates[field].append((dt, parsed_val))


def generate_figure(field, title, min_y=None, max_y=None, marker_size=5):
    yaxis = dict()
    if min_y is not None and max_y is not None:
        yaxis = dict(range=[min_y, max_y])

    fig = go.Figure(
        data=[
            go.Scatter(
                x=[dt for dt, _ in values_dates[field]],
                y=[ph for _, ph in values_dates[field]],
                mode='markers',
                marker=dict(
                    size=marker_size,
                )
            )
        ],
        layout=go.Layout(
            title=go.layout.Title(text=title),
            yaxis=yaxis
        )
    )
    # fig.show()

    fig.write_image("plots/%s.png" % field)


generate_figure("carbonates", "Carbonates (mg/l)", min_y=0, max_y=10)
generate_figure("calcium", "Calcium (mg/l)", min_y=0, max_y=100)
generate_figure("chlore_libre", "Chlore libre (mg/l)", min_y=0, max_y=2)
generate_figure("chlore_total", "Chlore total (mg/l)", min_y=0, max_y=5)
generate_figure("chlorures", "Chlorures (mg/l)", min_y=0, max_y=100)
generate_figure("hydrogenocarbonates", "Hydrogénocarbonates (mg/l)", min_y=0, max_y=200)
generate_figure("magnesium", "Magnésium (mg/l)", min_y=0, max_y=10)
generate_figure("ph", "pH", min_y=0, max_y=14)
generate_figure("ph_star", "pH (analyse réalisée sur le terrain)", min_y=0, max_y=14)
generate_figure("potassium", "Potassium (mg/l)", min_y=0, max_y=10)
generate_figure("sodium", "Sodium (mg/l)", min_y=0, max_y=50)
generate_figure("sulfates", "Sulfates (mg/l)", min_y=0, max_y=100)
generate_figure("temperature", "Température (°C)", min_y=0, max_y=40)
