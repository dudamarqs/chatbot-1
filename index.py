# Importando bibliotecas
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')
nltk.download('stopwords')

# Função para exibir o menu de setores
setores = {
    1: "Suporte Técnico",
    2: "Dúvidas",
    3: "Falar com um Atendente"
}

# Estruturas de perguntas frequentes para cada setor
# Perguntas e Respostas sobre Suporte Técnico usando frozenset
faq_suporte_tecnico = {
    frozenset(["Bug Status cronograma do projeto", "Problema no status cronograma do projeto"]): 
        "Clique no botão 'Atualizar Projeto' que fica no canto superior da tela para que os sinalizadores sejam calculados.",
    frozenset(["Notificação para responsável por contrato não está sendo enviada"]): 
        "Somente as pessoas que possuem permissão para receber relatório de análise de contratos irão receber.",
    frozenset(["Configuração de menu de projetos", "Ao configurar o menu de projetos está alterando o menu de projetos UTD"]): 
        "A configuração do menu do projeto permite a personalização das configurações do projeto, incluindo portfólios de projetos, relatórios de status e indicadores de projeto.",
    frozenset(["Análise sendo apagada ao salvar uma nova"]): 
        "Atualização da versão do sistema.",
    frozenset(["Usuário não consegue logar no sistema"]): 
        "Verificar se o usuário está cadastrado, validar no AD, limpar cookies do browser e tentar novamente.",
    frozenset(["Erro ao cadastrar comentário associado a risco de projeto"]): 
        "Cargas de usuários e unidades consumindo recursos demais geraram a degradação da performance.",
    frozenset(["Usuário recebendo mensagem de notificação indevida"]): 
        "Verificar e ajustar configurações de notificação do sistema.",
    frozenset(["Recurso (pessoa) não aparece no cronograma"]): 
        "Provavelmente, o usuário não está cadastrado como recurso corporativo.",
    frozenset(["No cadastro de usuário, existe o campo 'Unidade de negócio', em qual tabela do banco de dados consigo essa informação?"]): 
        "Segue a consulta SQL para obter tal informação.",
    frozenset(["O portal não mostra a listagem dos riscos excluídos, bem como suas justificativas, como proceder para visualização dos riscos excluídos?"]): 
        "Visualizar através de um relatório extrato diretamente do banco de dados.",
    frozenset(["Erro ao abrir cronograma"]): 
        "Fechar o Tasques, acessar o caminho C:\\Users\\XXXXXXX\\AppData\\Local\\Apps\\2.0 e apagar os arquivos com 'tasq'.",
    frozenset(["Solicitação de script de limpeza demandado pela equipe de Infraestrutura da TI NE"]): 
        "Estabelecer uma política de backup adequada para resolver o crescimento de logs.",
    frozenset(["Erro ao acessar a aba 'Documentos' no Fluxo de Medição"]): 
        "Acessar o menu de modelos de fluxos, procurar o projeto e agendar automaticamente.",
    frozenset(["BUG na Habilitação do Fluxo 'WF Medição Mensal'"]): 
        "Acessar o menu de modelos de fluxos e realizar o agendamento automático.",
    frozenset(["Indicador não aparece"]): 
        "Alterar o ano para 2024.",
    frozenset(["Acesso ao banco de imagens de perfil dos usuários do BRISK"]): 
        "Obter um token de autorização e usar as rotas de API apropriadas.",
    frozenset(["Core Building - relatório dinâmico não está funcionando"]): 
        "Usar o Query Builder para criar ou finalizar a consulta e criar o relatório.",
    frozenset(["Erro ao associar/desassociar fluxos"]): 
        "Clicar no ícone 'editar', acessar 'INTEGRAÇÕES', fechar a tela e associar novamente.",
    frozenset(["Verificar os perfis que têm acesso à funcionalidade 'Adicionar fluxo'"]): 
        "Desmarcar a opção 'Acessar Associação de fluxos' no perfil desejado.",
    frozenset(["Configuração de menus - formulários - fluxos"]): 
        "Os formulários e fluxos dinâmicos só aparecem nos menus dedicados.",
    frozenset(["É necessário habilitar os menus do módulo de projetos no ambiente da Seduc/PI"]): 
        "O menu 'Indicadores de Projetos' foi habilitado com sucesso, compatível com a versão mais nova.",
    frozenset(["Excluir formulários"]): 
        "Não é possível excluir formulários padrões do sistema BRISK.",
    frozenset(["Ao preencher formulários associados aos projetos aparecem caracteres incomuns no Campo Visível Grid"]): 
        "Retirar a apresentação do campo da lista.",
    frozenset(["App.briskppm.com.br na Entidade Cooperação Nacional está retornando uma outra versão de tela inicial ao clicar em filtros"]): 
        "(Resposta completa não fornecida no trecho)."
}

