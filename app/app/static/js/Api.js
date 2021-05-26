export default class Api {

    api = '/api';

    async search(params) {
        let response;
        
        try {
            response = await fetch(this._buildRequestUri(params), {
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

    async analyzePost(formData) {
        let response;
        
        try {
            response = await fetch(this._buildAnalyzePostUri(), {
                method: 'POST',
                body: this._encodeFormData(formData)
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

    _encodeFormData(formData) {
        const data = new URLSearchParams();

        for (let pair of formData) {
            data.append(pair[0], pair[1]);
        }

        return data;
    }

    _buildRequestUri({ termo, dtInicial, dtFinal }) {
        //return `${this.api}/${encodeURIComponent(termo)}/${dtInicial}/${dtFinal}`;
        const params = this._to_query_string({ term: termo, start: dtInicial, end: dtFinal });

        return `${this.api}/search?${params}`;
    }

    _buildAnalyzePostUri() {
        return `${this.api}/post`;
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