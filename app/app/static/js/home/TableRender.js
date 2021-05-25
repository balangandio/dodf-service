import { createList } from '../util/dom.js';

export default class TableRender {

    headers = [
        { header: 'Processo', field: 'numeroProcesso', render: this._renderProcesso },
        { header: 'Objeto', field: 'objeto', render: this._renderObjeto},
        { header: 'Valor', field: 'valor', render: this._renderValor },
        { header: 'Nota Empenho', field: 'notaEmpenho', render: this._renderNotas },
        { header: 'Signatários', field: 'signatarios', render: this._renderSignatarios },
        { header: 'Envolvidos', field: 'envolvidos', render: this._renderEnvolvidos },
        { header: 'Assinatura', field: 'assinatura', render: this._renderAssinatura },
        { header: 'Vigência', field: 'vigencia', render: this._renderVigencia },
        { header: 'Adicionais', field: 'adicionais', render: this._renderAdicionais },
        { header: 'Publicação', field: 'dataPublicacao', render: this._renderDtPublicacao }
    ];

    constructor(container) {
        this.container = container;
    }

    renderDocuments(documents, term) {
        this.container.innerHTML = '';

        const table = document.createElement('table');
        table.append(this._createHeader());
        table.append(this._createBody(documents, term));

        this.container.append(table);
    }

    _createHeader() {
        const header = document.createElement('thead');
        const row = document.createElement('tr');

        this.headers.forEach(({ header, field }) => {
            const th = document.createElement('th');
            th.setAttribute('data-field', field);
            th.innerText = header;
            row.append(th);
        });
        
        header.append(row);
        return header;
    }

    _createBody(documents, term) {
        const body = document.createElement('tbody');

        documents.forEach(({ context }) => {
            const row = document.createElement('tr');

            this.headers.forEach(header => {
                row.append(this._createDocumentCell(context.fields, header.field));
            });

            body.append(row);
        });

        return body;
    }

    _createDocumentCell(docFields, field) {
        const td = document.createElement('td');
        td.setAttribute('data-field', field);

        const value = docFields[field];

        if (value !== undefined) {
            this.headers.forEach(header => {
                if (header.field === field) {
                    header.render(value, td);
                }
            });
        }

        return td;
    }

    _renderProcesso(numProcesso, container) {
        container.innerText = numProcesso;
    }

    _renderObjeto(objeto, container) {
        container.innerText = objeto;
    }

    _renderValor(valor, container) {
        const formatter = new Intl.NumberFormat(undefined, {
            minimumFractionDigits: 2
        });
        const { currency, value } = valor;
        container.innerText = `${currency} ${formatter.format(value)}`;
    }

    _renderNotas(notas, container) {
        const list = createList(notas);
        container.append(list);
    }

    _renderSignatarios(signatarios, container) {
        const list = document.createElement('ul');

        signatarios.forEach(({ entity, agent }) => {
            const item = document.createElement('li');

            const desc = document.createElement('span');
            desc.innerText = entity;
            item.append(desc);

            const objList = createList([agent]);

            item.append(objList);
            list.append(item);
        });

        container.append(list);
    }

    _renderEnvolvidos(envolvidos, container) {
        const list = document.createElement('ul');

        envolvidos.forEach(({ role, ...env }) => {
            const item = document.createElement('li');

            if (role) {
                const desc = document.createElement('span');
                desc.innerText = `${role.substr(0, 1).toUpperCase()}${role.substr(1)}`;
                item.append(desc);

                const subListItems = Object.keys(env)
                    .map(prop => prop === 'cnpj'
                        ? `CNPJ: ${env[prop]}`
                        : env[prop]);

                const subList = createList(subListItems);
                item.append(subList);

            } else if (!Object.keys(env).length) {
                item.innerText = env.entity;
            } else {
                const { entity, ...props } = env;

                const desc = document.createElement('span');
                desc.innerText = entity;
                item.append(desc);

                const subListItems = Object.keys(props)
                    .map(prop => prop === 'cnpj'
                        ? `CNPJ: ${props[prop]}`
                        : props[prop]);

                const subList = createList(subListItems);
                item.append(subList);
            }

            list.append(item);
        });

        container.append(list);
    }

    _renderAssinatura(assinatura, container) {
        container.innerText = assinatura;
    }

    _renderVigencia(vigencia, container) {
        const { duration, interval } = vigencia;

        const items = [];

        if (duration) {
            const { value, unit } = duration;
            items.push(`${value} ${unit}`);
        }

        if (interval) {
            const { start, end } = interval;

            let desc = '';
            if (start && end) {
                desc = `${start} à ${end}`;
            } else if (start) {
                desc = `a partir de ${start}`;
            } else if (end) {
                desc = `até ${end}`;
            }

            items.push(`${desc}`);
        }

        if (items.length) {
            const list = createList(items);
            container.append(list);
        }
    }

    _renderAdicionais(fields, container) {
        const labels = {
            'fontesRecurso': 'Fontes de recurso',
            'naturezasDespesa': 'Naturezas da despesa',
            'ug': 'UG/UO',
            'programasTrabalho': 'Programas de Trabalho'
        };

        const items = Object.keys(labels).filter(f => f in fields).map(field => {
            let values = fields[field];

            if (Array.isArray(values)) {
                values = values.join(', ');
            }

            return `${labels[field]}: ${values}`;
        });

        if (items.length) {
            const list = createList(items);
            container.append(list);
        }
    }

    _renderDtPublicacao(dtPublicacao, container) {
        container.innerText = dtPublicacao;
    }
}