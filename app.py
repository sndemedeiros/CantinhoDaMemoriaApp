import streamlit as st
import pandas as pd
import pyttsx3
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, auth

import cloudinary
import cloudinary.uploader

# --- Configuração da página ---
st.set_page_config(page_title="Cantinho da Memória", layout="wide")

# --- Estilo visual ---
st.markdown("""
<style>
    html, body, [class*="st-"] { font-size: 18px; }
    div.stButton > button { font-size: 20px; padding: 10px 20px; height: auto; }
    h1 { font-size: 3em; } h2 { font-size: 2.5em; } h3 { font-size: 2em; }
</style>
""", unsafe_allow_html=True)

# --- Fala ---
def falar(texto):
    try:
        engine = pyttsx3.init()
        engine.say(texto)
        engine.runAndWait()
    except:
        pass # Ignora erros de TTS, caso não esteja configurado ou haja problemas

# --- Firebase ---
if not firebase_admin._apps:
    try:
        cred_data = dict(st.secrets["firebase_config"])
        cred = credentials.Certificate(cred_data)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"❌ Erro ao iniciar Firebase: {e}")
        st.stop()

db = firestore.client()

# --- Cloudinary ---
cloudinary.config(
    cloud_name = st.secrets["cloudinary"]["cloud_name"],
    api_key = st.secrets["cloudinary"]["api_key"],
    api_secret = st.secrets["cloudinary"]["api_secret"]
)

# --- Estado da sessão ---
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
if 'page' not in st.session_state:
    st.session_state['page'] = "Login" # Adicionado para controle de página

# --- Logout ---
def logout():
    st.session_state["user_id"] = None
    st.session_state["user_email"] = None
    st.session_state['page'] = "Login" # Retorna à página de Login

# --- Título ---
st.title("🌸 Cantinho da Memória")
st.markdown("_Registre momentos com afeto, para lembrar sempre._")

# --- Autenticação ---
if st.session_state["user_id"] is None:
    modo = st.radio("Acesso:", ["Login", "Registrar"])

    if modo == "Login":
        email = st.text_input("📧 E-mail")
        senha = st.text_input("🔐 Senha", type="password")

        if st.button("Entrar"):
            if not email or not senha:
                st.warning("Preencha e-mail e senha.")
            else:
                try:
                    user = auth.get_user_by_email(email)
                    st.session_state["user_id"] = user.uid
                    st.session_state["user_email"] = user.email
                    st.success(f"Bem-vindo(a), {user.email}!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Falha no login: {e}")

    else: # Modo Registrar
        email = st.text_input("📧 E-mail novo")
        senha = st.text_input("🔐 Senha (mín. 6 caracteres)", type="password")

        if st.button("Registrar"):
            if not email or not senha:
                st.warning("Preencha e-mail e senha.")
            elif len(senha) < 6:
                st.warning("A senha deve ter ao menos 6 caracteres.")
            else:
                try:
                    user = auth.create_user(email=email, password=senha)
                    st.success("Conta criada! Faça login para continuar.")
                except Exception as e:
                    st.error(f"Erro ao registrar: {e}")
