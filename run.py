from flask import Flask, Response, render_template
from pymongo import MongoClient
from bson import json_util

mongo = MongoClient()

db = mongo.kosovoprocurements

collection = db.procurements


app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World"

@app.route('/harta')
def harta():
    rezultati = collection.aggregate([
            {
              "$match": {
                    "komuna.slug": "gjilan",
                    "viti": 2013,
                    "kompania.selia.slug": {'$ne': ''}
                }
            },
            {
                "$group": {
                    "_id": {
                        "selia": "$kompania.selia.slug",
                        "emri": "$kompania.selia.emri",
                        "gjeresi": "$kompania.selia.kordinatat.gjeresi",
                        "gjatesi": "$kompania.selia.kordinatat.gjatesi",
                    },
                    "cmimi": {
                        "$sum": "$kontrata.qmimi"
                    },
                    "vlera": {
                        "$sum": "$kontrata.vlera"
                    },
                    "numriKontratave": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "_id.selia": 1
                }
            },
            {
                "$project": {
                    "selia": "$_id.selia",
                    "emri": "$_id.emri",
                    "gjeresia": "$_id.gjeresi",
                    "gjatesia": "$_id.gjatesi",
                    "cmimi": "$cmimi",
                    "vlera": "$vlera",
                    "numriKontratave": "$numriKontratave",
                    "_id": 0
                }
            }
        ])
    resp = Response(response=json_util.dumps(rezultati['result']),
        mimetype="application/json")

    return resp


@app.route('/pie')
def pie():
    rezultati = collection.aggregate([
            {"$match": {
                "komuna.slug": "gjilan",
                "viti": 2013
            }
            },
            {"$group": {
                "_id": {
                    "tipi": "$tipi"
                },
                "shumaProkurimit": {
                    "$sum": "$kontrata.vlera"
                }
            }

            },
            {"$sort": {
                "_id.tipi": 1
            }},
            {"$project": {
                "_id": 0,
                "tipi": "$_id.tipi",
                "shuma": "$shumaProkurimit"
            }}
        ])

    return Response(response=json_util.dumps(rezultati['result']), mimetype='application/json')


@app.route("/gilani/<string:emri>")
def gilani(emri):
    rezultati = "Si jeni zoteri , " + emri
    return rezultati

if __name__ == "__main__":
    app.run(debug=True, host= "0.0.0.0",port=5050)
