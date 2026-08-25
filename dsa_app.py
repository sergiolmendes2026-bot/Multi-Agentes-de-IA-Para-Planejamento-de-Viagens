import os
import sqlite3
from datetime import datetime
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import TavilySearchTool

# Configurações de layout do Streamlit
st.set_page_config(page_title="Agente de IA Viagens LM", page_icon="✈️", layout="wide")

# ==========================================
# 🗄️ PERSISTÊNCIA: CONFIGURAÇÃO DO SQLITE
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

def get_all_trips():
    conn = sqlite3.connect("travel_platform.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, destination, days, budget, profile, created_at, itinerary_text, finance_text FROM trips ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Inicializa o banco de dados local
init_db()

# ==========================================
# 📄 GERADOR DE ARQUIVO: EXPORTAÇÃO PDF
# ==========================================
def generate_travel_pdf(destination, days, profile, budget, itinerary_text, finance_text):
    """
    Gera um relatório PDF elegante em conformidade com as regras corporativas,
    salvando-o temporariamente e retornando os bytes binários para o Streamlit.
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    
    pdf_filename = "temp_roteiro_viagem.pdf"
    doc = SimpleDocTemplate(
        pdf_filename, 
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40,
        title=f"Roteiro de Viagem - {destination}"
    )
    
    styles = getSampleStyleSheet()
    
    # Definição da paleta de cores corporativa (Cool Tech / Dark Navy)
    PRIMARY_COLOR = colors.HexColor("#1A365D")   # Azul Escuro Naval
    SECONDARY_COLOR = colors.HexColor("#2B6CB0") # Azul Corporativo Médio
    TEXT_COLOR = colors.HexColor("#2D3748")      # Cinza Escuro Antracite
    BG_LIGHT = colors.HexColor("#F7FAFC")        # Fundo Off-White
    
    # Customização de Tipografia Estrita
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=PRIMARY_COLOR,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY_COLOR,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=TEXT_COLOR,
        spaceAfter=8
    )
    
    meta_label_style = ParagraphStyle(
        'MetaLabel',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white
    )
    
    meta_val_style = ParagraphStyle(
        'MetaValue',
        fontName='Helvetica',
        fontSize=10,
        leading=12,
        textColor=colors.white
    )

    story = []
    
    # Cabeçalho Principal do Documento
    story.append(Paragraph(f"Plano de Viagem: {destination}", title_style))
    story.append(Paragraph(f"Gerado de forma inteligente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}", body_style))
    story.append(Spacer(1, 15))
    
    # Tabela Executiva de Metadados da Viagem
    meta_data = [
        [Paragraph("Destino:", meta_label_style), Paragraph(destination, meta_val_style), 
         Paragraph("Duração:", meta_label_style), Paragraph(f"{days} dias", meta_val_style)],
        [Paragraph("Perfil:", meta_label_style), Paragraph(profile, meta_val_style), 
         Paragraph("Orçamento:", meta_label_style), Paragraph(f"USD {budget:,.2f}", meta_val_style)]
    ]
    meta_table = Table(meta_data, colWidths=[80, 185, 80, 185])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY_COLOR),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('CORNER_RADIUS', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))
    
    # Seção 1: O Roteiro Estruturado (Processamento de quebras de linha nativas)
    story.append(Paragraph("🗺️ Cronograma Diário Sugerido", h1_style))
    for paragraph_text in itinerary_text.split('\n'):
        clean_text = paragraph_text.strip()
        if clean_text:
            # Detecta subtópicos ou dias para aplicar destaques leves
            if clean_text.startswith("Dia") or clean_text.startswith("###"):
                story.append(Spacer(1, 5))
                story.append(Paragraph(f"<b>{clean_text.replace('###', '').strip()}</b>", ParagraphStyle('DayH', parent=body_style, textColor=SECONDARY_COLOR, fontName='Helvetica-Bold', fontSize=12)))
            else:
                story.append(Paragraph(clean_text, body_style))
                
    story.append(PageBreak()) # Força quebra de página profissional para o relatório financeiro
    
    # Seção 2: Análise Econômica e Viabilidade
    story.append(Paragraph("💰 Resumo Orçamentário Estruturado", h1_style))
    for paragraph_text in finance_text.split('\n'):
        clean_text = paragraph_text.strip()
        if clean_text:
            story.append(Paragraph(clean_text, body_style))
            
    # Rodapé Clínico/Aviso Legal Exigido por IA
    story.append(Spacer(1, 30))
    disclaimer_style = ParagraphStyle('Disclaimer', parent=body_style, fontName='Helvetica-Oblique', fontSize=8.5, textColor=colors.HexColor("#718096"))
    story.append(Paragraph("Este documento é um planejamento preliminar gerado por IA. Verifique taxas locais, disponibilidade de passagens, exigências de passaporte ou vistos antes de realizar pagamentos.", disclaimer_style))
    
    # Compila o documento final
    doc.build(story)
    
    # Lê os bytes gerados e remove o arquivo temporário
    with open(pdf_filename, "rb") as f:
        pdf_bytes = f.read()
    os.remove(pdf_filename)
    
    return pdf_bytes

# ==========================================
# ⚙️ INTERFACE GRÁFICA (STREAMLIT)
# ==========================================
with st.sidebar:
    st.title("🤖 Configuração do Sistema")
    st.markdown("**Plataforma Operacional de Viagens com Multi-Agentes**")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Chave gsk_...")
    tavily_api_key = st.text_input("Tavily API Key", type="password", help="Chave tvly_...")
    
    st.divider()
    st.info("💡 **Dica:** Os roteiros criados com sucesso ficarão listados automaticamente na aba lateral de histórico do dashboard principal.")

# Layout estrutural por Abas Globais do App
tab_home, tab_history = st.tabs(["🧳 Nova Viagem & Dashboard", "📄 Viagens Anteriores (Histórico)"])

# ------------------------------------------
# ABA 1: OPERAÇÃO PRINCIPAL / NOVA VIAGEM
# ------------------------------------------
with tab_home:
    st.title("✈️ Criar Novo Planejamento de Viagem")
    st.markdown("<h3 style='font-size:17px; color:#4F46E5;'>Preencha os dados e execute a malha de agentes cognitivos.</h3>", unsafe_allow_html=True)
    st.divider()

    os.environ["OPENAI_API_KEY"] = "NA" # Proteção contra chamadas não intencionais

    # Grid de Parâmetros
    col1, col2, col3 = st.columns(3)
    with col1:
        city = st.text_input("📍 Qual é o destino de interesse?", "Paris, França")
        days = st.number_input("📅 Janela temporal de permanência (Dias)", min_value=1, max_value=14, value=3)
    with col2:
        budget = st.number_input("💰 Teto do Orçamento de Alocação (USD)", min_value=100, max_value=100000, value=1500, step=100)
        profile = st.selectbox("🧳 Matriz de Perfil Executivo", ["Econômico", "Moderado / Familiar", "Luxo / Conforto", "Aventureiro / Mochileiro"])
    with col3:
        interests = st.text_area("🎯 Restrições de Interesse / Desejos Específicos", "Museus, culinária típica, deslocamentos curtos a pé.")

    col_btn, col_box = st.columns([3, 1])
    with col_btn:
        start_button = st.button("Acionar Engenharia de Agentes Sequenciais 🚀", use_container_width=True)
    with col_box:
        st.markdown("<div style='border:1px solid #ccc; padding:8px 10px; border-radius:6px; text-align:center; font-weight:bold; background-color:#F8FAFC;'>Créditos: Sergio Luiz Brito</div>", unsafe_allow_html=True)

    if start_button:
        if not groq_api_key or not tavily_api_key:
            st.error("❌ Credenciais Ausentes. Insira as chaves de API Groq e Tavily no painel lateral de configurações.")
