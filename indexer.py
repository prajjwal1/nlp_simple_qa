import pysolr
import os

LOC_ARTICLES = 'articles/'             # Where Articles are Stored to be Indexed


# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('http://localhost:8983/solr/', always_commit=True)

entries = []
for filename in os.listdir(LOC_ARTICLES):
  entry = {}
  entry['title'] = filename.split('.')[0]
  with open(f'{LOC_ARTICLES}/{filename}') as f:
    entry['text']= f.readlines()
  entries.append(entry)


# Indexing the Entries
solr.add(entries)

# How To Search
# results = solr.search('bananas')
