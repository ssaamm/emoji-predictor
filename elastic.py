import sys, sqlite3, emoji, re
from elasticsearch import Elasticsearch

es = Elasticsearch()

def ins():
    db = sqlite3.connect('data.db')
    cursor = db.cursor()
    cursor.execute("SELECT text FROM message")
    rows = cursor.fetchall()

    regExpr = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    
    i = 0
    for row in rows:
        if i % 10 == 0:
            print i
        if not regExpr.search(row[0]):
            continue
        doc = {
            'text' : row[0]
        }
        res = es.index(index="emoji-index", doc_type='message', id=i, body=doc)
        
        i += 1

def search(message):
    res = es.search(index="test-index", body={
        "query": {
            "query_string": {
                "query": message
            }
        }
    })
    print("Got %d hits:\n\n" % res['hits']['total'])
    for hit in res['hits']['hits']:
        print(emoji.emojize(hit["_source"]["text"]))

if __name__ == "__main__":
    pass
