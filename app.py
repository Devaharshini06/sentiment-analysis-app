
from flask import Flask, render_template, request
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import uuid
print("Running This app.py") 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiment = None
    polarity = 0
    emoji = ''
    message = ''
    bg_color = ''
    chart_filename = None
    wordcloud_filename = None
    if request.method == 'POST':
        text = request.form['text']
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.2:
            sentiment = "Positive"
            emoji = "😊"
            message = "Your message has a positive vibe!"
            bg_color = "#d4edda"
        elif polarity < -0.2:
            sentiment = "Negative"
            emoji = "😞"
            message = "Oops! That felt negative."
            bg_color = "#f8d7da"
        else:
            sentiment = "Neutral"
            emoji = "😐"
            message = "That's a neutral statement."
            bg_color = "#fff3cd"

        # Pie chart
        chart_filename = f"{uuid.uuid4().hex}_pie.png"
        chart_path = os.path.join(app.config['UPLOAD_FOLDER'], chart_filename)
        labels = ['Positive', 'Neutral', 'Negative']
        sizes = [max(polarity, 0), 1 - abs(polarity), max(-polarity, 0)]
        colors = ['#28a745', '#ffc107', '#dc3545']
        plt.figure(figsize=(4, 4))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()

        # Word Cloud
        wordcloud_filename = f"{uuid.uuid4().hex}_wc.png"
        wc_path = os.path.join(app.config['UPLOAD_FOLDER'], wordcloud_filename)
        wc = WordCloud(width=600, height=300, background_color='white').generate(text)
        wc.to_file(wc_path)

        return render_template('index.html', sentiment=sentiment, polarity=polarity, emoji=emoji,
                               message=message, text=text, bg_color=bg_color,
                               chart=chart_filename, wordcloud=wordcloud_filename)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
