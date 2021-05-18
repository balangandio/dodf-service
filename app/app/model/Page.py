from datetime import datetime

from .Context import ContratoContext


class Page:
    def __init__(self, json_result):
        self.details = PageDetails(json_result['paginacao'])
        self.total_overall = json_result['ttLocalizado']
        valid_docs = filter(lambda json : Document.is_valid_doc(json), json_result['lstDocumentos'])
        self.documents = list(map(lambda json : Document(json), valid_docs))
        self.total_in_page = len(self.documents)


class PageDetails:
    def __init__(self, result):
        self.current = result['pgAtual']
        self.total_per_page = result['tmgPaginas']
        self.total_pages = result['numPaginas']

    def is_last_page(self):
        return self.current >= self.total_pages


class Document(object):
    def __init__(self, json_result: dict):
        self.props_dict = json_result

    @property
    def titulo(self):
        return self.props_dict['titulo']

    @property
    def texto(self):
        return self.props_dict['texto']

    @property
    def row_number(self):
        return self.props_dict['RowNumber']

    @property
    def preambulo(self):
        return self.props_dict['preambulo']

    @property
    def nome(self):
        return self.props_dict['ds_nome']

    @property
    def dt_previsao_publicacao(self):
        return self.props_dict['dt_previsao_publicacao']

    @property
    def tipo_jornal(self):
        return self.props_dict['ds_descricao_jornal_tipo']

    @property
    def num_ordem_demandante(self):
        return self.props_dict['nu_ordem_demandante']

    @property
    def num_regra_tipo_jornal(self):
        return self.props_dict['co_regra_jornal_tipo']

    @property
    def num_jornal(self):
        return self.props_dict['numero_jornal']

    @property
    def letra_jornal(self):
        return self.props_dict['letra_jornal']

    @property
    def tipo(self):
        return self.props_dict['tipo']

    @property
    def num_ordem_tipo_materia(self):
        return self.props_dict['nu_ordem_tp_materia']

    @property
    def secao(self):
        return self.props_dict['ds_secao']

    @property
    def ordem_tipo_materia_secao(self):
        return self.props_dict['ordem_tp_materia_secao']

    def to_dict(self):
        return {
            'row_number': self.row_number,
            'titulo': self.titulo,
            'texto': self.texto,
            'preambulo': self.preambulo,
            'nome': self.nome,
            'dt_previsao_publicacao': self.dt_previsao_publicacao,
            'tipo_jornal': self.tipo_jornal,
            'num_ordem_demandante': self.num_ordem_demandante,
            'num_regra_tipo_jornal': self.num_regra_tipo_jornal,
            'num_jornal': self.num_jornal,
            'letra_jornal': self.letra_jornal,
            'tipo': self.tipo,
            'num_ordem_tipo_materia': self.num_ordem_tipo_materia,
            'secao': self.secao,
            'ordem_tipo_materia_secao': self.ordem_tipo_materia_secao
        }

    @staticmethod
    def is_valid_doc(doc_dict):
        return 'texto' in doc_dict and 'titulo' in doc_dict


class PageCollection:
    def __init__(self, pages=[]):
        self.pages = pages

    def extend(self, collection):
        self.pages.extend(collection.pages)
        return self

    def all_documents(self):
    	documents = []

    	for page in self.pages:
    		documents.extend(list(map(lambda doc : doc, page.documents)))

    	return documents

    def to_dict(self):
        documents = self.all_documents()

        result = {
            'documents': list(map(lambda doc : self._document_dict(doc), documents)),
            'total_of_documents': len(documents)
        }

        if len(documents) > 0:
        	(lowest_date, biggest_date) = self._find_previsao_publicacao(documents)
        	result['previsao_publicacao'] = {
            	'inicial': lowest_date.strftime('%Y-%m-%d %H:%M:%S'),
            	'final': biggest_date.strftime('%Y-%m-%d %H:%M:%S')
            }

        return result

    def _find_previsao_publicacao(self, documents):
    	lowest_date = None
    	biggest_date = None

    	for doc in documents:
    		if doc is not None:
    			doc_date = datetime.strptime(doc.dt_previsao_publicacao, '%Y-%m-%d %H:%M:%S')

    			if lowest_date is None:
    				lowest_date = doc_date
    			elif doc_date < lowest_date:
    				lowest_date = doc_date

    			if biggest_date is None:
    				biggest_date = doc_date
    			elif doc_date > biggest_date:
    				biggest_date = doc_date

    	return (lowest_date, biggest_date)

    def _document_dict(self, doc):
        context = ContratoContext(doc)

        return {
            'document': doc.to_dict(),
            'context': context.to_dict()
        }