# Perguntas e Respostas sobre Dúvidas do Sistema usando frozenset
faq_duvidas_sistema = {
    frozenset(["Descrever o perfil necessário para contratação do profissional que possa implantar a Governança da ISG"]): 
        "Perfil inclui habilidades em COSO, COBIT, ISO 31000, LGPD, gestão de projetos, certificações como PMP, Cobit 5, CBPP, entre outras.",
    frozenset(["Percebemos a necessidade da parametrização dos relatórios em PDF, foi citado pelo suporte a existência de um módulo para essa função"]): 
        "A parametrização só pode ser feita por técnicos da BRISK, pois requer conhecimentos de programação.",
    frozenset(["Seria possível um e-mail ser enviado ao usuário quando for cadastrado no sistema BRISK?"]): 
        "Sim, o e-mail é enviado automaticamente, mas o texto é padronizado.",
    frozenset(["Na tela de iniciativas no módulo de projetos no BRISK, qual a funcionalidade da coluna 'Unidade Atendimento'?"]): 
        "A coluna indica qual unidade será responsável pela execução do projeto e pode ser configurada em Configurações Gerais."
}

# Perguntas e Respostas sobre Dúvidas dos Serviços usando frozenset
faq_duvidas_servicos = {
    frozenset(["Qual o horário de funcionamento do atendimento da Brisk?"]): 
        "Nosso serviço de atendimento está disponível das 7h às 18h, de segunda a sexta-feira.",
    frozenset(["Quais serviços vocês oferecem?", "Qual o nicho de empresa?", "Com o que vocês trabalham?", "Do que se trata a empresa?"]): 
        "Somos uma empresa que oferece uma plataforma de gerenciamento de projetos e portfólios, com foco em facilitar a criação e monitoramento de planos estratégicos, além de gerenciar investimentos de grande porte. A ferramenta é voltada para empresas que buscam produtividade, integração entre equipes e um acompanhamento eficaz de seus programas e projetos.",
    frozenset(["Como funciona?", "Como é o processo?"]): 
        "Você marca uma reunião com um de nossos atendentes e ele te orienta sobre como vamos tratar da organização do seu projeto.",
    frozenset(["Gostaria de marcar uma reunião", "Quero marcar uma reunião"]): 
        "Ok, vamos te direcionar para um atendente. Aguarde um momento..."
}

# Função para processar a mensagem
def processar_texto(texto):
    stop_words = set(stopwords.words('portuguese'))
    palavras = word_tokenize(texto.lower())  # Tokeniza e converte para minúsculas
    palavras_sem_pontuacao = [palavra for palavra in palavras if palavra not in string.punctuation]
    palavras_limpas = [palavra for palavra in palavras_sem_pontuacao if palavra not in stop_words]
    return palavras_limpas

# Função para encontrar a pergunta mais próxima
def encontrar_faq(pergunta_usuario, faq_setor):
    pergunta_usuario_processada = processar_texto(pergunta_usuario)
    
    melhor_pergunta = None
    maior_correspondencia = 0

    # Percorrer todas as frozensets
    for perguntas, resposta in faq_setor.items():
        for pergunta in perguntas:
            pergunta_processada = processar_texto(pergunta)
            
            # Contar quantas palavras coincidem
            correspondencia = len(set(pergunta_usuario_processada) & set(pergunta_processada))
            
            if correspondencia > maior_correspondencia:
                melhor_pergunta = perguntas  # Aqui será um frozenset com várias perguntas
                maior_correspondencia = correspondencia
    
    # Retornar o conjunto de perguntas correspondente ou None
    return melhor_pergunta


