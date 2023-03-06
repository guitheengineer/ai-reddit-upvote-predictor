from flask import Flask, render_template, request
import praw
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.debug = True  # debug mode is required for templates to be reloaded

model_card = "microsoft/DialogRPT-updown"   # you can try other model_card listed in the table above
tokenizer = AutoTokenizer.from_pretrained(model_card)
model = AutoModelForSequenceClassification.from_pretrained(model_card)


reddit = praw.Reddit(client_id=os.environ.get('CLIENT_ID'),
                     client_secret=os.environ.get('CLIENT_SECRET'),
                     user_agent='upvote-predictor by guilhermefront')



def score(context, hyp):
    model_input = tokenizer.encode(context + "<|endoftext|>" + hyp, return_tensors="pt")
    result = model(model_input, return_dict=True)
    return torch.sigmoid(result.logits)



@app.route('/')
def index():
    search = request.args.get('search', '')
    comment = request.args.get('comment', '')
    upvote_probability = ''

    if search and comment:
        post = reddit.submission(url=search)
        title = post.title
        content = post.selftext

        context = title + ' ' + content

        upvote_probability = '%.3f' % score(context, comment)

    
    return render_template('index.html', search=search, comment=comment, upvote_probability=upvote_probability)
