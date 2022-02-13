import json
import numpy as np

def magical_color():
    color = list(np.random.choice(range(256), size=3))
    return f"rgb({color[0]}, {color[1]}, {color[2]})"

def translate(data):
    datasets = []
    for i in data:
        if i != "origin":
            datasets.append({
                "label": i,
                "data": data[i],
                "fill": False,
                "borderColor": magical_color(),
                "tension": 0.1
            })

    data = {
        "labels": data.get("origin"),
        "datasets": datasets
    }

    return json.dumps({
        "type": "line",
        "data": data
    })