# Mini-Projeto 9 - Deploy de App com Multi-Agentes de IA Para Planejamento de Viagens com CrewAI, Groq e Tavily

# Importa a biblioteca 'os' para manipulação de variáveis de ambiente
import os

# Importa o Streamlit para construção da interface web
import streamlit as st

# Importa classes essenciais do CrewAI para criar agentes, tarefas, equipes e gerenciar processos
from crewai import Agent, Task, Crew, Process, LLM

# Importa a ferramenta de busca do Tavily que será integrada ao CrewAI
from crewai_tools import TavilySearchTool

# Define configurações gerais da página no Streamlit (título, ícone e layout)
st.set_page_config(page_title = "Agente de IA Viagens LM", page_icon = ":100:", layout = "wide")

# Cria a barra lateral da aplicação
with st.sidebar:

    # Exibe o título da sidebar
    st.title("🤖 Configuração")
    
    # Adiciona uma descrição simples do projeto na sidebar
    st.markdown("Agente de IA Viagens LM")
    
    # Cria campo seguro para o usuário inserir a API Key do Groq
    groq_api_key = st.text_input("Groq API Key", type="password")
    
    # Cria campo seguro para o usuário inserir a API Key do Tavily
    tavily_api_key = st.text_input("Tavily API Key", type="password")
    
    # Exibe um aviso informativo sobre possíveis imprecisões geradas pela IA
    st.sidebar.info("Aviso: IA pode gerar respostas imprecisas, incompletas ou erradas. Sempre verifique informações críticas antes de confiar totalmente no roteiro gerado.")
    
    # Cria uma área expansível para suporte
    with st.sidebar.expander("🆘 Suporte / Fale conosco", expanded = False):
        
        # Exibe o email de suporte dentro do expander
        st.write("Se tiver dúvidas envie mensagem para sergiolmendes2026@gmail.com")
        st.markdown(
    """
    <a href="https://wa.me/55SEUNUMERO" target="_blank" 
       style="background-color: #25d366; color: white; padding: 10px 15px; 
       text-decoration: none; border-radius: 5px; font-weight: bold; 
       display: block; text-align: center; margin-top: 10px; font-size: 15px;">
       <svg viewBox="0 0 24 24" width="20" height="20" fill="white" style="vertical-align: middle; margin-right: 8px;">
           <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.372-.025-.521-.075-.148-.67-1.613-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.955c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
       </svg>
       Falar no WhatsApp
    </a>
    """, 
    unsafe_allow_html=True
)

# Título principal da aplicação
st.title("Agente de IA Viagens LM")

# Subtítulo descrevendo diretamente o propósito da aplicação
st.subheader("✈️ Multi-Agentes de IA Para Planejamento de Viagens")

# Bloco HTML customizado para introduzir a funcionalidade da app
st.markdown(
    "<h3 style='font-size:22px; color:red;'>Forneça os detalhes da sua viagem e uma equipe de Agentes de IA criará seu roteiro.</h3>",
    unsafe_allow_html=True
)

# Insere um divisor visual na interface
st.divider()

# Salva a API Key do Tavily nas variáveis de ambiente (caso esteja vazia, tenta resgatar do sistema)
os.environ["TAVILY_API_KEY"] = tavily_api_key or os.environ.get("TAVILY_API_KEY", "")

# Define variável do OpenAI como vazia para evitar fallback automático quando não utilizado
os.environ["OPENAI_API_KEY"] = ""

# Cria duas colunas para organizar os inputs
col1, col2 = st.columns(2)

# Primeira coluna com campos da cidade e número de dias
with col1:

    # Campo para o usuário informar a cidade da viagem
    city = st.text_input("Para qual cidade/país você quer ir?", "Paris, França")
    
    # Campo numérico para selecionar a quantidade de dias (1 a 14)
    days = st.number_input("Quantos dias?", min_value = 1, max_value = 14, value = 3)

# Segunda coluna com campo para interesses do viajante
with col2:

    # Campo de texto para o usuário listar seus interesses principais
    interests = st.text_area("Quais são seus interesses principais?", "Museus, gastronomia e natureza.")

# Cria 2 colunas
col_btn, col_box = st.columns([2, 1])

# Botão para disparar a geração do roteiro
with col_btn:
    start_button = st.button("Gerar Roteiro 🚀")

