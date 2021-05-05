from datetime import datetime

from Context import ContratoContext


class Page:
    def __init__(self, json_result):
        self.details = PageDetails(json_result['paginacao'])
        self.total_overall = json_result['ttLocalizado']
        self.documents = list(map(lambda json : Document(json), json_result['lstDocumentos']))
        self.total_in_page = len(self.documents)


class PageDetails:
    def __init__(self, result):
        self.current = result['pgAtual']
        self.total_per_page = result['tmgPaginas']
        self.total_pages = result['numPaginas']

    def is_last_page(self):
        return self.current >= self.total_pages


class Document:
    def __init__(self, result):
        self.row_number = result['RowNumber']
        self.titulo = result['titulo']
        self.texto = result['texto']
        self.preambulo = result['preambulo']
        self.nome = result['ds_nome']
        self.dt_previsao_publicacao = result['dt_previsao_publicacao']
        self.tipo_jornal = result['ds_descricao_jornal_tipo']
        self.num_ordem_demandante = result['nu_ordem_demandante']
        self.num_regra_tipo_jornal = result['co_regra_jornal_tipo']
        self.num_jornal = result['numero_jornal']
        self.letra_jornal = result['letra_jornal']
        self.tipo = result['tipo']
        self.num_ordem_tipo_materia = result['nu_ordem_tp_materia']
        self.secao = result['ds_secao']
        self.ordem_tipo_materia_secao = result['ordem_tp_materia_secao']

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