else: # Usuário logado
    st.sidebar.success(f"Logado como: {st.session_state['user_email']}")
    st.sidebar.button("🚪 Sair", on_click=logout)

    menu = st.radio("Escolha uma seção:", ["📅 Lembretes", "📝 Notas", "🧺 Minhas Memórias"])

    # --- Lembretes ---
    if menu == "📅 Lembretes":
        st.header("📝 Criar Lembrete")
        tarefa = st.text_input("Tarefa")
        hora = st.time_input("Horário")
        repeticao = st.selectbox("Repetição", ["Nenhuma", "Diária", "Semanal", "Mensal"])

        if st.button("Salvar Lembrete"):
            if not tarefa:
                st.warning("Digite a tarefa.")
            else:
                try:
                    db.collection("lembretes").add({
                        "user_id": st.session_state["user_id"],
                        "Tarefa": tarefa,
                        "Hora": str(hora),
                        "Repetição": repeticao,
                        "CriadoEm": firestore.SERVER_TIMESTAMP
                    })
                    st.success("Lembrete salvo!")
                    falar(f"Lembrete: {tarefa}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro: {e}")

        st.subheader("🔔 Meus Lembretes")
        try:
            lembretes = db.collection("lembretes").where(
                "user_id", "==", st.session_state["user_id"]
            ).stream()

            for doc in lembretes:
                item = doc.to_dict()
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**{item.get('Tarefa', 'Sem Tarefa')}** às {item.get('Hora', 'Sem Hora')} — {item.get('Repetição', 'Nenhuma')}")
                with col2:
                    if st.button("🗑️", key=f"lembrete_{doc.id}"):
                        db.collection("lembretes").document(doc.id).delete()
                        st.rerun()
        except Exception as e:
            st.error(f"Erro ao carregar lembretes: {e}")

    # --- Notas ---
    elif menu == "📝 Notas":
        st.header("📝 Nova Nota")
        nota = st.text_area("Escreva sua nota")

        if st.button("Salvar Nota"):
            if not nota:
                st.warning("Digite algo.")
            else:
                try:
                    db.collection("notas").add({
                        "user_id": st.session_state["user_id"],
                        "Nota": nota,
                        "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "CriadoEm": firestore.SERVER_TIMESTAMP
                    })
                    st.success("Nota registrada!")
                    falar("Nota salva com sucesso.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar nota: {e}")

        st.subheader("📚 Minhas Notas")
        try:
            notas = db.collection("notas").where(
                "user_id", "==", st.session_state["user_id"]
            ).stream()

            for doc in notas:
                item = doc.to_dict()
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**{item.get('Nota', 'Sem Nota')}** (_{item.get('Data', 'Sem Data')}_)")
                with col2:
                    if st.button("🗑️", key=f"nota_{doc.id}"):
                        db.collection("notas").document(doc.id).delete()
                        st.rerun()
        except Exception as e:
            st.error(f"Erro ao carregar notas: {e}")

    # --- Memórias ---
    elif menu == "🧺 Minhas Memórias":
        st.header("📷 Registrar uma lembrança especial")

        titulo = st.text_input("Título da memória")
        descricao = st.text_area("Descrição")
        uploaded_file = st.file_uploader("Foto da memória (opcional)", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            st.image(uploaded_file, caption="Pré-visualização", use_column_width=True)

        if st.button("Salvar Memória"):
            if not titulo or not descricao:
                st.warning("Preencha título e descrição.")
            else:
                try:
                    image_url = None
                    if uploaded_file:
                        # Upload da imagem para o Cloudinary
                        result = cloudinary.uploader.upload(uploaded_file, folder="memorias")
                        image_url = result["secure_url"]

                    # Salvar memória no Firestore
                    db.collection("memorias").add({
                        "user_id": st.session_state["user_id"],
                        "Título": titulo,
                        "Descrição": descricao,
                        "ImagemURL": image_url, # Pode ser None se não houver upload
                        "CriadoEm": firestore.SERVER_TIMESTAMP
                    })
                    st.success("🌸 Memória registrada com carinho!")
                    falar(f"Memória registrada: {titulo}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar memória: {e}")

        st.subheader("📖 Memórias guardadas com afeto")
        try:
            memorias_ref = db.collection("memorias").where(
                "user_id", "==", st.session_state["user_id"]
            ).order_by("CriadoEm", direction=firestore.Query.DESCENDING).stream()

            minhas_memorias = []
            for doc in memorias_ref:
                item = doc.to_dict()
                item["ID"] = doc.id
                minhas_memorias.append(item)

                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**{item.get('Título', 'Sem título')}** — {item.get('Descrição', 'Sem descrição')}")
                    if item.get("ImagemURL"):
                        st.image(item["ImagemURL"], caption="🖼️ Foto da memória", use_column_width=True)
                with col2:
                    if st.button("🗑️", key=f"memoria_del_{item['ID']}"):
                        try:
                            db.collection("memorias").document(item["ID"]).delete()
                            st.success("Memória removida!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro ao deletar memória: {e}")

            if minhas_memorias:
                df = pd.DataFrame(minhas_memorias)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📂 Baixar Minhas Memórias",
                    data=csv,
                    file_name="minhas_memorias.csv",
                    mime="text/csv"
                )
            else:
                st.info("Nenhuma memória encontrada. Que tal registrar a primeira?")
        except Exception as e:
            st.error(f"Erro ao carregar memórias: {e}")