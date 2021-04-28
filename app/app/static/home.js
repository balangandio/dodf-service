window.app = (function() {

    class AppForm {
        constructor(formElement) {
            this.formElement = formElement;
        }

        getInputs() {
            return {
                termo: this.formElement.termo,
                dtInicial: this.formElement.dtInicial,
                dtFinal: this.formElement.dtFinal
            };
        }

        getData() {
            const inputs = this.getInputs();

            return Object.keys(inputs).reduce((obj, key) => (
                { ...obj, [key]: inputs[key].value }
            ), {});
        }

        setEnabled(enabled) {
            enabled
                ? this.formElement.classList.remove('disabled')
                : this.formElement.classList.add('disabled');

            const buttons = this.formElement.getElementsByTagName('button');

            Object.values(this.getInputs())
                .concat(Array.from(buttons))
                .forEach(input => input.disabled = !enabled);
        }
    }

    class DataList {
        constructor(containerElement) {
            this.containerElement = containerElement;
        }

        setResults(requestResult) {
            const documents = (requestResult.result && requestResult.result.documents) || [];
            
            this.containerElement.innerHTML = '';

            documents.forEach(doc => {
                this.containerElement.append(this._createDocument(doc));
            });
        }

        setVisibility(visible) {
            visible
                ? this.containerElement.classList.remove('hided')
                : this.containerElement.classList.add('hided');
        }

        _createDocument(doc) {
            const docContainer = document.createElement('div');
            docContainer.className = 'document-container';

            const titleContainer = document.createElement('div');
            titleContainer.className = 'document-title';
            docContainer.append(titleContainer);
            titleContainer.innerText = doc.titulo;

            const contentContainer = document.createElement('div');
            contentContainer.className = 'document-content';
            docContainer.append(contentContainer);
            contentContainer.insertAdjacentHTML('beforeend', doc.texto);

            return docContainer;
        }
    }

    return {
        api: '',
        async onFormSubmit(formElement, event) {
            event && event.preventDefault();

            const form = new AppForm(formElement);
            const dataList = new DataList(document.querySelector('.data-container'));

            form.setEnabled(false);
            dataList.setVisibility(false);
            try {
                const data = this.validateFormaData(form.getData());

                const requestResult = await this.request(data);

                dataList.setResults(requestResult);
            } catch(err) {
                alert(err);
            } finally {
                form.setEnabled(true);
                dataList.setVisibility(true);
            }
        },
        setResults(requestResult) {
            const documents = (requestResult.result && requestResult.result.documents) || [];
            
            const container = document.querySelector('.data-container');
            container.innerHTML = '';

            documents.forEach(doc => {
                container.append(this._createDocument(doc));
            });
        },
        validateFormaData({ termo, dtInicial, dtFinal }) {
            if (!termo) {
                throw 'Termo não informado';
            }

            dtInicial = this._parseData(dtInicial);
            dtFinal = this._parseData(dtFinal);
            
            return { termo, dtInicial, dtFinal };
        },
        async request({ termo, dtInicial, dtFinal }) {
            let response;
            try {
                response = await fetch(`${this.api}/${termo}/${dtInicial}/${dtFinal}`, {
                    method: 'GET'
                });
            } catch(err) {
                throw 'Ocorreu um erro ao solicitar o serviço - ' + err;
            }

            if (response.status !== 200) {
                throw 'Serviço retornou status não esperado';
            }

            try {
                return response.json();
            } catch(err) {
                throw 'Error ao processar resposta do serviço - ' + err
            }
        },
        _parseData(data) {
            if (!data || typeof data !== 'string') {
                throw `A data informada [${data}] é inválida`;
            }

            const groups = /^([0-9]{2})\/([0-9]{2})\/([0-9]{4})$/.exec(data);

            if (groups == null) {
                throw `A data informada [${data}] é inválida`;
            }

            const [_, dia, mes, ano] = groups;

            return `${ano}-${mes}-${dia}`;
        }
    };
})();

document.addEventListener('DOMContentLoaded', e => {
    window.app.onFormSubmit(document.querySelector('form'))
});