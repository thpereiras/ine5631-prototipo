import os
from flask import Flask, jsonify, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.response_selection import get_random_response

botName="MyBot"
dbName="myBotData.sqlite3"

mybot = ChatBot(
    botName,
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        }
    ],
    #input_adapter="chatterbot.input.VariableInputTypeAdapter",
    #output_adapter="chatterbot.output.OutputAdapter",
    response_selection_method=get_random_response, # Uma alternativa seria get_most_frequent_response
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///"+dbName
)

### Training via list data
dialogs = [ # Perguntas e respostas em pares
    'Oi', 'Olá',
    'Olá', 'Oi',
    'Ola', 'Oi',
    'Adeus', 'Tchau',
    'Quem é você?', 'Sou um protótipo de chatbot desenvolvido para o TCC do Thiago.',
    'O que é você?', 'Sou um programa de computador!',
    'Qual é o seu nome?', 'Ainda não fui batizado :/',
    'Qual seu nome?', 'Ainda não fui batizado :/',
    'Cala a boca', 'Seja mais educado por favor!',
    'Tudo bem?', 'Ótimo',
    'Cante uma música', 'Ainda estou apreendendo a cantar.',
    'E ai como vai?', 'Muito bem',
    'E ai como vai?', 'Muito bem',
    'Tudo bem também', 'Que maravilha',
    'Tudo tranquilo', 'Que maravilha',
    'Tudo tudo ótimo', 'Que maravilha',
    'Tudo certo', 'Que maravilha',
    'Tchau', 'Até logo.',
    'Você gosta de programar?', 'Sim, eu programo em Python.',
    'Como vai?', 'Eu estou bem, obrigado.',
    'Oi, prazer em conhece-lo.', 'Obrigado. Prazer em conhece-lo também.',
    'Como está o tempo hoje?', 'Resfriado pelo cooler =)',
    'UFSC', 'Sigla para Universidade Federal de Santa Catarina',
    'Qual o objetivo do curso de Sistemas de Informação?', 'O curso de Sistemas de Informação da UFSC tem como objetivo formar profissionais que contribuam para a solução de problemas de tratamento de informação, por meio da concepção, construção e manutenção de modelos informatizados de automação corporativa, apoiados nos conceitos e técnicas de informática, teoria de sistemas e administração.',
    'Qual o objetivo do curso de Sistemas?', 'O curso de Sistemas de Informação da UFSC tem como objetivo formar profissionais que contribuam para a solução de problemas de tratamento de informação, por meio da concepção, construção e manutenção de modelos informatizados de automação corporativa, apoiados nos conceitos e técnicas de informática, teoria de sistemas e administração.',
    'Qual o objetivo do curso?', 'O curso de Sistemas de Informação da UFSC tem como objetivo formar profissionais que contribuam para a solução de problemas de tratamento de informação, por meio da concepção, construção e manutenção de modelos informatizados de automação corporativa, apoiados nos conceitos e técnicas de informática, teoria de sistemas e administração.',
    'Quantas vagas por semestre?', 'São 50 vagas por semestre.',
    'Qual a duração do curso de Sistemas de Informação?', 'O curso de Sistemas de Informação possui 9 semestres de duração.',
    'Qual a duração do curso de Sistemas?', 'O curso de Sistemas de Informação possui 9 semestres de duração.',
    'Qual a duração do curso?', 'O curso de Sistemas de Informação possui 9 semestres de duração.',
    'Qual o período do curso de Sistemas de Informação?', 'Noturno.',
    'Qual o período do curso de Sistemas?', 'Noturno.',
    'Qual o período do curso?', 'Noturno.',
    'Qual a titulação do curso de Sistemas de Informação?', 'Bacharel em Sistemas de Informação',
    'Qual a titulação do curso?', 'Bacharel em Sistemas de Informação',
    'Qual o site do curso de Sistemas de Informação?', 'http://sin.inf.ufsc.br/',
    'Qual o site do curso de Sistemas?', 'http://sin.inf.ufsc.br/',
    'Qual o site do curso?', 'http://sin.inf.ufsc.br/',
    'Qual o telefone do curso?', '(48) 3721-7560',
    'Qual o telefone da secretaria do curso?', '(48) 3721-7560',
    'Quem é o coordenador do curso?', 'Prof. Cristian Koliver',
    'Qual o objetivo do curso?', 'O curso tem como objetivo geral formar profissionais empreendedores, capazes de projetar, implementar e gerenciar a infra-estrutura de tecnologia de informação, envolvendo computadores, comunicação e dados em sistemas organizacionais.',
    'Qual o objetivo do curso de sistemas?', 'O curso tem como objetivo geral formar profissionais empreendedores, capazes de projetar, implementar e gerenciar a infra-estrutura de tecnologia de informação, envolvendo computadores, comunicação e dados em sistemas organizacionais.',
]

trainerByList = ListTrainer(mybot)
trainerByList.train(dialogs)

app = Flask(__name__)

@app.route('/')
def nao_entre_em_panico():
    msg = request.args.get('msg')
    if msg:
        answer = mybot.get_response(msg)
        if float(answer.confidence) > 0.50:
            return jsonify({"message": answer.text})
        else:
            return jsonify({"message": "Não tenho nada a dizer sobre isso"})

    return jsonify({"message": "Envie uma mensagem com parâmetro msg="})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
