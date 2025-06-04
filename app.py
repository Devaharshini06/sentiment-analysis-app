from flask import Flask, render_template, request
from textblob import TextBlob
from wordcloud import WordCloud
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return 'Positive', polarity
    elif polarity < -0.1:
        return 'Negative', polarity
    else:
        return 'Neutral', polarity

def generate_wordcloud(text):
    wc = WordCloud(width=400, height=300, background_color='white', colormap='plasma').generate(text)
    filename = f"{uuid.uuid4().hex}_wc.png"
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    wc.to_file(path)
    return filename

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    polarity = 0
    text = ""
    pie_data = {"Positive": 0, "Negative": 0, "Neutral": 0}
    emoji = ""
    wordcloud_file = None

    if request.method == "POST":
        text = request.form["text"]
        sentiment, polarity = analyze_sentiment(text)
        wordcloud_file = generate_wordcloud(text)

        if sentiment == "Positive":
            pie_data["Positive"] = 70
            pie_data["Neutral"] = 30
            emoji = "😊"
        elif sentiment == "Negative":
            pie_data["Negative"] = 70
            pie_data["Neutral"] = 30
            emoji = "😞"
        else:
            pie_data["Neutral"] = 100
            emoji = "😐"

    return render_template(
        "index.html",
        text=text,
        sentiment=sentiment,
        polarity=round(polarity, 3),
        emoji=emoji,
        pie_data=pie_data,
        wordcloud_file=wordcloud_file
    )

if __name__ == "__main__":
    app.run(debug=True)

