import os
import sqlite3
import time
from datetime import datetime
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import TavilySearchTool

# Configurações de layout profissional e amplo
st.set_page_config(
    page_title="Plataforma de Viagens IA - Dashboard", 
    page_icon="✈️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 🎨 INJEÇÃO DE CSS CUSTOMIZADO (UI/UX Premium)
# ==========================================
st.markdown("""
    <style>
        /* Estilização dos Cards do Dashboard */
        .metric-card {
            background-color: #1E293B;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #334155;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #38BDF8;
            margin-bottom: 5px;
        }
        .metric-label {
            font-size: 14px;
            color: #94A3B8;
        }
        /* Ajuste de espaçamento dos títulos */
        .section-title {
            font-size: 20px;
            font-weight: bold;
            color: #F8FAFC;
            margin-top: 15px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🗄️ PERSISTÊNCIA: BANCO DE DADOS (SQLite)
# ==========================================
def init_db():
    conn = sqlite3.connect("travel_platform_pro.db")
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
            hotel_rating TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_trip(destination, days, budget, profile, interests, itinerary, finance, hotel_rating):
    conn = sqlite3.connect("travel_platform_pro.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trips (destination, days, budget, profile, interests, itinerary_text, finance_text, hotel_rating, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (destination, days, budget, profile, interests, itinerary, finance, hotel_rating, datetime.now().strftime("%d/%m/%Y %H:%M")))
    conn.commit()
    conn.close()

def get_stats():
    conn = sqlite3.connect("travel_platform_pro.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), SUM(budget) FROM trips")
    count, total_budget = cursor.fetchone()
    conn.close()
    return count or 0, total_budget or 0.0

def get_all_trips():
    conn = sqlite3.connect("travel_platform_pro.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, destination, days, budget, profile, created_at, itinerary_text, finance_text FROM trips ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

init_db()

# ==========================================
# 📄 GESTÃO DE CHAVES NA SIDEBAR
# ==========================================
with st.sidebar:
    st.title("⚙️ Configurações SaaS")
    st.markdown("Insira suas credenciais operacionais para ativar a malha de agentes.")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Chave gsk_...")
    tavily_api_key = st.text_input("Tavily API Key", type="password", help="Chave tvly_...")
    
    st.divider()
    st.markdown("### 📄 Documentação Clínica")
    st.caption("Desenvolvido por: Sergio Luiz Brito")
    st.caption("Versão do Core: Enterprise v2.4 (CrewAI)")

# ==========================================
# 📊 INTERFACE PRINCIPAL EM ABAS (Multi-Funções)
# ==========================================
tab_dash, tab_new, tab_docs, tab_history = st.tabs([
    "🏠 Dashboard & Visão Geral", 
    "🧳 Criar Nova Viagem", 
    "📄 Gestão de Documentos",
    "📜 Histórico de Viagens"
])

# ------------------------------------------
# 🏠 ABA 1: DASHBOARD & METRICAS DE GASTOS
# ------------------------------------------
with tab_dash:
    st.title("🏠 Dashboard Gerencial de Viagens")
    st.markdown("Monitore suas métricas de alocação de capital e status das jornadas planejadas.")
    
    total_trips, total_spent = get_stats()
    
    # Grid de Indicadores de Performance (KPIs) com CSS Customizado
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{total_trips}</div><div class="metric-label">Viagens Planejadas</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown('<div class="metric-card"><div class="metric-value">0</div><div class="metric-label">Em Andamento</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">US$ {total_spent:,.2f}</div><div class="metric-label">Teto de Gastos Acumulado</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown('<div class="metric-card"><div class="metric-value">Enterprise</div><div class="metric-label">Plano de Conta</div></div>', unsafe_allow_html=True)
        
    st.divider()
    
    # Simulação Visual Gráfica de Orçamento do Dashboard
    st.markdown("### 💰 Proporção Recomendada de Alocação de Gastos (Estimada)")
    mock_data = {
        "Hospedagem (40%)": 40,
        "Passagens/Transporte (30%)": 30,
        "Alimentação (20%)": 20,
        "Passeios/Lazer (10%)": 10
    }
    st.bar_chart(mock_data)

# ------------------------------------------
# 🧳 ABA 2: CRIAR NOVA VIAGEM (Layout Compacto)
# ------------------------------------------
with tab_new:
    st.title("🧳 Nova Viagem com Orquestração de IA")
    st.markdown("Insira os parâmetros para a análise paralela da malha de Agentes Autônomos.")
    st.divider()
    
    os.environ["OPENAI_API_KEY"] = "NA"
    
    # Organização em colunas para maior aproveitamento de tela e visual limpo
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">📍 Destino Alvo</div>', unsafe_allow_html=True)
        city = st.text_input("Cidade ou País", "Paris, França", label_visibility="collapsed")
        
        st.markdown('<div class="section-title">📅 Duração da Estadiana</div>', unsafe_allow_html=True)
        days = st.number_input("Quantidade de Dias", min_value=1, max_value=14, value=3, label_visibility="collapsed")
        
        st.markdown('<div class="section-title">🏨 Categoria de Hospedagem Preferida</div>', unsafe_allow_html=True)
        hotel_rating = st.selectbox("Estrelas / Padrão", ["Hotéis Econômicos / Hostels", "3 Estrelas (Intermediário)", "4 Estrelas (Premium)", "5 Estrelas (Luxo)"], label_visibility="collapsed")

    with col2:
        st.markdown('<div class="section-title">💰 Alocação de Orçamento Máximo (USD)</div>', unsafe_allow_html=True)
        budget = st.number_input("Orçamento em Dólar", min_value=100, max_value=50000, value=1500, step=100, label_visibility="collapsed")
        
        st.markdown('<div class="section-title">👤 Perfil Estratégico da Viagem</div>', unsafe_allow_html=True)
        profile = st.selectbox("Perfil do Viajante", ["Econômico", "Moderado / Familiar", "Luxo / Conforto", "Aventureiro / Mochileiro"], label_visibility="collapsed")
        
        st.markdown('<div class="section-title">❤️ Preferências e Restrições Específicas</div>', unsafe_allow_html=True)
        interests = st.text_area("Interesses e Hobbies", "Museus, culinária típica, deslocamentos curtos a pé.", height=68, label_visibility="collapsed")

    st.divider()
    start_button = st.button("🚀 INICIAR ENGENHARIA DE MULTI-AGENTES", use_container_width=True)
    st.divider()

    status_container = st.empty()

    if start_button:
        if not groq_api_key or not tavily_api_key:
            st.error("❌ Credenciais Ausentes. Digite as chaves de API Groq e Tavily no painel lateral esquerdo.")
        else:
            os.environ["GROQ_API_KEY"] = groq_api_key
            os.environ["TAVILY_API_KEY"] = tavily_api_key

            with status_container.container():
                st.markdown("### 🤖 Orquestração de IA em Progresso")
                s1 = st.markdown("🔄 Agente de Destino: Analisando atrações locais...")
                s2 = st.markdown("⏳ Agente de Hospedagem: Mapeando hotéis padrão " + hotel_rating)
                s3 = st.markdown("⏳ Agente Financeiro: Verificando teto orçamentário...")
                s4 = st.markdown("⏳ Agente Coordenador: Consolidando e validando roteiro final...")
                st.divider()

            try:
                llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api_key)
                search_tool = TavilySearchTool()

                # Mudança de Status do Pipeline
                s1.markdown("✅ Agente de Destino: Concluído.")
                s2.markdown("🔄 Agente de Hospedagem: Buscando opções reais...")
                time.sleep(1)

                # --- CONFIGURAÇÃO DA MALHA DE AGENTES COGNITIVOS ---
                agente_guia = Agent(
                    role=f"Especialista Geográfico de {city}",
                    goal=f"Mapear rotas otimizadas por proximidade física em {city} para {days} dias de estadia.",
                    backstory="Você é um engenheiro de rotas que organiza o dia de passeios eliminando custos desnecessários de táxi e tempo.",
                    llm=llm, tools=[search_tool], allow_delegation=False, verbose=False
                )

                s2.markdown("✅ Agente de Hospedagem: Concluído.")
                s3.markdown("🔄 Agente Financeiro: Processando dados da carteira...")

                agente_financeiro = Agent(
