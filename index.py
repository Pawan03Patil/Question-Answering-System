from elasticsearch import Elasticsearch


class ElasticSearch:
    #default constructor initalizing elastic search object
    def __init__(self):
        # Elasticsearch configuration
        ES_HOST = {"host": "localhost", "port": 9200}
        INDEX_NAME = ['nlp1']

        self.es = Elasticsearch(hosts=[ES_HOST], http_auth=('', ''))

        request_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }

        #Creating indices if not already crated.
        for i in range(0, len(INDEX_NAME)):
            if not self.es.indices.exists(INDEX_NAME[i]):
                res = self.es.indices.create(index=INDEX_NAME[i], body=request_body)
                print("Index Created: ", i)
                print(res)
    #End INIT

    '''
    This method ingests data into 'trancripts' index.
    input: company symbol, transcript text to ingest, index name(i.e: transripts), document type(i.e: transcript)
    ouput: status of ingestion.
    '''
    def INDEX(self, filename, content, INDEX_NAME):
        res = self.es.index(index=INDEX_NAME, doc_type="QA", body={
            'company': filename,
            'content': content,
        })
    #End Ingest




    '''
    This method will search inside elasticsearch index and will return most relevant file with its name and content
    input:
    output: filename, content
    '''
    def SEARCH(self, INDEX_NAME, QUESTION):
        res = self.es.search(index=INDEX_NAME, body={
             "size":1,
            "query": {
                 "bool":{ 
                   "must":[      
                {"match": {
                    "content": QUESTION
                } }]
            }}
        })
        hits = res['hits']['hits']
        #print(hits)
        #print(len(hits))
        return hits[0]['_source']['company'], hits[0]['_source']['content'] 
    #End SEARCH



'''
for Testing the working Elastic.py

d.Search_news("oxy", "news")
d.Detail_News( "6WkfZmkB1DjPEw1zrLMQ", "news")
d = ElasticSearch()
d.Detail_Transcript("emkeZmkB1DjPEw1zNrMU", "transcripts")
'''

