from pymongo import MongoClient, collection
from src.init import init
from pathlib import Path
import plotly.express as px
from plotly.graph_objects import Figure
from dash import Dash, html, dcc, callback, Output, Input

app = Dash()
client = MongoClient("mongodb://root:example@db")
col: collection.Collection | None = None

def aggregate_education_data(collection: collection.Collection, filter:dict, post_filter: None | dict = None, min_max: bool = False) -> list[dict]:
    """
    Perform aggregation to group data by town size and calculate
    the percentage of people in each education group.

    Parameters:
    collection (collection.Collection): The MongoDB collection to perform aggregation on.
    filter (str): filtering value for uzemi_txt

    Returns:
    List[Dict]: Aggregated data.
    """
    aggregation = [
        {
            "$match": filter,
        },
        {
            "$group": {
                "_id": {
                    "townSize":"$velikostobce_txt",
                    "education":"$vzdelani_txt"
                },
                "count": {"$sum": 1},
            }
        },
        
        {
            "$group": {
                "_id": "$_id.townSize",
                "educationCounts": {
                    "$push": { 
                        "education": "$_id.education",
                        "count": "$count"
                    }
                },
                "total": {"$sum": "$count"},
            }
        },

        {
            "$unwind": "$educationCounts"
        },

        {
            "$project": {
                "education": "$educationCounts.education",
                "percentage": {
                    "$multiply": [
                        {"$divide": ["$educationCounts.count", "$total"]},
                        100
                    ]
                }
            }
        }
    ]
    if post_filter:
        aggregation.append({"$match": post_filter})
    if min_max:
        aggregation.append({"$group": {
            "_id": None,
            "max": {"$max": "$percentage"},
            "min": {"$min": "$percentage"}
            }})

    return list(collection.aggregate(aggregation))

@callback(Output("pie-vzdelani","figure"),Input("selection-uzemi","value") )
def change_pie(filter_value: str) -> Figure:
    if col is None:
        raise Exception("need to initialize collection first")
    data = aggregate_education_data(col,{"velikostobce_txt" :filter_value})
    return px.pie(data,values="percentage", names="education")


if __name__ == "__main__": 
    if not "db" in client.list_database_names():
        init(Path("data.csv"), client["db"]["collection"])
    db = client["db"]
    col = db["collection"]

    town_size_dist = col.distinct("velikostobce_txt")
    count_dist = col.distinct("uzemi_txt")

    counties_res = []

    for county in count_dist:
        res = aggregate_education_data(col,{"uzemi_txt":county},{"education": "Vysokoškolské"}, min_max=True)[0]
        counties_res.append({"uzemí": county, "op": "min", "podíl vysokoškoláků" : res["min"]})
        counties_res.append({"uzemí": county, "op": "max", "podíl vysokoškoláků" : res["max"]})
    
    county_figure = px.bar(counties_res,x="uzemí",y="podíl vysokoškoláků", color="op", barmode="group",text_auto=".2s") # type: ignore
    county_figure.update_layout(showlegend=False)



    app.layout = html.Div([
        dcc.Dropdown(town_size_dist,value=town_size_dist[0], id="selection-uzemi"),
        dcc.Graph(id="pie-vzdelani"),
        dcc.Graph(figure=county_figure)
    ])
    app.run()
    