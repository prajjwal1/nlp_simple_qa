from __future__ import print_function
import pysolr
from dataset_utils import load_data

solr = pysolr.Solr('http://localhost:8983/solr/', always_commit=True)

solr.ping()


