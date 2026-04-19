import streamlit as st
import pandas as pd
import os
import hashlib
import streamlit.components.v1 as components

# ─── CONFIG ───────────────────────────────────────────────────────────────────


# Настройка вкладки браузера
st.set_page_config(
    page_title="GUWfix", 
    page_icon="GUWfix.jpg", 
    layout="centered"
)

# Настройка иконки для главного экрана смартфона
st.markdown(
    f"""
    <head>
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/amanzholzhanur/GUWfix/main/GUWfix.jpg">
        <link rel="icon" href="https://raw.githubusercontent.com/amanzholzhanur/GUWfix/main/GUWfix.jpg">
        
        <meta name="apple-mobile-web-app-title" content="GUWfix">
        
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
    </head>
    <style>
        /* Убираем лишний отступ сверху, чтобы дизайн смотрелся чище */
        .block-container {{
            padding-top: 3rem;
        }}
    </style>
    """,
    unsafe_allow_html=True
)
USER_FILE      = "users_v2.csv"
REP_FILE       = "reports_v2.csv"
ADMIN_EMAIL    = "admin@guwfix.kz"
ADMIN_PASSWORD = "admin123"

# ─── TRANSLATIONS ─────────────────────────────────────────────────────────────

LANG = {
"RU": {
"app_sub": "Городская платформа решения дорожных проблем",
"login": "Войти", "register": "Регистрация",
"email": "Email", "password": "Пароль",
"confirm_pw": "Повторите пароль", "name": "Имя",
"login_btn": "Войти", "reg_btn": "Зарегистрироваться", "logout": "Выйти",
"menu_profile": "Профиль", "menu_report": "Новая заявка", "menu_leaders": "Лидеры",
"profile_title": "Мой профиль", "my_reports": "Мои заявки",
"no_reports": "У вас ещё нет заявок.", "new_report": "Новая заявка",
"address": "Адрес", "category": "Категория", "description": "Описание проблемы",
"submit": "Отправить заявку", "leaderboard": "Таблица лидеров",
"admin_panel": "Панель администратора", "pending": "Ожидают решения",
"solved": "Решено", "no_pending": "Нет новых заявок.",
"admin_answer": "Ответ администратора", "mark_fixed": "Отметить как исправлено",
"all_reports": "Все заявки", "voice_hint": "Голосовой ввод (Chrome/Edge)",
"speak": "Говорить", "level": "Уровень", "xp": "Опыт (XP)",
"err_addr": "Укажите адрес.", "err_desc": "Добавьте описание.",
"err_fill": "Заполните все поля.", "err_pw": "Пароли не совпадают.",
"err_exists": "Этот email уже зарегистрирован.",
"err_notfound": "Пользователь не найден.", "err_wrong_pw": "Неверный пароль.",
"err_answer": "Напишите ответ перед отправкой.",
"success_reg": "Аккаунт создан! Войдите.",
"success_rep": "Заявка отправлена! +50 XP",
"success_fixed": "Статус обновлён!",
"categories": ["Дороги"],
"levels": [("Tourist 🎒",0),("Активный гражданин 🏃",100),("Страж города 🛡️",300),("Легендарный урбанист 🏆",600)],
"name_col": "Имя",
},
"KZ": {
"app_sub": "Жол мәселелерін шешудің қалалық платформасы",
"login": "Кіру", "register": "Тіркелу",
"email": "Email", "password": "Құпиясөз",
"confirm_pw": "Құпиясөзді растаңыз", "name": "Аты",
"login_btn": "Кіру", "reg_btn": "Тіркелу", "logout": "Шығу",
"menu_profile": "Профиль", "menu_report": "Жаңа өтініш", "menu_leaders": "Көшбасшылар",
"profile_title": "Менің профилім", "my_reports": "Менің өтініштерім",
"no_reports": "Сізде әлі өтініш жоқ.", "new_report": "Жаңа өтініш",
"address": "Мекен-жай", "category": "Санат", "description": "Мәселенің сипаттамасы",
"submit": "Өтінішті жіберу", "leaderboard": "Көшбасшылар кестесі",
"admin_panel": "Әкімші панелі", "pending": "Шешімін күтуде",
"solved": "Шешілді", "no_pending": "Жаңа өтініш жоқ.",
"admin_answer": "Әкімші жауабы", "mark_fixed": "Орындалды деп белгілеу",
"all_reports": "Барлық өтініштер", "voice_hint": "Дауыстық енгізу (Chrome/Edge)",
"speak": "Сөйлеу", "level": "Деңгей", "xp": "Тәжірибе (XP)",
"err_addr": "Мекен-жайды көрсетіңіз.", "err_desc": "Сипаттама қосыңыз.",
"err_fill": "Барлық өрістерді толтырыңыз.", "err_pw": "Құпиясөздер сәйкес емес.",
"err_exists": "Бұл email тіркелген.",
"err_notfound": "Пайдаланушы табылмады.", "err_wrong_pw": "Қате құпиясөз.",
"err_answer": "Жіберу алдында жауап жазыңыз.",
"success_reg": "Аккаунт жасалды! Кіріңіз.",
"success_rep": "Өтініш жіберілді! +50 XP",
"success_fixed": "Күй жаңартылды!",
"categories": ["Жолдар"],
"levels": [("Tourist 🎒",0),("Белсенді азамат 🏃",100),("Қала қорғаушысы 🛡️",300),("Аңызға айналған урбанист 🏆",600)],
"name_col": "Аты",
},
"EN": {
"app_sub": "Urban Road Issue Resolution Platform",
"login": "Log In", "register": "Register",
"email": "Email", "password": "Password",
"confirm_pw": "Confirm Password", "name": "Name",
"login_btn": "Log In", "reg_btn": "Register", "logout": "Log Out",
"menu_profile": "Profile", "menu_report": "New Report", "menu_leaders": "Leaders",
"profile_title": "My Profile", "my_reports": "My Reports",
"no_reports": "You have no reports yet.", "new_report": "New Report",
"address": "Address", "category": "Category", "description": "Problem Description",
"submit": "Submit Report", "leaderboard": "Leaderboard",
"admin_panel": "Admin Panel", "pending": "Awaiting Resolution",
"solved": "Resolved", "no_pending": "No new reports.",
"admin_answer": "Admin Response", "mark_fixed": "Mark as Fixed",
"all_reports": "All Reports", "voice_hint": "Voice Input (Chrome/Edge)",
"speak": "Speak", "level": "Level", "xp": "Experience (XP)",
"err_addr": "Please enter an address.", "err_desc": "Please add a description.",
"err_fill": "Please fill in all fields.", "err_pw": "Passwords do not match.",
"err_exists": "This email is already registered.",
"err_notfound": "User not found.", "err_wrong_pw": "Incorrect password.",
"err_answer": "Please write a response before submitting.",
"success_reg": "Account created! Please log in.",
"success_rep": "Report submitted! +50 XP",
"success_fixed": "Status updated!",
"categories": ["Roads"],
"levels": [("Tourist 🎒",0),("Active Citizen 🏃",100),("City Guardian 🛡️",300),("Legendary Urbanist 🏆",600)],
"name_col": "Name",
},
}

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def load_users():
    if os.path.exists(USER_FILE): return pd.read_csv(USER_FILE)
    return pd.DataFrame(columns=["email","name","password","xp"])
