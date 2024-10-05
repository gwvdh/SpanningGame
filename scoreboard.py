from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")


def get_entries(types: dict[int, str]):
    dict_keys = ["type", "name", "score", "filename"]
    scoreboards = {}
    with open ("user_input/entries.txt", "r") as f:
        entries = f.readlines()
        # csv to dict
        entries = [dict(zip(dict_keys, entry.split(","))) for entry in entries]
        for entry in entries:
            if int(entry["type"]) not in scoreboards:
                if int(entry["type"]) not in types:
                    continue
                scoreboards[int(entry["type"])] = {"title": types[int(entry["type"])], "entries": []}
            scoreboards[int(entry["type"])]["entries"].append(entry)
        # sort by score
        for _, scoreboard in scoreboards.items():
            scoreboard["entries"] = sorted(scoreboard["entries"], key=lambda x: float(x["score"]), reverse=False)
        scoreboards = [value for _, value in scoreboards.items()]
        return scoreboards

 
@app.route("/")
def index():
    return render_template("scoreboard.html", message="Hello World", scoreboards=get_entries({1: "TUM logo", 2: "Spanning tree"}))
 
 
if __name__ == "__main__":
    app.run(debug=True)