# Caixa de texto (label)
with col_box:
    st.markdown(
        "<div style='border:1px solid #ccc; padding:6px 10px; border-radius:6px; text-align:center;'>Sergio Luiz Brito</div>",
        unsafe_allow_html=True
    )

# Se o botão for pressionado, inicia as validações e execução dos agentes
if start_button:

    # Valida se a API Key do Groq foi informada
    if not groq_api_key:

        # Exibe erro caso esteja vazia
        st.error("Por favor, insira sua Groq API Key na barra lateral.")
    
    # Valida se a API Key do Tavily foi informada
    elif not tavily_api_key:
        
        # Exibe erro caso esteja vazia
        st.error("Por favor, insira sua Tavily API Key na barra lateral.")
    
    # Valida se a cidade foi preenchida
    elif not city:

        # Exibe erro caso esteja vazia
        st.error("Por favor, insira uma cidade.")
    
    else:
        
        # Salva a API do Groq nas variáveis de ambiente
        os.environ["GROQ_API_KEY"] = groq_api_key
        
        # Salva a API do Tavily nas variáveis de ambiente
        os.environ["TAVILY_API_KEY"] = tavily_api_key
        
        # Garante que a variável do OpenAI continue definida mesmo sem uso
        os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")

        # Inicia um bloco try para capturar possíveis falhas durante o processamento
        try:

            # Mostra um spinner enquanto a IA trabalha na criação do roteiro
            with st.spinner("Os Agentes de IA estão pesquisando e planejando sua viagem..."):
                
                # Instancia o modelo LLM usando o provedor Groq
                llm = LLM(model = "groq/llama-3.3-70b-versatile", api_key = groq_api_key)
                
                # Inicializa a ferramenta de busca do Tavily
                search_tool = TavilySearchTool()

                # Cria o agente especialista local, responsável por pesquisar atrações
                dsa_agente_guia_viagem = Agent(
                    
                    # Define a função do agente com base na cidade escolhida
                    role = f"Especialista Local de {city}",
                    
                    # Estabelece o objetivo do agente considerando dias e interesses
                    goal = f"Fornecer as melhores sugestões de locais para uma viagem de {days} dias em {city}, com foco em {interests}.",
                    
                    # Define a personalidade e contexto do agente
                    backstory = f"Você é um guia turístico local de {city}, apaixonado por compartilhar os segredos da sua cidade.",
                    
                    # Associa o LLM ao agente
                    llm = llm,
                    
                    # Associa a ferramenta de busca do Tavily
                    tools = [search_tool],
                    
                    # Impede que o agente delegue tarefas
                    allow_delegation = False,
                    
                    # Desativa logs detalhados
                    verbose = False
                )

                # Cria o agente planejador, responsável por organizar o roteiro
                dsa_agente_planejador = Agent(
                    
                    # Define a função do agente
                    role = "Planejador Logístico de Viagem",
                    
                    # Determina seu objetivo principal
                    goal = f"Organizar as sugestões em um roteiro lógico e eficiente para {days} dias.",
                    
                    # Explica seu perfil e especialização
                    backstory = "Você é um especialista em logística que agrupa atividades por proximidade e horários.",
                    
                    # Associa o LLM ao agente
                    llm = llm,
                    
                    # Impede delegação de tarefas
                    allow_delegation = False,
                    
                    # Desativa logs extensos
                    verbose = False
                )

                # Cria o agente final que escreve o roteiro pronto em Markdown
                dsa_agente_gerador_roteiro = Agent(
                    
                    # Define o papel do agente
                    role = "Revisor e Escritor de Roteiros",
                    
                    # Define o objetivo de gerar um roteiro final formatado
                    goal = "Transformar o esboço em um itinerário diário detalhado e agradável em Markdown.",
                    
                    # Define o contexto do agente
                    backstory = "Você é um concierge de hotel 5 estrelas.",
                    
                    # Associa o LLM ao agente
                    llm = llm,
                    
                    # Impede delegação
                    allow_delegation = False,
                    
                    # Desabilita logs em console
                    verbose = False
                )

                # Cria a primeira tarefa: pesquisa de locais e experiências
                tarefa_pesquisa = Task(
                    
                    # Descreve o objetivo da tarefa
                    description = (f"Use a ferramenta de busca para achar atrações, restaurantes e experiências para {days} dias em {city} "
                                   f"com base em: {interests}. Explique brevemente o motivo de cada sugestão e inclua a fonte/URL."),
                    
                    # Determina o formato esperado de entrega
                    expected_output = "Lista com pelo menos 10 sugestões, cada uma com 1 motivo e 1 URL.",
                    
                    # Define qual agente executará a tarefa
                    agent = dsa_agente_guia_viagem
                )

                # Cria a tarefa de planejamento e agrupamento
                tarefa_planejamento = Task(
                    
                    # Informa o que deve ser feito
                    description = f"Agrupe as sugestões por localização e crie um esboço dia a dia para {days} dias.",
                    
                    # Define o formato esperado do retorno
                    expected_output = f"Plano estruturado por dia, com blocos por região e janelas de horário.",
                    
                    # Associa ao agente planejador
                    agent = dsa_agente_planejador,
                    
                    # Define dependência da tarefa anterior (contexto)
                    context = [tarefa_pesquisa]
                )

                # Cria a tarefa final de escrita do roteiro
                tarefa_roteiro = Task(
                    
                    # Descreve a ação desejada
                    description = "Escreva o roteiro final em Markdown, com seções por dia e dicas práticas.",
                    
                    # Define o output esperado
                    expected_output = "Roteiro completo em Markdown, pronto para copiar.",
                    
                    # Associa ao agente escritor
                    agent = dsa_agente_gerador_roteiro,
                    
                    # Determina dependência do planejamento
                    context = [tarefa_planejamento]
                )

                # Cria a equipe (Crew) que executará as tarefas de forma sequencial
                dsa_equipe_agentes_ia = Crew(
                    
                    # Lista de agentes envolvidos
                    agents = [dsa_agente_guia_viagem, dsa_agente_planejador, dsa_agente_gerador_roteiro],
                    
                    # Lista de tarefas a serem cumpridas
                    tasks = [tarefa_pesquisa, tarefa_planejamento, tarefa_roteiro],
                    
                    # Define execução sequencial
                    process = Process.sequential,
                    
                    # Desabilita logs detalhados da execução
                    verbose = 0
                )

                # Dispara a execução do fluxo completo
                result = dsa_equipe_agentes_ia.kickoff()
                
                # Exibe mensagem de sucesso ao usuário
                
                st.success("Seu roteiro de viagem personalizado está pronto!")
                
                # Renderiza o roteiro em Markdown na interface
                st.markdown(result)

        # Captura qualquer erro e exibe na interface
        except Exception as e:

          
            # Mostra mensagem genérica de erro com detalhes
            st.error(f"Ocorreu um erro ao gerar o roteiro: {e}")
            
            # Orienta validações básicas de causa provável
            st.error("Confirme as chaves de API e a versão dos pacotes.")

