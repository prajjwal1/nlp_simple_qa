import pysolr

# Create a client instance. The timeout and authentication options are not required.
solr = pysolr.Solr('http://localhost:8983/solr/', always_commit=True)

# Indexing the Data
solr.add([
    {
        "id": "doc_1",
        "title": "A test document",
    },
    {
        "id": "doc_2",
        "title": "The Banana: Tasty or Dangerous?",
        "_doc": [
            { "id": "child_doc_1", "title": "peel" },
            { "id": "child_doc_2", "title": "seed" },
        ]
    },
])