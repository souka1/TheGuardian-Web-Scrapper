from flask import Flask, request, render_template
import pymongo



app = Flask(__name__)


MONGO_URI = 'mongodb+srv://user-1:user@cluster0.6h3jr.mongodb.net/test?retryWrites=true&w=majority'
connection = pymongo.MongoClient(MONGO_URI)
db = connection['test']


# Return the home page
@app.route('/')
def index():
    return render_template('index.html')


# Retrieves and returns all the available articles in the mongodb collection.
@app.route('/showall')
def articles():
    page = int(request.args.get("page", "1"))
    num_articles = int(request.args.get("num_articles", "10"))
    skips = num_articles * (page - 1)

    result = db.test.find().limit(num_articles).skip(skips)
    result = [{"headline": ' '.join(map(str, data["headline"])),
               "content":data["content"],
               "author":' '.join(map(str, data["author"])),
               "category":' '.join(map(str, data["category"])),
               "published_at":data["published_at"],
               "url":data["url"] }  for data in result]

    return  render_template('searchlist.html', news=result)


# Search and retrieve articles by keyword
@app.route('/search')
def search_content():
    query = request.args.get("text", "")
    query = query.replace(" ", "|")

    page = int(request.args.get("page", "1"))
    num_articles = int(request.args.get("num_articles", "5"))
    skips = num_articles * (page - 1)

    result = db.test.find({ "$or" : [ { "content": {"$regex": query, "$options": "ig"}},{"author": {"$regex": query, "$options": "ig"}}, { "category": {"$regex": query, "$options": "ig"}}, { "headline": {"$regex": query, "$options": "ig"}}]}).limit(num_articles).skip(skips)
    result = [{"headline": ' '.join(map(str, data["headline"])),
               "content": data["content"],
               "author": ' '.join(map(str, data["author"])),
               "category": ' '.join(map(str, data["category"])),
               "published_at": data["published_at"],
               "url": data["url"]} for data in result]
    return render_template('searchlist.html', news=result)


