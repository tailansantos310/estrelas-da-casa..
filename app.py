import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Estrelas da Casa", page_icon="⭐", layout="wide", initial_sidebar_state="expanded")

# --- ESTADOS DA SESSÃO (SESSION STATE) ---
if "jogadores" not in st.session_state:
    st.session_state.jogadores = {
        "TAILAN": {"estrelas": 25, "escudos": 0, "fantasmas": 0, "chefes": 0, "coringas": 0},
        "CAROL": {"estrelas": 25, "escudos": 0, "fantasmas": 0, "chefes": 0, "coringas": 0},
        "KARINE": {"estrelas": 25, "escudos": 0, "fantasmas": 0, "chefes": 0, "coringas": 0},
        "CAIO": {"estrelas": 25, "escudos": 0, "fantasmas": 0, "chefes": 0, "coringas": 0}
    }

if "tarefas_concluidas_hoje" not in st.session_state:
    st.session_state.tarefas_concluidas_hoje = []
if "tarefas_fantasmas_hoje" not in st.session_state:
    st.session_state.tarefas_fantasmas_hoje = []
if "tarefas_chefes_hoje" not in st.session_state:
    st.session_state.tarefas_chefes_hoje = {}
if "punicoes_fim_de_semana" not in st.session_state:
    st.session_state.punicoes_fim_de_semana = []

# Controle do Dado Diário por Jogador
if "dado_jogado_hoje" not in st.session_state:
    st.session_state.dado_jogado_hoje = {j: False for j in st.session_state.jogadores.keys()}
if "resultado_dado" not in st.session_state:
    st.session_state.resultado_dado = None

# --- ESCALAS DE TAREFAS ---
escala_semana1 = {
    "Café manhã": {"QUA": "KARINE", "QUI": "CAIO", "SEX": "TAILAN", "SÁB": "CAROL", "DOM": "KARINE", "SEG": "CAIO", "TER": "TAILAN"},
    "Café tarde": {"QUA": "CAIO", "QUI": "CAROL", "SEX": "KARINE", "SÁB": "CAIO", "DOM": "TAILAN", "SEG": "CAROL", "TER": "KARINE"},
    "Varrer manhã": {"QUA": "KARINE", "QUI": "CAROL", "SEX": "KARINE", "SÁB": "CAIO", "DOM": "TAILAN", "SEG": "CAROL", "TER": "KARINE"},
    "Varrer tarde": {"QUA": "CAROL", "QUI": "CAIO", "SEX": "TAILAN", "SÁB": "CAROL", "DOM": "KARINE", "SEG": "CAIO", "TER": "TAILAN"},
    "Almoço": {"QUA": "CAROL", "QUI": "KARINE", "SEX": "CAROL", "SÁB": "KARINE", "DOM": "CAIO", "SEG": "CAROL", "TER": "KARINE"},
    "Janta": {"QUA": "TAILAN", "QUI": "CAROL", "SEX": "KARINE", "SÁB": "CAIO", "DOM": "TAILAN", "SEG": "CAROL", "TER": "KARINE"},
    "Fogão almoço": {"QUA": "CAROL", "QUI": "KARINE", "SEX": "CAIO", "SÁB": "TAILAN", "DOM": "CAROL", "SEG": "KARINE", "TER": "CAIO"},
    "Fogão janta": {"QUA": "KARINE", "QUI": "CAIO", "SEX": "TAILAN", "SÁB": "CAROL", "DOM": "KARINE", "SEG": "CAIO", "TER": "TAILAN"},
    "Banheiro": {"QUA": "KARINE", "QUI": "CAIO", "SEX": "TAILAN", "SÁB": "CAROL", "DOM": "KARINE", "SEG": "CAIO", "TER": "TAILAN"},
    "Garrafas": {"QUA": "CAIO", "QUI": "TAILAN", "SEX": "CAROL", "SÁB": "KARINE", "DOM": "CAIO", "SEG": "TAILAN", "TER": "CAROL"},
    "Roupa": {"QUA": "TAILAN", "QUI": "CAROL", "SEX": "KARINE", "SÁB": "CAIO", "DOM": "TAILAN", "SEG": "CAROL", "TER": "KARINE"},
    "Organizar": {"QUA": "CAROL", "QUI": "KARINE", "SEX": "CAIO", "SÁB": "TAILAN", "DOM": "CAROL", "SEG": "KARINE", "TER": "CAIO"},
    "Passar pano": {"QUA": "CAROL", "QUI": "-", "SEX": "KARINE", "SÁB": "-", "DOM": "CAIO", "SEG": "-", "TER": "TAILAN"}
}

