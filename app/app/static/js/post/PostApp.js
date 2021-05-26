import Api from '../Api.js';
import FieldsRender from './FieldsRender.js';
import SentencesRender from './SentencesRender.js';

export default class PostApp {
    api = new Api();
    inputDelay = 500;
    timerId = null;

    init = () => {
        this.form = document.querySelector('#post_form ');

        const input = this.form.texto;
        input.addEventListener('input', evt => this._debounceFunction(this._onPostInputChange, this.inputDelay));

        const sentencesContainer = document.querySelector('.sentences-content');
        const fieldsContainer = document.querySelector('.fields-content');

        this.sentencesRender = new SentencesRender(sentencesContainer);
        this.fieldsRender = new FieldsRender(fieldsContainer);

        if (input.value) {
            this._onPostInputChange();
        }
    }

    _onPostInputChange = async () => {
        const texto = this.form.texto.value.trim();

        if (!texto) {
            return;
        }

        const formData = new FormData(this.form);

        try {
            const requestResult = await this.api.analyzePost(formData);

            const { sentences, fields } = requestResult.context;

            this.sentencesRender.render(sentences);
            this.fieldsRender.render(fields);
        } catch(err) {
            console.error(err);
            alert(err);
        }
    }

    _debounceFunction = (func, delay) => {
        clearTimeout(this.timerId);
    
        this.timerId = setTimeout(func, delay);
    }
}