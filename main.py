#!/usr/bin/env python3
import markovify
import facebook
from flask import Flask
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import io

app = Flask(__name__)


# I'm writing this late at night
# I'm assuming there's an easier
# way to do this but I couldn't find it
def split_after_nth_spaces(_st, n):
    count = 0
    r = []
    val = ''
    for i in range(len(_st)-1):
        if count >= n and val[count-1] == ' ' or count == len(_st)-1:
            count = 0
            r.append(val)
            val = ''
        val += _st[i]
        count += 1
    r.append(val)
    return r


def stirner_quote(data, context):
    # Get raw text as string.
    with open('eaho.txt') as f:
        text = f.read()

    # Build the model.
    text_model = markovify.Text(text)

    sentence = text_model.make_sentence()

    base = Image.open('stirner.png').convert('RGBA')

    txt = Image.new('RGBA', base.size, (255,255,255,0))

    fnt = ImageFont.truetype('Helvetica-Regular.ttf', 50)
    d = ImageDraw.Draw(txt)
    n = 30
    it = 460

    for s in split_after_nth_spaces(sentence, n):
        it = it - 80
        d.text((300,base.size[1]-it), s, font=fnt, fill=(0,0,0,255))

    out = Image.alpha_composite(base, txt)
    saved = io.BytesIO()
    out.save(saved, format='PNG')
    saved.seek(0)

    with open('token') as f:
        token = f.read()
    graph = facebook.GraphAPI(access_token=token)
    graph.put_photo(image=saved.read())
    return "It worked!"
