import * as DOMutil from '../util/dom.js';

export default class FieldFilter {

    listeners = [];
    options = [];
    inverted = false;
    panelExpandedClass = 'expand';

    constructor(containerElement) {
        this.container = containerElement;
        this._bindContainer();
        this.setOptions([
            {value: 'numeroProcesso', name: 'Nº Processo', selected: true},
            {value: 'objeto', name: 'Objeto', selected: true},
            {value: 'valor', name: 'Valor'},
            {value: 'notaEmpenho', name: 'Nota de Empenho'},
            {value: 'signatarios', name: 'Signatários', selected: true},
            {value: 'dataPublicacao', name: 'Dt. Publicação'},
            {value: 'envolvidos', name: 'Envolvidos'}
        ]);
    }

    getState() {
        return new FilterState(this.options, this.inverted);
    }

    setOptions(options) {
        this.options = options.map(({ name, value, selected }) => {
            return new Option(value, name, selected);
        });
        this._renderOptions();
    }

    addListener(listener) {
        this.listeners.push(listener);
    }

    togglePanel = () => {
        DOMutil.toggleClassName(this.panelExpandedClass, this.container);
    }

    isPanelOpen() {
        return this.container.classList.contains(this.panelExpandedClass);
    }

    _bindContainer() {
        const label = this.container.querySelector('.filter-label');
        label.addEventListener('click', this.togglePanel);
        
        const invertControl = this.container.querySelector('.invert-control > input');
        invertControl.addEventListener('change', this._onInvertControlChange);

        const invertLabel = this.container.querySelector('.invert-control');
        invertLabel.addEventListener('click', ({ target }) => {
            if (target.tagName !== 'INPUT') {
                invertControl.click();
            }
        });

        document.body.addEventListener('click', ({ target }) => {
            if (this.isPanelOpen() && !DOMutil.isParentInTree(target, this.container)) {
                this.togglePanel();
            }
        });
    }

    _renderOptions() {
        const container = this.container.querySelector('.options-container > .list');
        container.innerHTML = '';

        this.options.forEach(option => {
            container.append(option.createElement(op => {
                this._onOptionsChange(op);
            }));
        });
    }

    _onOptionsChange(option) {
        this._emitEvent({ type: 'option-change', option });
    }

    _onInvertControlChange = (event) => {
        this.inverted = !this.inverted;
        this._emitEvent({ type: 'invert' });
    }

    _emitEvent(event) {
        this.listeners.forEach(listener => {
            listener(event, this.getState());
        });
    }

}

class Option {
    selected = false;

    constructor(value, name, selected) {
        this.value = value;
        this.name = name;
        if (selected) {
            this.selected = selected;
        }
    }

    createElement(selectionListener = () => {}) {
        const option = document.createElement('div');
        option.setAttribute('data-value', this.value);

        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = this.selected;
        input.addEventListener('change', event => {
            this.selected = !this.selected;
            selectionListener(this);
        });
        option.append(input);

        const label = document.createElement('span');
        label.innerText = this.name;
        option.append(label);

        option.addEventListener('click', event => {
            if (event.target.tagName !== 'INPUT') {
                input.click();
            }
        });

        return option;
    }
}

class FilterState {
    constructor(options, inverted) {
        this.options = options;
        this.inverted = inverted;
        this.selectedValues = this.options
            .filter(op => op.selected)
            .map(op => op.value);
    }

    isDocumentAccepted(doc) {
        const { fields } = doc.context;

        if (!this.selectedValues.length) {
            return true;
        }

        const selectedFields = this.selectedValues.filter(val => val in fields);

        const allFieldsSelected = selectedFields.length === this.selectedValues.length;

        if (!this.inverted) {
            return allFieldsSelected;
        }

        return !allFieldsSelected;
    }
}