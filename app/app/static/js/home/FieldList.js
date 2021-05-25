import ContextList from './ContextList.js';
import * as DOMutil from '../util/dom.js';

export default class FieldList extends ContextList {
    renders = [
        {'numeroProcesso': this._renderNumProcessoItem},
        {'objeto': this._renderObjetoItem},
        {'valor': this._renderValorItem},
        {'notaEmpenho': this._renderNotaEmpenhoItem},
        {'envolvidos': this._renderEnvolvidos},
        {'signatarios': this._renderSignatarioItem},
        {'assinatura': this._renderAssinatura},
        {'vigencia': this._renderVigencia},
        {'adicionais': this._renderAdicionais},
        {'dataPublicacao': this._renderDataPublicacao}
    ];

    constructor(fields = {}) {
        super('fields');
        this.fields = fields;
    }
    
    renderToggle() {
        const total = Object.keys(this.fields).length;
        const toggle = super.renderToggle();
        toggle.innerText = `Campos: ${total}`;
        if (!total) {
            toggle.setAttribute('disabled', 'true');
        }
        return toggle;
    }

    renderList() {
        const list = super.renderList();

        const fields = [];

        this.renders.forEach(render => {
            for (let field in render) {
                if (field in this.fields) {
                    fields.push(field);
                }
            }
        });

        fields.forEach(field => {
            list.append(this._createFieldItem(field, this.fields[field]));
        });

        return list;
    }

    _createFieldItem(fieldName, fieldValue) {
        const item = document.createElement('li');

        const name = document.createElement('span');
        name.innerText = fieldName;
        item.append(name);

        const valueList = document.createElement('ul');

        this.renders.forEach(render => {
            for (let field in render) {
                if (field === fieldName) {
                    render[field](fieldValue, valueList);
                    item.setAttribute('data-field', field);
                }
            }
        });

        item.append(valueList);

        return item;
    }

    _renderNumProcessoItem(numProc, list) {
        const valueItem = document.createElement('li');
        valueItem.innerText = numProc;
        list.append(valueItem);
    }

    _renderSignatarioItem(signatarios, list) {
        signatarios.forEach(({ entity, agent }) => {
            const item = document.createElement('li');

            const desc = document.createElement('span');
            desc.innerText = entity;
            item.append(desc);

            const objList = DOMutil.createList([agent]);

            item.append(objList);
            list.append(item);
        });
    }

    _renderObjetoItem(value, list) {
        const item = document.createElement('li');
        item.innerText = value;
        list.append(item);
    }

    _renderValorItem({ currency, value }, list) {
        const formatter = new Intl.NumberFormat(undefined, {
            minimumFractionDigits: 2
        });
        const item = document.createElement('li');
        item.innerText = `${currency} ${formatter.format(value)}`;
        list.append(item);
    }

    _renderNotaEmpenhoItem(notas, list) {
        notas.forEach(nota => {
            const item = document.createElement('li');
            item.innerText = nota;
            list.append(item);
        });
    }

    _renderDataPublicacao(dt, list) {
        const item = document.createElement('li');
        item.innerText = dt;
        list.append(item);
    }

    _renderEnvolvidos(envolvidos, list) {
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

                const subList = DOMutil.createList(subListItems);
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

                const subList = DOMutil.createList(subListItems);
                item.append(subList);
            }

            list.append(item);
        });
    }

    _renderAssinatura(dtAssinatura, list) {
        const item = document.createElement('li');
        item.innerText = dtAssinatura;
        list.append(item);
    }

    _renderVigencia({ duration, interval }, list) {
        if (duration) {
            const { value, unit } = duration;
            const item = document.createElement('li');
            item.append(`${value} ${unit}`);

            list.append(item);
        }

        if (interval) {
            const { start, end } = interval;
            const item = document.createElement('li');
            let desc = '';
            if (start && end) {
                desc = `${start} à ${end}`;
            } else if (start) {
                desc = `a partir de ${start}`;
            } else if (end) {
                desc = `até ${end}`;
            }

            item.append(`${desc}`);

            list.append(item);
        }
    }

    _renderAdicionais(fields, list) {
        const labels = {
            'fontesRecurso': 'Fontes de recurso',
            'naturezasDespesa': 'Naturezas da despesa',
            'ug': 'UG/UO',
            'programasTrabalho': 'Programas de Trabalho'
        };

        Object.keys(labels).forEach(field => {
            if (field in fields) {
                let values = fields[field];

                if (Array.isArray(values)) {
                    values = values.join(', ');
                }

                const item = document.createElement('li');
                item.append(`${labels[field]}: ${values}`);
                list.append(item);
            }
        });
    }

}