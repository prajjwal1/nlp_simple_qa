import pysolr
import os

LOC_ARTICLES = 'data/articles/'   # Where Articles to be Indexed are Stored

# Create a Client Instance
solr = pysolr.Solr('http://localhost:8983/solr/gettingstarted', always_commit=True, timeout=10)

def ping_server():
  '''Ping Server to Check if it is Alive'''
  solr.ping()

def index_articles():
  '''Load File Id (Title) & Text from Articles Folder into Entries List'''
  entries = []
  for filename in os.listdir(LOC_ARTICLES):
    entry = { "id": filename.split('.')[0] }
    with open(f'{LOC_ARTICLES}/{filename}', 'r', encoding="utf8") as f:
      entry['text'] = f.read().strip()
    entries.append(entry)
  solr.add(entries)               # Add Entries List to the Indexer

def search(query: str):
  '''Search for a String Query in the Index
  Returns a List of Documents that match the Query'''
  return [x['id'] for x in solr.search(f'text:{query}').docs]
