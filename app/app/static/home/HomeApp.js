import AppForm from './AppForm.js';
import DataList from './DataList.js';

export default class HomeApp {

    api = '/api';

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

    async request(params) {
        const buildRequestUri = ({ termo, dtInicial, dtFinal }) => {
            //return `${this.api}/${encodeURIComponent(termo)}/${dtInicial}/${dtFinal}`;
            const params = this._to_query_string({ term: termo, start: dtInicial, end: dtFinal });

            return `${this.api}/search?${params}`;
        };

        let response;
        try {
            response = await fetch(buildRequestUri(params), {
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

    _to_query_string(obj) {
        const str = [];
        for (let p in obj) {
            if (obj.hasOwnProperty(p)) {
                str.push(`${encodeURIComponent(p)}=${encodeURIComponent(obj[p])}`);
            }
        }
        return str.join('&');
    }
}