# Função para tratar perguntas sobre o sistema
def tratar_duvidas_sistema():
    print("\nVocê escolheu dúvidas sobre o sistema. Como posso te ajudar?")
    
    while True:
        pergunta_usuario = input("Você: ")
        
        if pergunta_usuario.lower() in ['sair', 'exit', 'quit']:
            print("\nVoltando ao menu principal...")
            break
        
        melhor_pergunta = encontrar_faq(pergunta_usuario, faq_duvidas_sistema)
        
        if melhor_pergunta:
            print(f"{faq_duvidas_sistema[melhor_pergunta]}")
        else:
            print("Desculpe, não sei a resposta para isso. Vou encaminhar para um atendente.")

# Função para tratar perguntas sobre o serviço
def tratar_duvidas_servico():
    print("\nVocê escolheu dúvidas sobre o serviço. Como posso te ajudar?")
    
    while True:
        pergunta_usuario = input("Você: ")
        
        if pergunta_usuario.lower() in ['sair', 'exit', 'quit']:
            print("\nVoltando ao menu principal...")
            break
        
        melhor_pergunta = encontrar_faq(pergunta_usuario, faq_duvidas_servicos)
        
        if melhor_pergunta:
            # Retornar a resposta correta
            print(f"{faq_duvidas_servicos[melhor_pergunta]}")
        else:
            print("Desculpe, não sei a resposta para isso. Vou encaminhar para um atendente.")

# Função para tratar dúvidas gerais
def tratar_duvidas():
    print("\nVocê escolheu dúvidas. Por favor, escolha uma das opções:\n")
    print("1 - Dúvidas sobre o sistema")
    print("2 - Dúvidas sobre o serviço")
    
    while True:
        try:
            opcao = int(input("\nEscolha uma opção: "))
            if opcao == 1:
                tratar_duvidas_sistema()
                break
            elif opcao == 2:
                tratar_duvidas_servico()
                break
            else:
                print("\nOpção inválida. Por favor, escolha 1 ou 2.")
        except ValueError:
            print("\nPor favor, insira um número válido.")

# Função para tratar perguntas no setor de suporte
def tratar_perguntas_suporte():
    print("\nParece que você está com problemas técnicos. Como posso te ajudar?")
    
    while True:
        pergunta_usuario = input("Você: ")
        
        if pergunta_usuario.lower() in ['sair', 'exit', 'quit']:
            print("\nVoltando ao menu principal...")
            break
        
        melhor_pergunta = encontrar_faq(pergunta_usuario, faq_suporte_tecnico)
        
        if melhor_pergunta:
            print(f"{faq_suporte_tecnico[melhor_pergunta]}")
        else:
            print("\nDesculpe, não sei a resposta para isso. Vou encaminhar para um atendente.")

def exibir_menu():
    for numero, setor in setores.items():
        print(f"{numero} - {setor}")

# Função para direcionar o usuário para o setor escolhido
def escolher_setor(opcao):
    if opcao in setores:
        if opcao == 1:
            tratar_perguntas_suporte()
        elif opcao == 2:
            tratar_duvidas()  # Adicionando o tratamento de dúvidas
        elif opcao == 3:
            print("\nConectando você a um atendente...")
    else:
        print("\nOpção inválida. Por favor, escolha um número de 1 a 3.")

# Função principal do chatbot
def chatbot_arvore_decisoes():
    print("\n\nOlá, somos a BRISK PPM! Em que podemos te ajudar?")

    while True:
        exibir_menu()
        try:
            opcao = int(input("\nInsira o número do setor desejado: \n"))
            escolher_setor(opcao)
        except ValueError:
            print("\nPor favor, insira um número válido.")

        continuar = input("\nDeseja escolher outro setor? (Sim/Não)\n").lower()
        if continuar != "sim":
            print("Obrigado por entrar em contato conosco. Até logo!")
            break

# Iniciar o chatbot
chatbot_arvore_decisoes()