def save_users(df): df.to_csv(USER_FILE, index=False)
def load_reports():
    if os.path.exists(REP_FILE): return pd.read_csv(REP_FILE)
    return pd.DataFrame(columns=["id","user","addr","cat","desc","status","admin_note"])
def save_reports(df): df.to_csv(REP_FILE, index=False)
def next_id(df):
    if df.empty or "id" not in df.columns: return 1
    return int(df["id"].max()) + 1
def get_level(xp, lang="RU"):
    result = LANG[lang]["levels"][0][0]
    for name, threshold in LANG[lang]["levels"]:
        if xp >= threshold: result = name
    return result

# ─── SESSION STATE ────────────────────────────────────────────────────────────

for k, v in [("auth",False),("user",""),("role",""),("voice_desc",""),("lang","RU")]:
    if k not in st.session_state: st.session_state[k] = v

def T(key): return LANG[st.session_state.lang][key]

# ─── CSS ──────────────────────────────────────────────────────────────────────

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;900&family=Nunito:wght@400;600;700;800&display=swap');

:root {
  --gold:    #D4A017;
  --gold2:   #F0C040;
  --brown:   #5C3A1E;
  --brown2:  #3B2007;
  --cream:   #FDF6E3;
}

html, body, [data-testid="stAppViewContainer"] {
  font-family: 'Nunito', sans-serif !important;
}
[data-testid="stAppViewContainer"] > .main {
  background-color: var(--cream);
}

