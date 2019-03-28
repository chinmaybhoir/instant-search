"""
    Author: Chinmay Bhoir
    Created on: 26/3/19 1:17 PM
"""
import csv
import os

from instant_search.seq_matcher import score_aggregator

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Enable Cross-Origin Resource Sharing
CORS(app)

FILE = os.environ.get("FILE", "data/test_data_sample.csv")


with open(FILE) as f:
    reader = csv.reader(f)
    # get first name, middle name, and last name from file
    f_names, m_names, l_names = map(list, zip(*[(row[0], row[1], row[2]) if len(row) > 2
                                                else (row[0], row[1], "") if len(row) == 2
                                                else (row[0], "", "") for row in reader]))
    # Remove column names
    f_names = f_names[1:]
    m_names = m_names[1:]
    l_names = l_names[1:]
    # 'names' contains the list of objects with proper name,
    # separated first name, last name and middle name for convenience
    names = [dict(name=str(f_names[i]+" "+m_names[i]+" "+l_names[i]),
                  f_name=f_names[i].lower(),
                  m_name=m_names[i].lower(),
                  l_name=l_names[i].lower()) for i in range(len(f_names))]


@app.route('/process_search')
def gen_search_json():
    query = request.args.get("q", '')
    # results = [{"name": "This is invalid, just to demo AJAX call is working"}]
    # must be list of dicts: [{"name": "foo"}, {"name": "bar"}]
    results = score_aggregator(query, names)
    # print(results[:10])
    resp = jsonify(results=results[:10])  # top 10 results
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run(port=8080, debug=True)
