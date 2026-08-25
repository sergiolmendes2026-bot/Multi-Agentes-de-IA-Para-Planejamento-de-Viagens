import os
import sqlite3
import time
from datetime import datetime
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import TavilySearchTool

# Configurações de layout do Streamlit
st.set_page_config(page_title="Agente de IA Viagens LM", page_icon="✈️", layout="centered")

# ==========================================
# 🗄️ BANCO DE DADOS LOCAL (SQLite)
# ==========================================
def init_db():
    conn = sqlite3.connect("travel_platform.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            days INTEGER NOT NULL,
            budget REAL NOT NULL,
            profile TEXT NOT NULL,
            interests TEXT,
            itinerary_text TEXT,
            finance_text TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_trip(destination, days, budget, profile, interests, itinerary, finance):
    conn = sqlite3.connect("travel_platform.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trips (destination, days, budget, profile, interests, itinerary_text, finance_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (destination, days, budget, profile, interests, itinerary, finance, datetime.now().strftime("%d/%m/%Y %H:%M")))
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 📄 BARRA LATERAL (Configurações Ocultas)
# ==========================================
with st.sidebar:
    st.title("🤖 API Keys")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Chave gsk_...")
    tavily_api_key = st.text_input("Tavily API Key", type="password", help="Chave tvly_...")
    st.caption("SaaS por: Sergio Luiz Brito")

# ==========================================
# ✈️ INTERFACE PRINCIPAL (Fiel ao seu Rascunho)
# ==========================================
st.title("✈️ Criar Novo Planejamento de Viagem")
st.markdown("Planeje sua viagem com o auxílio de múltiplos agentes de IA.")

st.divider()

# Inputs verticais organizados exatamente como solicitado
st.markdown("### 📍 DESTINO")
city = st.text_input("Destino", "Paris, França", label_visibility="collapsed")

st.markdown("### 💰 ORÇAMENTO")
budget = st.number_input("Orçamento Máximo (USD)", min_value=100, max_value=50000, value=1500, step=100, label_visibility="collapsed")

st.markdown("### 📅 DURAÇÃO")
days = st.number_input("Dias", min_value=1, max_value=14, value=3, label_visibility="collapsed")
st.markdown(f"**{days}** dias")

st.markdown("### 👤 PERFIL DA VIAGEM")
profile = st.selectbox("Perfil", ["Econômico", "Moderado / Familiar", "Luxo / Conforto", "Aventureiro / Mochileiro"], label_visibility="collapsed")

st.markdown("### ❤️ PREFERÊNCIAS")
interests = st.text_area("Preferências", "Museus, culinária típica, deslocamentos curtos a pé.", label_visibility="collapsed")

st.divider()

# Botão centralizado de execução
start_button = st.button("🚀 GERAR PLANEJAMENTO", use_container_width=True)

st.divider()

# Container vazio para gerenciar as atualizações de status das IAs trabalhando
status_container = st.empty()

# Execução do processamento de múltiplos agentes
if start_button:
    if not groq_api_key or not tavily_api_key:
        st.error("❌ Por favor, preencha as chaves Groq e Tavily na barra lateral antes de começar.")
    else:
        os.environ["GROQ_API_KEY"] = groq_api_key
        os.environ["TAVILY_API_KEY"] = tavily_api_key
        os.environ["OPENAI_API_KEY"] = "NA"

        # 1. Tela mostrando a IA trabalhando em tempo real (Estilo o seu rascunho)
        with status_container.container():
            st.markdown("### 🤖 IA trabalhando no seu planejamento")
            status_1 = st.markdown("🔄 Análise do destino")
            status_2 = st.markdown("⏳ Análise do orçamento")
            status_3 = st.markdown("⏳ Construção do roteiro")
            status_4 = st.markdown("⏳ Recomendações")
            status_5 = st.markdown("⏳ Revisão final")
            st.divider()

        try:
            # Configuração inicial do CrewAI
            llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api_key)
            search_tool = TavilySearchTool()

            # Atualiza status visual 1
            status_1.markdown("✅ Análise do destino")
            status_2.markdown("🔄 Análise do orçamento")
            time.sleep(1)

            # --- DEFINIÇÃO DOS AGENTES (Modelados com base na sua arquitetura) ---
            agente_guia = Agent(
                role=f"Especialista Geográfico de {city}",
                goal=f"Mapear atrações otimizadas em {city} para {days} dias.",
                backstory="Você analisa a geografia do local garantindo rotas curtas e inteligentes.",
                llm=llm, tools=[search_tool], allow_delegation=False, verbose=False
            )

            agente_financeiro = Agent(
                role="Auditor de Custos",
                goal=f"Garantir viabilidade frente ao orçamento de USD {budget}.",
                backstory="Você calcula os custos reais de alimentação, transporte e ingressos de forma rigorosa.",
                llm=llm, tools=[search_tool], allow_delegation=False, verbose=False
            )

            # Atualiza status visual 2
            status_2.markdown("✅ Análise do orçamento")
            status_3.markdown("🔄 Construção do roteiro")

            # --- DEFINIÇÃO DAS TAREFAS ---
            tarefa_roteiro = Task(
                description=f"Crie um roteiro dia a dia para {days} dias em {city}. Perfil: {profile}. Interesses: {interests}.",
                expected_output="Roteiro sequencial estruturado por blocos diários.",
                agent=agente_guia
            )

            tarefa_financeira = Task(
                description=f"Valide financeiramente o roteiro gerado comparando com o teto de USD {budget}.",
                expected_output="Análise de custos e veredito final.",
                agent=agente_financeiro
            )

            # Execução em Equipe
            equipe = Crew(
                agents=[agente_guia, agente_financeiro],
                tasks=[tarefa_roteiro, tarefa_financeira],
                process=Process.sequential,
                verbose=False
            )

            # Atualiza status visual 3 e 4
            status_3.markdown("✅ Construção do roteiro")
            status_4.markdown("✅ Recomendações")
            status_5.markdown("🔄 Revisão final")

            # Kickoff da IA
            resultado = equipe.kickoff()
            
            # Limpa os indicadores de carregamento após a conclusão
            status_5.markdown("✅ Revisão final")
            time.sleep(1)
            status_container.empty()

            # Salva o resultado no banco
            res_itinerary = tarefa_roteiro.output.raw
            res_finance = tarefa_financeira.output.raw
            save_trip(city, days, budget, profile, interests, res_itinerary, res_finance)

            # 2. SEU PLANEJAMENTO (Exibição idêntica ao seu desenho)
            st.markdown("## 🗺️ SEU PLANEJAMENTO")
            st.markdown(f"### 🇫🇷 {city} — {days} dias")
            st.markdown(f"**💰 Orçamento estimado:** US$ {budget:,.2f}")
            st.markdown(f"**👤 Perfil:** {profile}")
            
            st.divider()
            
            st.markdown("#### 📅 Roteiro Diário")
            st.markdown(res_itinerary)
            
            st.divider()
            st.markdown("#### 📊 Análise Financeira e Validação")
            st.markdown(res_finance)

        except Exception as e:
            status_container.empty()
            st.error(f"❌ Ocorreu um erro no processamento: {str(e)}")