escala_semana2 = {
    "Café manhã": {"QUA": "CAROL", "QUI": "KARINE", "SEX": "CAIO", "SÁB": "TAILAN", "DOM": "CAROL", "SEG": "KARINE", "TER": "CAIO"},
    "Café tarde": {"QUA": "CAIO", "QUI": "CAROL", "SEX": "KARINE", "SÁB": "CAIO", "DOM": "TAILAN", "SEG": "CAROL", "TER": "KARINE"},
    "Varrer manhã": {"QUA": "CAROL", "QUI": "KARINE", "SEX": "CAROL", "SÁB": "KARINE", "DOM": "CAIO", "SEG": "CAROL", "TER": "KARINE"},
    "Varrer tarde": {"QUA": "CAROL", "QUI": "CAIO", "SEX": "TAILAN", "SÁB": "CAROL", "DOM": "KARINE", "SEG": "CAIO", "TER": "TAILAN"},
    "Almoço": {"QUA": "CAROL", "QUI": "KARINE", "SEX": "CAROL", "SÁB": "KARINE", "DOM": "CAIO", "SEG": "CAROL", "TER": "KARINE"},
    "Janta": {"QUA": "CAIO", "QUI": "TAILAN", "SEX": "CAROL", "SÁB": "KARINE", "DOM": "CAIO", "SEG": "TAILAN", "TER": "CAROL"},
    "Fogão almoço": {"QUA": "CAROL", "QUI": "KARINE", "SEX": "CAIO", "SÁB": "TAILAN", "DOM": "CAROL", "SEG": "KARINE", "TER": "CAIO"},
    "Fogão janta": {"QUA": "CAROL", "QUI": "KARINE", "SEX": "CAIO", "SÁB": "TAILAN", "DOM": "CAROL", "SEG": "KARINE", "TER": "CAIO"},
    "Banheiro": {"QUA": "CAROL", "QUI": "KARINE", "SEX": "CAIO", "SÁB": "TAILAN", "DOM": "CAROL", "SEG": "KARINE", "TER": "CAIO"},
    "Garrafas": {"QUA": "KARINE", "QUI": "CAIO", "SEX": "TAILAN", "SÁB": "CAROL", "DOM": "KARINE", "SEG": "CAIO", "TER": "TAILAN"},
    "Roupa": {"QUA": "CAIO", "QUI": "TAILAN", "SEX": "CAROL", "SÁB": "KARINE", "DOM": "CAIO", "SEG": "TAILAN", "TER": "CAROL"},
    "Organizar": {"QUA": "TAILAN", "QUI": "CAROL", "SEX": "KARINE", "SÁB": "CAIO", "DOM": "TAILAN", "SEG": "CAROL", "TER": "CAIO"},
    "Passar pano": {"QUA": "-", "QUI": "CAROL", "SEX": "-", "SÁB": "KARINE", "DOM": "-", "SEG": "CAIO", "TER": "-"}
}

st.title("⭐ ESTRELAS DA CASA - CADA UM POR SI ⭐")

with st.expander("📜 CLIQUE AQUI PARA VER AS REGRAS OFICIAIS DO JOGO", expanded=False):
    st.markdown("""
    * **Cartões:** 1 card = 1 tarefa só. | **Dado é todo dia.**
    * **⚠️ PUNIÇÃO SEMANAL:** Quem deixar de fazer uma tarefa perderá uma estrela (**-1 ⭐**) e fará a tarefa do próximo participante no fim de semana!
    * **🎲 EFEITOS DO DADO DIÁRIO:**
        * **Face 1:** Perde 1 estrela automaticamente.
        * **Face 2:** Nada acontece. Aguarde o próximo dia.
        * **Face 3:** +1 Estrela & Ganha 🛡️ ESCUDO (Evita perda de estrela se falhar em uma tarefa).
        * **Face 4:** Ganha 👻 FANTASMA (Oculta e cancela uma tarefa sua no dia).
        * **Face 5:** Ganha 👑 CHEFE (Delega uma tarefa sua para outro participante fazer).
        * **Face 6:** Ganha 🃏 CORINGA (Você escolhe se quer usar o Escudo, Fantasma ou Chefe).
    * **Metas de Evolução:** 35 ⭐ = 👻 FANTASMA | 45 ⭐ = 🛡️ ESCUDO | 55 ⭐ = 👑 CHEFE | 65 ⭐ = 🃏 CORINGA
    * **Fim de ano:** Quem tiver mais estrelas ganha **R$ 150**.
    """)

