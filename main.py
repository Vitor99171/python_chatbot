import os
import logging
from typing import List
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200

def format_response(texts: List[str]) -> jsonify:
    return jsonify({"fulfillmentMessages": [{"text": {"text": texts}}]})

@app.route('/dialogflow', methods=['POST'])
def dialogflow():
    data = request.get_json()

    # Verificar a estrutura recebida
    logger.info(f"Recebido JSON: {data}")

    action = data['queryResult'].get('action', 'Unknown Action')
    parameters = data['queryResult'].get('parameters', {})
    
    # Extrair callback_data corretamente da requisição do Telegram
    callback_data = data['originalDetectIntentRequest']['payload']['data']['callback_query'].get('data')

    # Usando logs ao invés de print
    logger.info(f"action: {action}")
    logger.info(f"callback_data: {callback_data}")

    # Tratar diferentes ações baseadas na intent detectada
    if action == 'defaultWelcomeIntent':
        response = format_response(['Olá! Como posso te ajudar hoje? Escolha uma das opções.'])

    elif action == 'agendar_servico':
        response = format_response(['Para agendar um serviço como RG, CNH ou Passaporte, acesse nosso portal de agendamentos.'])

    elif action == 'horario_atendimento':
        response = format_response(['Os horários de atendimento das centrais são de segunda a sexta, das 8h às 17h.'])

    elif action == 'localizacao_central':
        response = format_response(['Você pode encontrar a central mais próxima usando nosso localizador online.'])

    elif action == 'status_solicitacao':
        response = format_response(['Para verificar o status da sua solicitação, forneça o número do protocolo no site.'])

    elif action == 'resolucao_problemas':
        response = format_response(['Caso tenha perdido um documento ou enfrentado problemas com o pagamento, visite nossa página de suporte.'])

    elif action == 'suporte_tecnico':
        response = format_response(['Se você está com dificuldades para acessar o sistema de agendamentos, entre em contato com o suporte técnico.'])

    else:
        response = format_response([f'Ação não reconhecida: {action}.'])

    return response

if __name__ == '__main__':
    # Pegar a porta da variável de ambiente ou usar 5000 como padrão
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port)
