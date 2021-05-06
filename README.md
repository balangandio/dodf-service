# DODF search service

# Install
```
pip install -r app/app/requirements.txt
```

# Run
Execute Flask with script at: `run.[sh|bat]`

# Docker
Build and run:
```
docker build -t <image-name> .
docker run -d -p 4444:<external-port> --name=<container-name> <image-name>
```
Auxiliar script at: `start-docker.sh`

# Request: `/api/<term>/<start_date>/<end_date>`
```
GET /api/contrato/2021-03-21/2021-04-14
```
```json
{
    "term": "contrato",
    "start_date": "2021-03-21",
    "end_date": "2021-04-14",
    "result": {
        "documents": [
            {
                "context": {
                    "sentences": [
                        {
                            "sentence": "Processo: 00054.00007911/2019-97.",
                            "field": "Processo",
                            "value": "00054.00007911/2019-97."
                        }
                    ]
                },
                "document": {
                    "dt_previsao_publicacao": "2021-03-22 08:00:00",
                    "letra_jornal": null,
                    "nome": "Administração Regional do Núcleo Bandeirante",
                    "num_jornal": "54",
                    "num_ordem_demandante": "67",
                    "num_ordem_tipo_materia": "999",
                    "num_regra_tipo_jornal": "31",
                    "ordem_tipo_materia_secao": null,
                    "preambulo": null,
                    "row_number": "4",
                    "secao": "Seção III",
                    "texto": "<p style=\"text-align:justify;\">Com fulc",
                    "tipo": "Reconhecimento de dívida",
                    "tipo_jornal": "Normal",
                    "titulo": "RECONHECIMENTO DE DÍVIDA"
                }
            }
        ],
        "previsao_publicacao": {
            "inicial": "2021-03-22 08:00:00",
            "final": "2021-04-13 08:00:00"
        },
        "total_of_documents": 779
    }
}
```

# Service
```
GET https://dodf.df.gov.br/default/index/resultado-json?termo=%22contrato%22&tpBusca=Contexto&tpSecao=Todas&tpJornal=Todos&tpLocalBusca=tudo&dtInicial=13/04&dtFinal=14/04&ano=2021
```
```json
{
	"paginacao": {
        "tmgPaginas": 10,
        "numPaginas": 4,
        "pgAtual": 1
    },
	"ttLocalizado": 36,
    "result": true,
    "lstDocumentos": [
		{
			"RowNumber": "2",
            "titulo": "EXTRATO DO PRIMEIRO TERMO ADITIVO AO CONTRATO Nº 16/2020",
            "preambulo": null,
			"texto": "<p>fwefwefewfwef</p>",
			"ds_nome": "Departamento de Logística e Finanças",
            "dt_previsao_publicacao": "2021-04-13 08:00:00",
            "ds_descricao_jornal_tipo": "Normal",
            "nu_ordem_demandante": "451",
            "co_regra_jornal_tipo": "31",
            "numero_jornal": "68",
            "letra_jornal": null,
            "tipo": "Extrato",
            "nu_ordem_tp_materia": "19",
            "ds_secao": "Seção III",
            "ordem_tp_materia_secao": null
		}
	]
}
```