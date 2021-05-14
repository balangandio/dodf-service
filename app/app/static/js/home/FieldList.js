import ContextList from './ContextList.js';

export default class FieldList extends ContextList {
    renders = [
        {'numeroProcesso': this._renderNumProcessoItem},
        {'objeto': this._renderObjetoItem},
        {'valor': this._renderValorItem},
        {'notaEmpenho': this._renderNotaEmpenhoItem},
        {'signatarios': this._renderSignatarioItem},
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

            const objList = document.createElement('ul');
            const subItem = document.createElement('li');
            subItem.innerText = agent;
            objList.append(subItem);

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
}