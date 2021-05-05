import AppForm from './AppForm.js';
import DataList from './DataList.js';

export default class HomeApp {

    api = '';

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
    }

    setResults(requestResult) {
        const documents = (requestResult.result && requestResult.result.documents) || [];
        
        const container = document.querySelector('.data-container');
        container.innerHTML = '';

        documents.forEach(doc => {
            container.append(this._createDocument(doc));
        });
    }

    validateFormaData({ termo, dtInicial, dtFinal }) {
        if (!termo) {
            throw 'Termo não informado';
        }

        dtInicial = this._parseData(dtInicial);
        dtFinal = this._parseData(dtFinal);
        
        return { termo, dtInicial, dtFinal };
    }

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
    }

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
}