# Bloco único para salvar o roteiro e ativar o chat interativo
if "roteiro_gerado" in st.session_state:
    st.divider()
    st.markdown("### 💬 Chat com Agente de IA para Dúvidas sobre o Roteiro")
    st.info("O agente de IA leu seu roteiro e está pronto para responder perguntas específicas sobre ele!")

    # Inicializa o histórico de mensagens
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe as mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de chat na parte inferior
    if prompt := st.chat_input("Digite sua mensagem para o agente..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Resposta inteligente do Agente baseada no roteiro gerado
        with st.chat_message("assistant"):
            with st.spinner("O assistente está analisando sua dúvida..."):
                try:
                    chat_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api_key)
                    
                    chat_agent = Agent(
                        role="Assistente de Viagem Inteligente",
                        goal=f"Responder dúvidas do usuário com base exclusiva no roteiro gerado.",
                        backstory="Você é um assistente prestativo especialista em viagens.",
                        llm=chat_llm,
                        verbose=False
                    )
                    
                    chat_task = Task(
                        description=f"Roteiro da viagem:\n{st.session_state['roteiro_gerado']}\n\nDúvida do usuário: {prompt}",
                        expected_output="Resposta clara e útil em Markdown.",
                        agent=chat_agent
                    )
                    
                    chat_crew = Crew(
                        agents=[chat_agent],
                        tasks=[chat_task],
                        process=Process.sequential,
                        verbose=0
                    )
                    
                    ai_response = chat_crew.kickoff()
                    st.markdown(ai_response)
                    
                    st.session_state.messages.append({"role": "assistant", "content": str(ai_response)})
                
                except Exception as chat_error:
                    error_message = f"Não foi possível gerar a resposta: {chat_error}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})