/* Typography */
h1,h2,h3 {
  font-family: 'Playfair Display', serif !important;
  color: var(--brown) !important;
}
p, label, div, span {
  font-family: 'Nunito', sans-serif !important;
  font-size: 1.05rem !important;
}

/* Buttons */
.stButton > button {
  background: linear-gradient(135deg, var(--gold), var(--brown)) !important;
  color: #fff !important;
  border: none !important;
  border-radius: 14px !important;
  font-family: 'Nunito', sans-serif !important;
  font-size: 1.05rem !important;
  font-weight: 800 !important;
  padding: 0.65rem 1.5rem !important;
  box-shadow: 0 4px 18px rgba(212,160,23,0.38) !important;
  transition: transform 0.15s, box-shadow 0.15s !important;
  letter-spacing: 0.02em;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(212,160,23,0.5) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > textarea {
  border-radius: 12px !important;
  border: 2px solid var(--gold) !important;
  font-family: 'Nunito', sans-serif !important;
  font-size: 1.05rem !important;
  background: rgba(255,255,255,0.95) !important;
  padding: 0.55rem 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > textarea:focus {
  border-color: var(--brown) !important;
  box-shadow: 0 0 0 3px rgba(212,160,23,0.22) !important;
}
.stSelectbox > div > div {
  border-radius: 12px !important;
  border: 2px solid var(--gold) !important;
  font-size: 1.05rem !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
  font-family: 'Playfair Display', serif !important;
  font-size: 1.15rem !important;
  color: var(--brown) !important;
  font-weight: 600;
}
.stTabs [aria-selected="true"] {
  color: var(--gold) !important;
  border-bottom: 3px solid var(--gold) !important;
}

/* Metrics */
[data-testid="metric-container"] {
  background: linear-gradient(135deg, rgba(212,160,23,0.15), rgba(92,58,30,0.08)) !important;
  border-radius: 18px !important;
  padding: 1.1rem 1.3rem !important;
  border: 1.5px solid rgba(212,160,23,0.35) !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  font-family: 'Playfair Display', serif !important;
  color: var(--gold) !important;
  font-size: 2.1rem !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
  font-size: 1rem !important;
  color: var(--brown) !important;
  font-weight: 700 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, var(--brown2) 0%, var(--brown) 100%) !important;
}
[data-testid="stSidebar"] * { color: var(--cream) !important; }
[data-testid="stSidebar"] .stRadio label {
  font-size: 1.1rem !important;
  font-weight: 700 !important;
}

/* Expander */
.streamlit-expanderHeader {
  font-family: 'Nunito', sans-serif !important;
  font-size: 1.05rem !important;
  font-weight: 700 !important;
  color: var(--brown) !important;
  background: rgba(212,160,23,0.1) !important;
  border-radius: 10px !important;
}

/* Alerts */
.stAlert {
  border-radius: 12px !important;
  font-size: 1.05rem !important;
}

hr { border-color: rgba(212,160,23,0.4) !important; margin: 1.2rem 0 !important; }

/* Header card */
.header-card {
  background: linear-gradient(135deg, var(--brown2), #7A4A1E);
  border-radius: 24px;
  padding: 2.2rem 2.5rem 1.8rem;
  margin-bottom: 1.8rem;
  box-shadow: 0 8px 36px rgba(59,32,7,0.28);
  text-align: center;
  position: relative;
  overflow: hidden;
}
.header-card h1 {
  color: var(--gold2) !important;
  font-size: 3rem !important;
  margin: 0 0 0.3rem 0 !important;
  text-shadow: 0 2px 10px rgba(0,0,0,0.35);
}
.header-card p {
  color: rgba(253,246,227,0.85) !important;
  font-size: 1.15rem !important;
  margin: 0 !important;
}

/* XP bar */
.xp-bar-bg {
  background: rgba(212,160,23,0.2);
  border-radius: 99px; height: 14px;
  margin-top: 0.5rem; overflow: hidden;
}
.xp-bar-fill {
  background: linear-gradient(90deg, var(--gold2), var(--brown));
  height: 100%; border-radius: 99px;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  [data-testid="stAppViewContainer"] > .main { background-color: #1A1008 !important; }
  h1,h2,h3 { color: var(--gold2) !important; }
  .stTextInput > div > div > input,
  .stTextArea > div > textarea { background: rgba(40,24,8,0.95) !important; color: var(--cream) !important; }
}
</style>
""", unsafe_allow_html=True)

# ─── KAZAKH ORNAMENTS (injected via HTML component) ──────────────────────────

def inject_ornaments():
    components.html("""
<script>
(function() {
const dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const stroke = dark ? '#FFFFFF' : '#D4A017';
const op = dark ? '0.08' : '0.12';

  function makeSVG(rotate) {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"
                  width="100%" height="100%"
                  style="transform:rotate(${rotate}deg)" opacity="${op}">
      <g fill="none" stroke="${stroke}" stroke-width="2.2">
        <circle cx="200" cy="200" r="90"/>
        <circle cx="200" cy="200" r="62"/>
        <circle cx="200" cy="200" r="34"/>
        <path d="M200,110 Q235,155 200,200 Q165,155 200,110"/>
        <path d="M290,200 Q245,235 200,200 Q245,165 290,200"/>
        <path d="M200,290 Q165,245 200,200 Q235,245 200,290"/>
        <path d="M110,200 Q155,165 200,200 Q155,235 110,200"/>
        <path d="M263,137 Q245,178 200,200 Q222,158 263,137"/>
        <path d="M263,263 Q222,242 200,200 Q245,222 263,263"/>
        <path d="M137,263 Q158,222 200,200 Q178,242 137,263"/>
        <path d="M137,137 Q178,158 200,200 Q158,178 137,137"/>
        <path d="M15,15 Q55,15 55,55 Q55,95 15,95" stroke-width="3.5"/>
        <path d="M15,15 Q15,55 55,55" stroke-width="1.8"/>
        <path d="M35,15 Q55,35 55,55" stroke-width="1.2" stroke-dasharray="4,3"/>
        <path d="M385,15 Q345,15 345,55 Q345,95 385,95" stroke-width="3.5"/>
        <path d="M385,15 Q385,55 345,55" stroke-width="1.8"/>
        <path d="M365,15 Q345,35 345,55" stroke-width="1.2" stroke-dasharray="4,3"/>
        <path d="M15,385 Q55,385 55,345 Q55,305 15,305" stroke-width="3.5"/>
        <path d="M15,385 Q15,345 55,345" stroke-width="1.8"/>
        <path d="M385,385 Q345,385 345,345 Q345,305 385,305" stroke-width="3.5"/>
        <path d="M385,385 Q385,345 345,345" stroke-width="1.8"/>
        <polyline points="0,12 25,0 50,12 75,0 100,12 125,0 150,12 175,0 200,12 225,0 250,12 275,0 300,12 325,0 350,12 375,0 400,12" stroke-width="1.5"/>
        <polyline points="0,388 25,400 50,388 75,400 100,388 125,400 150,388 175,400 200,388 225,400 250,388 275,400 300,388 325,400 350,388 375,400 400,388" stroke-width="1.5"/>
        <path d="M8,180 Q28,200 8,220" stroke-width="2"/>
        <path d="M392,180 Q372,200 392,220" stroke-width="2"/>
        <rect x="178" y="178" width="44" height="44" transform="rotate(45,200,200)" stroke-width="1.2"/>
        <rect x="162" y="162" width="76" height="76" transform="rotate(45,200,200)" stroke-width="0.8"/>
      </g>
    </svg>`;
  }

  const positions = [
    {top:'-40px', left:'-40px', rot:0},
    {bottom:'-40px', right:'-40px', rot:180},
  ];

  positions.forEach(({top,left,bottom,right,rot}) => {
    const d = document.createElement('div');
    d.style.cssText = [
      'position:fixed', 'z-index:0', 'pointer-events:none',
      'width:34vw', 'height:34vw',
      top    ? `top:${top}`       : '',
      left   ? `left:${left}`     : '',
      bottom ? `bottom:${bottom}` : '',
      right  ? `right:${right}`   : '',
    ].filter(Boolean).join(';') + ';';
    d.innerHTML = makeSVG(rot);
    document.body.appendChild(d);
  });
})();
</script>
""", height=0)

# ─── HEADER CARD ──────────────────────────────────────────────────────────────

def header_card():
    st.markdown(f"""
<div class="header-card">
<h1>🛣️ GUWfix Pro</h1>
<p>{T('app_sub')}</p>
</div>
""", unsafe_allow_html=True)

# ─── LANGUAGE BUTTONS ─────────────────────────────────────────────────────────

def lang_buttons():
    _, c1, c2, c3 = st.columns([4,1,1,1])
    if c1.button("🇷🇺 RU"): st.session_state.lang="RU"; st.rerun()
    if c2.button("🇰🇿 KZ"): st.session_state.lang="KZ"; st.rerun()
    if c3.button("🇬🇧 EN"): st.session_state.lang="EN"; st.rerun()

# ─── VOICE COMPONENT ──────────────────────────────────────────────────────────

def voice_component():
    lang_map = {"RU":"ru-RU","KZ":"kk-KZ","EN":"en-US"}
    lc = lang_map[st.session_state.lang]
    components.html(f"""
<style>
.vbtn {{background:linear-gradient(135deg,#D4A017,#5C3A1E);color:#fff;
border:none;border-radius:14px;padding:13px 28px;font-size:16px;
font-weight:800;cursor:pointer;font-family:'Nunito',sans-serif;
box-shadow:0 4px 16px rgba(212,160,23,0.45);transition:transform .15s;}}
.vbtn:hover{{transform:translateY(-2px);}}
#vs{{margin-top:10px;font-size:14px;color:#D4A017;font-family:'Nunito',sans-serif;font-weight:700;}}
</style>
<button class="vbtn" onclick="go()">🎤 {T('speak')}</button>
<p id="vs">{T('voice_hint')}</p>
<script>
function go(){{
const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
if(!SR){{document.getElementById('vs').innerText='❌ Chrome/Edge only';return;}}
const r=new SR(); r.lang='{lc}'; r.interimResults=false;
document.getElementById('vs').innerText='🔴 …';
r.onresult=e=>{{
const t=e.results[0][0].transcript;
document.getElementById('vs').innerText='✅ '+t;
const u=new URL(window.parent.location.href);
u.searchParams.set('voice',t);
window.parent.history.replaceState({{}},'',u);
}};
r.onerror=e=>{{document.getElementById('vs').innerText='❌ '+e.error;}};
r.start();
}}
</script>
""", height=100)

# ─── SCREENS ──────────────────────────────────────────────────────────────────

def show_auth():
    lang_buttons()
    header_card()
    tab1, tab2 = st.tabs([f"🔑 {T('login')}", f"📝 {T('register')}"])

    with tab1:
        email = st.text_input(T("email"), key="li_e").strip().lower()
        pwd   = st.text_input(T("password"), type="password", key="li_p")
        if st.button(T("login_btn"), use_container_width=True, key="li_btn"):
            if email == ADMIN_EMAIL and pwd == ADMIN_PASSWORD:
                st.session_state.update(auth=True,user=ADMIN_EMAIL,role="admin"); st.rerun()
            else:
                df = load_users(); row = df[df["email"]==email]
                if row.empty: st.error(T("err_notfound"))
                elif row.iloc[0]["password"] != hash_pw(pwd): st.error(T("err_wrong_pw"))
                else: st.session_state.update(auth=True,user=email,role="user"); st.rerun()

    with tab2:
        name  = st.text_input(T("name"), key="re_n")
        email = st.text_input(T("email"), key="re_e").strip().lower()
        pwd   = st.text_input(T("password"), type="password", key="re_p")
        pwd2  = st.text_input(T("confirm_pw"), type="password", key="re_p2")
        if st.button(T("reg_btn"), use_container_width=True, key="re_btn"):
            if not all([name,email,pwd,pwd2]): st.error(T("err_fill"))
            elif pwd != pwd2: st.error(T("err_pw"))
            else:
                df = load_users()
                if email in df["email"].values: st.error(T("err_exists"))
                else:
                    new = pd.DataFrame([{"email":email,"name":name,"password":hash_pw(pwd),"xp":0}])
                    save_users(pd.concat([df,new],ignore_index=True))
                    st.success(T("success_reg"))

def show_admin():
    st.title(f"🏛️ {T('admin_panel')}")
    df = load_reports()
    pending = df[df["status"]=="Pending"]
    fixed   = df[df["status"]=="Fixed"]
    c1,c2 = st.columns(2)
    c1.metric(T("pending"), len(pending))
    c2.metric(T("solved"),  len(fixed))
    st.divider()
    if pending.empty:
        st.info(T("no_pending"))
    else:
        for idx, row in pending.iterrows():
            with st.expander(f"📌 #{int(row['id'])} — {row['addr']}"):
                st.markdown(f"**👤** {row['user']}")
                st.markdown(f"**📝** {row['desc']}")
                ans = st.text_area(T("admin_answer"), key=f"aa_{int(row['id'])}")
                if st.button(T("mark_fixed"), key=f"fix_{int(row['id'])}"):
                    if not ans.strip(): st.warning(T("err_answer"))
                    else:
                        # ТА САМАЯ СТРОКА ИСПРАВЛЕНИЯ:
                        df["admin_note"] = df["admin_note"].astype(str)
                        
                        df.loc[idx,"status"] = "Fixed"
                        df.loc[idx,"admin_note"] = ans.strip()
                        save_reports(df)
                        st.success(T("success_fixed")); st.rerun()
    st.divider()
    st.subheader(T("all_reports"))
    if not df.empty:
        st.dataframe(df[["id","user","addr","status"]], use_container_width=True)

def show_profile():
    st.header(f"👤 {T('profile_title')}")
    users = load_users(); reps = load_reports()
    row = users[users["email"]==st.session_state.user]
    if row.empty: st.warning("Profile not found."); return
    xp   = int(row.iloc[0]["xp"])
    name = row.iloc[0]["name"]
    lvl  = get_level(xp, st.session_state.lang)
    milestones = [100,300,600,1000]
    next_ms = next((m for m in milestones if m > xp), 1000)
    pct = min(int(xp/next_ms*100),100)
    c1,c2 = st.columns(2)
    c1.metric(T("name"), name)
    c2.metric(T("xp"), f"{xp} XP")
    st.markdown(f"**{T('level')}:** {lvl}")
    st.markdown(f"""
<div class="xp-bar-bg"><div class="xp-bar-fill" style="width:{pct}%"></div></div>
<small style="color:#8B6914;font-size:0.9rem">{xp} / {next_ms} XP</small>
""", unsafe_allow_html=True)
    st.divider()
    st.subheader(T("my_reports"))
    my = reps[reps["user"]==st.session_state.user]
    if my.empty: st.write(T("no_reports"))
    else:
        cols = [c for c in ["id","addr","cat","status","admin_note"] if c in my.columns]
        st.dataframe(my[cols], use_container_width=True)

def show_report():
    st.header(f"📝 {T('new_report')}")
    st.markdown(f"**🎤 {T('voice_hint')}**")
    voice_component()
    params = st.query_params
    if "voice" in params and params["voice"]:
        st.session_state.voice_desc = params["voice"]
        st.query_params.clear()
    st.divider()
    addr = st.text_input(f"📍 {T('address')}")
    cat  = st.selectbox(f"📂 {T('category')}", T("categories"))
    desc = st.text_area(f"📝 {T('description')}", value=st.session_state.get("voice_desc",""), height=130)
    if st.button(f"📤 {T('submit')}", use_container_width=True):
        if not addr.strip(): st.error(T("err_addr"))
        elif not desc.strip(): st.error(T("err_desc"))
        else:
            reps  = load_reports(); users = load_users()
            nid   = next_id(reps)
            new_r = pd.DataFrame([{"id":nid,"user":st.session_state.user,"addr":addr.strip(),
"cat":cat,"desc":desc.strip(),"status":"Pending","admin_note":""}])
            save_reports(pd.concat([reps,new_r],ignore_index=True))
            if st.session_state.user in users["email"].values:
                users.loc[users["email"]==st.session_state.user,"xp"] += 50
            else:
                nu = pd.DataFrame([{"email":st.session_state.user,"name":"User","password":"","xp":50}])
                users = pd.concat([users,nu],ignore_index=True)
            save_users(users)
            st.session_state.voice_desc = ""
            st.balloons()
            st.success(f"✅ #{nid} — {T('success_rep')}")

def show_leaderboard():
    st.header(f"🏆 {T('leaderboard')}")
    users = load_users()
    if users.empty: st.info("---"); return
    ld = users[["name","xp"]].copy()
    ld[T("level")] = ld["xp"].apply(lambda x: get_level(int(x), st.session_state.lang))
    ld = ld.sort_values("xp",ascending=False).reset_index(drop=True)
    ld.index += 1
    st.dataframe(ld.rename(columns={"name":T("name_col"),"xp":"XP"}), use_container_width=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────

inject_css()
inject_ornaments()

if not st.session_state.auth:
    show_auth()
else:
    if st.session_state.role == "admin":
        show_admin()
        st.divider()
        if st.button(f"🚪 {T('logout')}"):
            for k in ["auth","user","role","voice_desc"]:
                st.session_state[k] = False if k=="auth" else ""
            st.rerun()
    else:
        with st.sidebar:
            st.markdown(f"## 🛣️ GUWfix")
            st.markdown(f"👋 `{st.session_state.user}`")
            st.divider()
            menu = st.radio("", [
                f"👤 {T('menu_profile')}",
                f"📝 {T('menu_report')}",
                f"🏆 {T('menu_leaders')}"
            ])
            st.divider()
            c1,c2,c3 = st.columns(3)
            if c1.button("RU", key="sb_ru"): st.session_state.lang="RU"; st.rerun()
            if c2.button("KZ", key="sb_kz"): st.session_state.lang="KZ"; st.rerun()
            if c3.button("EN", key="sb_en"): st.session_state.lang="EN"; st.rerun()
            st.divider()
            if st.button(f"🚪 {T('logout')}", use_container_width=True):
                for k in ["auth","user","role","voice_desc"]:
                    st.session_state[k] = False if k=="auth" else ""
                st.rerun()

        if T("menu_profile") in menu:   show_profile()
        elif T("menu_report") in menu:  show_report()
        elif T("menu_leaders") in menu: show_leaderboard()
