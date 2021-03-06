from elasticsearch import Elasticsearch


# Connect to Elastic Search

class export_elastic_search(object):
	
	def __init__(self, index = "opensemanticsearch"):
	
		self.verbose=False
	
		self.config = {}
		self.config['index'] = index
		self.config['verbose'] = self.verbose


	#
	# Write data to Elastic Search
	#

	def process (self, parameters={}, data={} ):

		self.config = parameters

		# if not there, set config defaults
		if 'verbose' in self.config:
			self.verbose = self.config['verbose']
	
		if 'elastic' in parameters:
			self.elastic = parameters['elastic']

		if 'index' in parameters:
			self.index = parameters['index']

	

		# post data to solr
		self.update(data=data)
	
		return parameters, data

	
	
	# send the updated field data to Solr
	def update(self, docid=None, data=[]):
	
		if docid:
			data['id'] = docid
		else:
			docid = data['id']
			
		es = Elasticsearch()
		result = es.index(index=self.index, doc_type='document', id=docid, body=data)

		return result
	
	
	def get_lastmodified(self, docid, parameters = {}):
	
	
		es = Elasticsearch()

		doc_exists = es.exists(index=self.index, doc_type="document", id=docid)

		# if doc with id exists in index, read modification date
		if doc_exists:	
			doc = es.get(index=self.index, doc_type="document", id=docid, _source=False, fields="file_modified_dt")
			last_modified = doc['fields']['file_modified_dt'][0]
		else:
			last_modified=None
			
		return last_modified
