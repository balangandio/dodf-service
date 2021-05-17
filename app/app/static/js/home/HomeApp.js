import AppForm from './AppForm.js';
import DataList from './DataList.js';
import Api from '../Api.js';
import { parseDate } from '../util/date.js';
import FieldFilter from './FieldFilter.js';

export default class HomeApp {

    api = new Api();

    init = () => {
        this.fieldFilter = new FieldFilter(document.querySelector('.field-filter'));

        const form = document.querySelector('form');
        this.onFormSubmit(form);
    }

    async onFormSubmit(formElement, event) {
        event && event.preventDefault();

        const form = new AppForm(formElement);
        const dataList = new DataList(document.querySelector('.data-container'), this.fieldFilter);

        form.setEnabled(false);
        dataList.setVisibility(false);
        try {
            const data = this.validateFormaData(form.getData());

            const requestResult = await this.api.search(data);

            dataList.setResults(requestResult);
        } catch(err) {
            console.log(err);
            alert(err);
        } finally {
            form.setEnabled(true);
            dataList.setVisibility(true);
        }
    }

    validateFormaData({ termo, dtInicial, dtFinal }) {
        if (!termo) {
            throw 'Termo não informado';
        }

        dtInicial = parseDate(dtInicial);
        dtFinal = parseDate(dtFinal);
        
        return { termo, dtInicial, dtFinal };
    }

}