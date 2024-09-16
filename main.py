import os
from typing import List
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200


def format_response(texts: List[str]) -> jsonify:
    return jsonify({"fulfillmentMessages": [{"text": {"text": texts}}]})


@app.route('/dialogflow', methods=['POST'])
def dialogflow():
    data = request.get_json()

    action = data['queryResult']['action']

    # Tratar diferentes ações baseadas na intent detectada
    if action == 'defaultWelcomeIntent':
        response = format_response(['Hi, how can I help you today?'])

    elif action == 'input.welcome':
        response = format_response(['testando resposta', 'apareceu aii?'])

    elif action == 'teste.action':
        # Aqui é onde você trataria o callback_data
        # Verificar os parâmetros passados na intent
        parameters = data['queryResult'].get('parameters', {})
        callback_data = parameters.get('callback_data')

        if callback_data == 'opcao_1':
            response = format_response(['opção 1 selecionada'])
        elif callback_data == 'opcao_2':
            response = format_response(['opção 2 selecionada'])
        else:
            response = format_response(['Nenhuma opção válida foi selecionada.'])

    elif action == 'inputUnknown':
        response = format_response(['Sorry, I did not understand that clearly.'])

    else:
        response = format_response([f'No handler for the action name {action}.'])

    return response


if __name__ == '__main__':
    # Pegar a porta da variável de ambiente ou usar 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
