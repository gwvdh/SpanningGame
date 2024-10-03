from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__, template_folder="templates")


def get_entries(page):
    dict_keys = ["type", "name", "score", "filename"]
    with open ("user_input/entries.txt", "r") as f:
        entries = f.readlines()
        # csv to dict
        entries = [dict(zip(dict_keys, entry.split(","))) for entry in entries]
        print(f'{entries}')
        # filter by page
        entries = [entry for entry in entries if int(entry["type"]) == page]
        for entry in entries:
            if int(entry["type"]) == 1:
                entry["type"] = "TUM logo"
            elif int(entry["type"]) == 2:
                entry["type"] = "Spanning tree"
        # sort by score
        entries = sorted(entries, key=lambda x: float(x["score"]), reverse=False)
        return entries

 
@app.route("/")
def index():
    return render_template("index.html", message="Hello World", table_1_entries=get_entries(1), table_2_entries=get_entries(2))
 
 
if __name__ == "__main__":
    app.run(debug=True)