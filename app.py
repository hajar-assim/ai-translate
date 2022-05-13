import openai
from flask import Flask, redirect, url_for, render_template, request
from api_secrets import API_KEY

app = Flask(__name__)

# api key, make sure to gitignore
openai.api_key = API_KEY

# storing the translation history
box = []

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":

        lang = (request.form["language"]).capitalize()
        sentence = request.form["sentence"].capitalize()

        # open ai info
        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt= (returntext().format(sentence, lang.capitalize())),
        temperature=0.3,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )

        # vars
        aitext = response["choices"][0]["text"]
        storage_dict = {"Language:":lang, "Sentence:": sentence, "Translation:": aitext}
        box.insert(0,storage_dict)

        # debugging
        print(lang)
        print(box)

        return render_template("index.html", result=aitext, stored = box, storedlength = len(box))

    # understand this line of code
    result = request.args.get("result")
    return render_template("index.html")


def returntext():
    return """Translate this to Polish:

Winter is my favorite season.

Zima jest moją ulubioną porą roku.

Translate this to French:

I love hiking.

J'adore la randonnée.

Translate this to Arabic:

I love you, mother.

أنا أحبك أمي

Translate this into {1}:

{0}
    """

if __name__ == "__main__":
    app.run()
