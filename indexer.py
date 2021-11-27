import pysolr
import os

LOC_ARTICLES = 'articles/'             # Where Articles are Stored to be Indexed

# Create a Client Instance
solr = pysolr.Solr('http://localhost:8983/solr/', always_commit=True, timeout=10)

# Load File Title & Text from Articles Folder into Entries List
entries = []
for filename in os.listdir(LOC_ARTICLES):
  entry = { "id": filename.split('.')[0] }  # id = title
  with open(f'{LOC_ARTICLES}/{filename}') as f:
    entry['title'] = f.readlines()          # title = text
  entries.append(entry)

# Add Entries List to the Indexer
solr.add(entries)

# Search with Solr
# results = solr.search('bananas')