st.write("---")

st.sidebar.header("👤 Quem está mexendo?")
lista_jogadores = ["TAILAN", "CAROL", "KARINE", "CAIO"]
jogador_atual = st.sidebar.selectbox("Escolha seu nome:", lista_jogadores)

if st.sidebar.button("🔄 Virar o Dia / Reset Diário"):
    st.session_state.tarefas_concluidas_hoje = []
    st.session_state.tarefas_fantasmas_hoje = []
    st.session_state.tarefas_chefes_hoje = {}
    st.session_state.dado_jogado_hoje = {j: False for j in st.session_state.jogadores.keys()}
    st.session_state.resultado_dado = None
    st.sidebar.success("Dia virado com sucesso!")
    st.rerun()

aba_escala, aba_ranking, aba_dados = st.tabs(["📅 Marcar Tarefas", "🏆 Ranking Geral", "🎲 Dado & Cartas"])

# --- ABA 1: TAREFAS & PUNIÇÕES ---
with aba_escala:
    st.header("📅 Escala de Tarefas do Dia")
    col1, col2 = st.columns(2)
    with col1: semana_sel = st.radio("Selecione a Semana:", ["Semana 1", "Semana 2"], horizontal=True)
    with col2: dia_sel = st.selectbox("Selecione o Dia:", ["QUA", "QUI", "SEX", "SÁB", "DOM", "SEG", "TER"])
    
    escala_ativa = escala_semana1 if semana_sel == "Semana 1" else escala_semana2
    
    st.subheader(f"📋 Obrigações de {jogador_atual}")
    alguma_tarefa = False
    
    # Gerenciamento de tarefas normais/chefes/fantasmas
    for tarefa, dias in escala_ativa.items():
        responsavel_original = dias[dia_sel]
        if responsavel_original == "-":
            continue
            
        chave_busca = f"{semana_sel}_{dia_sel}_{tarefa}"
        responsavel_atual = st.session_state.tarefas_chefes_hoje.get(chave_busca, responsavel_original)
        
        if responsavel_atual == jogador_atual:
            alguma_tarefa = True
            chave_tarefa = f"{semana_sel}_{dia_sel}_{tarefa}_{jogador_atual}"
            
            if chave_busca in st.session_state.tarefas_fantasmas_hoje:
                st.markdown(f"### 👻 ~~{tarefa}~~ (Sumiu com carta Fantasma!)")
            else:
                col_txt, col_btn = st.columns([3, 1])
                with col_txt:
                    txt_exibir = f"### ✨ {tarefa}"
                    if responsavel_original != jogador_atual:
                        txt_exibir += f" *(Mandada por {responsavel_original} 👑)*"
                    st.markdown(txt_exibir)
                with col_btn:
                    if chave_tarefa in st.session_state.tarefas_concluidas_hoje:
                        st.success("✅ Concluída!")
                    else:
                        if st.button("Concluí! ⭐", key=chave_tarefa):
                            # CORREÇÃO AQUI: removida linha antiga com erro de digitação ('stars')
                            st.session_state.jogadores[jogador_atual]["estrelas"] += 1
                            st.session_state.tarefas_concluidas_hoje.append(chave_tarefa)
                            st.rerun()

    # Mostrar Punições aplicadas no Fim de Semana
    if dia_sel in ["SÁB", "DOM"]:
        for punicao in st.session_state.punicoes_fim_de_semana:
            if punicao["culpado"] == jogador_atual and punicao["dia_aplicar"] == dia_sel:
                alguma_tarefa = True
                chave_punicao = f"punir_{punicao['culpado']}_{punicao['tarefa']}_{punicao['dia_aplicar']}"
                
                col_txt, col_btn = st.columns([3, 1])
                with col_txt:
                    st.markdown(f"### ⚠️ [PUNIÇÃO] Executar: **{punicao['tarefa']}** *(Pertencia a {punicao['dono_original']})*")
                with col_btn:
                    if chave_punicao in st.session_state.tarefas_concluidas_hoje:
                        st.success("✅ Punição Cumprida!")
                    else:
                        if st.button("Cumpri Punição!", key=chave_punicao):
                            st.session_state.tarefas_concluidas_hoje.append(chave_punicao)
                            st.rerun()
                            
    if not alguma_tarefa:
        st.info("Você não tem nenhuma tarefa ou punição escalada para este dia! 🎉")

# --- ABA 2: RANKING GERAL ---
with aba_ranking:
