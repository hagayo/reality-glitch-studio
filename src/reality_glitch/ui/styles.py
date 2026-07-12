import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --ink: #082f3b;
                --navy: #062b35;
                --teal: #00a896;
                --cyan: #00c8e8;
                --orange: #ff6b35;
                --yellow: #ffd23f;
                --lime: #9ee37d;
                --paper: #f7fffd;
                --muted: #55747c;
                --line: rgba(8, 47, 59, 0.12);
            }

            html, body, [class*="css"] {
                font-family: Inter, system-ui, -apple-system, "Segoe UI", sans-serif;
            }

            .stApp {
                direction: rtl;
                color: var(--ink);
                background:
                    radial-gradient(circle at 92% 5%, rgba(255, 210, 63, .34), transparent 19rem),
                    radial-gradient(circle at 4% 20%, rgba(0, 200, 232, .18), transparent 25rem),
                    linear-gradient(135deg, #f7fffd 0%, #effffc 48%, #fffaf0 100%);
            }

            .block-container {
                max-width: 1450px;
                padding-top: 1.15rem;
                padding-bottom: 5rem;
            }

            h1, h2, h3, h4, p, label { text-align: right; }

            [data-testid="stSidebar"] {
                background:
                    radial-gradient(circle at 15% 0%, rgba(0, 200, 232, .20), transparent 14rem),
                    linear-gradient(180deg, #063d49 0%, #052c36 55%, #041f28 100%);
                border-left: 0;
                box-shadow: 18px 0 45px rgba(3, 37, 46, .18);
            }

            [data-testid="stSidebar"] * { color: #f4fffd; }
            [data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }
            [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.12); }
            [data-testid="stSidebar"] [data-baseweb="select"] > div,
            [data-testid="stSidebar"] [data-baseweb="input"] > div,
            [data-testid="stSidebar"] [data-baseweb="textarea"] > div {
                background: rgba(255,255,255,.10);
                border-color: rgba(255,255,255,.20);
            }
            [data-testid="stSidebar"] [data-baseweb="select"] svg { fill: #fff; }
            [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
            [data-testid="stSidebar"] .stCaption { color: rgba(244,255,253,.74) !important; }

            .sidebar-brand {
                display: flex;
                align-items: center;
                gap: .8rem;
                padding: .55rem .15rem 1rem;
            }
            .brand-mark {
                display: grid;
                place-items: center;
                width: 46px;
                height: 46px;
                border-radius: 15px;
                color: #06323d !important;
                font-weight: 950;
                font-size: 1.3rem;
                background: linear-gradient(135deg, var(--yellow), var(--orange));
                box-shadow: 0 10px 25px rgba(255,107,53,.35);
            }
            .sidebar-brand strong { display: block; font-size: 1.05rem; }
            .sidebar-brand span { display: block; color: rgba(244,255,253,.62) !important; font-size: .78rem; margin-top: .1rem; }

            .start-here {
                display: flex;
                align-items: center;
                gap: .55rem;
                margin: 0 0 1.2rem;
                padding: .72rem .8rem;
                border: 1px solid rgba(255,210,63,.45);
                border-radius: 14px;
                background: rgba(255,210,63,.13);
                color: #fff3b0 !important;
                font-size: .85rem;
                font-weight: 800;
            }
            .start-dot {
                width: 9px;
                height: 9px;
                border-radius: 50%;
                background: var(--yellow);
                box-shadow: 0 0 0 6px rgba(255,210,63,.14);
                animation: pulse 1.8s infinite;
            }
            @keyframes pulse { 50% { box-shadow: 0 0 0 11px rgba(255,210,63,0); } }

            .control-heading {
                display: flex;
                align-items: center;
                gap: .72rem;
                margin: 1.15rem 0 .6rem;
            }
            .control-heading > span {
                display: grid;
                place-items: center;
                min-width: 31px;
                height: 31px;
                border-radius: 10px;
                background: linear-gradient(135deg, var(--cyan), var(--teal));
                color: #032e37 !important;
                font-weight: 950;
                box-shadow: 0 7px 16px rgba(0,200,232,.22);
            }
            .control-heading strong { display: block; color: #fff !important; font-size: .96rem; }
            .control-heading small { display: block; color: rgba(244,255,253,.56) !important; font-size: .73rem; margin-top: .03rem; }

            [data-testid="stFileUploader"] section {
                border: 2px dashed rgba(255,210,63,.65);
                border-radius: 18px;
                background: rgba(255,255,255,.07);
                padding: .65rem;
            }
            [data-testid="stFileUploader"] section:hover {
                border-color: var(--yellow);
                background: rgba(255,210,63,.10);
            }
            [data-testid="stFileUploader"] button {
                color: var(--navy) !important;
                background: var(--yellow) !important;
                border: 0 !important;
            }

            [data-testid="stSidebar"] .stButton > button {
                border: 1px solid rgba(255,255,255,.20);
                background: rgba(255,255,255,.08);
                color: #fff !important;
            }
            [data-testid="stSidebar"] .stButton > button:hover {
                border-color: var(--cyan);
                background: rgba(0,200,232,.16);
            }
            [data-testid="stSidebar"] .stButton > button[kind="primary"] {
                color: #062f39 !important;
                border: 0;
                background: linear-gradient(135deg, var(--yellow), var(--orange));
                box-shadow: 0 10px 24px rgba(255,107,53,.22);
            }

            .pipeline-ribbon {
                margin: .6rem 0 .95rem;
                padding: .8rem .85rem;
                border-radius: 15px;
                color: #062e38 !important;
                font-size: .81rem;
                font-weight: 850;
                line-height: 1.6;
                background: linear-gradient(135deg, #b8fff2, #fff3a8);
                box-shadow: inset 0 0 0 1px rgba(255,255,255,.55);
            }

            [data-testid="stSidebar"] details {
                border: 1px solid rgba(255,255,255,.12);
                border-radius: 14px;
                background: rgba(255,255,255,.055);
            }
            [data-testid="stSidebar"] details[open] {
                border-color: rgba(0,200,232,.38);
                background: rgba(0,200,232,.07);
            }

            .sidebar-tip {
                margin-top: 1.15rem;
                padding: .85rem .9rem;
                border-right: 4px solid var(--orange);
                border-radius: 12px;
                color: rgba(244,255,253,.74) !important;
                background: rgba(255,107,53,.10);
                font-size: .78rem;
                line-height: 1.55;
            }
            .sidebar-tip b { color: #ffb08e !important; }

            /* Sidebar widget contrast: keep all controls readable on the dark panel. */
            [data-testid="stSidebar"] [data-baseweb="select"] > div,
            [data-testid="stSidebar"] [data-baseweb="input"] > div,
            [data-testid="stSidebar"] [data-baseweb="textarea"] > div,
            [data-testid="stSidebar"] [data-baseweb="base-input"] {
                color: #f7fffd !important;
                background: #0b4a56 !important;
                border-color: rgba(255,255,255,.28) !important;
            }
            /* Form fields use light backgrounds, so their entered/selected text is navy. */
            input,
            textarea {
                color: navy !important;
                -webkit-text-fill-color: navy !important;
                opacity: 1 !important;
            }
            [data-testid="stSidebar"] input,
            [data-testid="stSidebar"] textarea,
            [data-testid="stSidebar"] [data-baseweb="input"] input,
            [data-testid="stSidebar"] [data-baseweb="base-input"] input,
            [data-testid="stSidebar"] [role="combobox"],
            [data-testid="stSidebar"] [role="combobox"] *,
            [data-testid="stSidebar"] [data-baseweb="select"] span,
            [data-testid="stSidebar"] [data-baseweb="select"] p {
                color: navy !important;
                -webkit-text-fill-color: navy !important;
                opacity: 1 !important;
            }
            [data-testid="stSidebar"] input::placeholder,
            [data-testid="stSidebar"] textarea::placeholder {
                color: rgba(247,255,253,.58) !important;
                -webkit-text-fill-color: rgba(247,255,253,.58) !important;
            }
            [data-testid="stSidebar"] details,
            [data-testid="stSidebar"] details > summary {
                color: #f7fffd !important;
                background: #0a3d48 !important;
            }
            [data-testid="stSidebar"] details > summary:hover {
                background: #0d4b58 !important;
            }
            [data-testid="stSidebar"] details p,
            [data-testid="stSidebar"] details label,
            [data-testid="stSidebar"] details span,
            [data-testid="stSidebar"] details div {
                color: #f7fffd;
            }
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
            [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
                color: #eefefa !important;
            }
            [data-testid="stSidebar"] [data-baseweb="tag"] {
                color: #06333c !important;
                background: #ffd23f !important;
            }
            [data-testid="stSidebar"] [data-baseweb="tag"] * {
                color: #06333c !important;
                -webkit-text-fill-color: #06333c !important;
            }
            [data-testid="stSidebar"] [role="radiogroup"] label,
            [data-testid="stSidebar"] [data-testid="stCheckbox"] label {
                color: #f7fffd !important;
            }
            [data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {
                color: #062f39 !important;
                background: var(--yellow) !important;
            }

            [data-testid="stSidebar"] [data-baseweb="input"] > div,
            [data-testid="stSidebar"] [data-baseweb="base-input"],
            [data-testid="stSidebar"] [data-baseweb="textarea"] > div {
                background: #ffffff !important;
                color: navy !important;
            }

            /* Selectboxes use a light field, so their selected value must be dark. */
            [data-testid="stSidebar"] div[data-baseweb="select"] > div {
                background: #ffffff !important;
                border-color: rgba(8, 47, 59, .18) !important;
                color: #082f3b !important;
            }
            [data-testid="stSidebar"] div[data-baseweb="select"] > div *,
            [data-testid="stSidebar"] div[data-baseweb="select"] input {
                color: #082f3b !important;
                -webkit-text-fill-color: #082f3b !important;
                opacity: 1 !important;
            }

            [data-testid="stSidebar"] [role="combobox"],
            [data-testid="stSidebar"] [role="combobox"] div,
            [data-testid="stSidebar"] [role="combobox"] span,
            [data-testid="stSidebar"] [role="combobox"] p {
                color: navy !important;
                -webkit-text-fill-color: navy !important;
                opacity: 1 !important;
            }

            [data-testid="stSidebar"] div[data-baseweb="select"] svg {
                fill: #082f3b !important;
                color: #082f3b !important;
            }
            [data-testid="stSidebar"] div[data-baseweb="select"] input::placeholder {
                color: #55747c !important;
                -webkit-text-fill-color: #55747c !important;
                opacity: 1 !important;
            }

            /* BaseWeb menus are rendered in a portal outside the sidebar. */
            [role="listbox"],
            [role="option"] {
                color: #082f3b !important;
                background: #ffffff !important;
            }
            [role="option"] * {
                color: #082f3b !important;
                -webkit-text-fill-color: #082f3b !important;
            }
            [role="option"]:hover,
            [aria-selected="true"][role="option"] {
                background: #dffff8 !important;
            }

            .energy-hero {
                position: relative;
                overflow: hidden;
                min-height: 250px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 2.5rem 3rem;
                margin-bottom: 1.25rem;
                border-radius: 34px;
                color: #fff;
                background:
                    linear-gradient(118deg, #063c49 0%, #007d78 55%, #00a896 100%);
                box-shadow: 0 25px 65px rgba(4, 71, 82, .22);
            }
            .energy-hero::after {
                content: "";
                position: absolute;
                inset: auto -8% -70% 20%;
                height: 220px;
                transform: rotate(-7deg);
                background: linear-gradient(90deg, var(--yellow), var(--orange));
                opacity: .96;
            }
            .energy-copy { position: relative; z-index: 2; max-width: 820px; }
            .energy-kicker {
                display: inline-block;
                padding: .38rem .7rem;
                border-radius: 999px;
                color: #073640 !important;
                background: var(--yellow);
                font-size: .7rem;
                font-weight: 950;
                letter-spacing: .14em;
            }
            .energy-copy h1 {
                color: #fff;
                font-size: clamp(2.5rem, 5.2vw, 5.2rem);
                line-height: .95;
                letter-spacing: -.06em;
                margin: .85rem 0 .75rem;
            }
            .energy-copy h1 em {
                color: var(--yellow);
                font-style: normal;
            }
            .energy-copy p {
                color: rgba(255,255,255,.82);
                font-size: 1.15rem;
                margin: 0;
            }
            .hero-pills { display: flex; gap: .48rem; flex-wrap: wrap; margin-top: 1.2rem; }
            .hero-pills span {
                padding: .38rem .7rem;
                border-radius: 999px;
                color: #fff !important;
                background: rgba(255,255,255,.13);
                border: 1px solid rgba(255,255,255,.17);
                font-size: .76rem;
                font-weight: 750;
            }
            .hero-spark {
                position: relative;
                z-index: 2;
                display: grid;
                place-items: center;
                min-width: 135px;
                height: 135px;
                border-radius: 38px;
                transform: rotate(9deg);
                color: #073640 !important;
                font-size: 4.5rem;
                background: linear-gradient(135deg, var(--yellow), #fff5b5);
                box-shadow: 0 20px 50px rgba(255,210,63,.34);
            }
            .hero-orb { position: absolute; border-radius: 50%; filter: blur(1px); opacity: .35; }
            .orb-one { width: 170px; height: 170px; top: -65px; right: 36%; background: var(--cyan); }
            .orb-two { width: 95px; height: 95px; bottom: 20px; left: 38%; background: var(--orange); }

            .launch-zone {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 1.5rem;
                min-height: 250px;
                padding: 2.5rem;
                border: 3px dashed rgba(0,168,150,.34);
                border-radius: 30px;
                background: rgba(255,255,255,.65);
                box-shadow: 0 18px 45px rgba(8,47,59,.06);
            }
            .launch-symbol {
                display: grid;
                place-items: center;
                width: 85px;
                height: 85px;
                border-radius: 25px;
                color: #083943;
                font-size: 2.4rem;
                font-weight: 900;
                background: linear-gradient(135deg, var(--yellow), var(--orange));
                box-shadow: 0 15px 34px rgba(255,107,53,.24);
            }
            .launch-label { color: var(--orange); font-weight: 900; font-size: .75rem; letter-spacing: .1em; }
            .launch-zone h2 { margin: .3rem 0; font-size: 2rem; }
            .launch-zone p { margin: 0; color: var(--muted); }

            .journey-card {
                min-height: 135px;
                margin-top: 1rem;
                padding: 1.1rem;
                border-radius: 22px;
                background: #fff;
                border: 1px solid var(--line);
                box-shadow: 0 13px 30px rgba(8,47,59,.06);
            }
            .journey-card span { color: var(--orange); font-weight: 950; font-size: .8rem; }
            .journey-card strong { display: block; margin: .45rem 0 .15rem; font-size: 1.15rem; }
            .journey-card small { color: var(--muted); }

            .info-tile {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: .85rem 1rem;
                margin-bottom: .85rem;
                border-radius: 16px;
                border: 1px solid var(--line);
                background: rgba(255,255,255,.78);
                box-shadow: 0 9px 24px rgba(8,47,59,.05);
            }
            .info-tile span { color: var(--muted); font-size: .8rem; }
            .info-tile strong { color: var(--teal); }

            .section-banner {
                display: flex;
                align-items: end;
                justify-content: space-between;
                margin: .6rem 0 .8rem;
                padding: .1rem .2rem;
            }
            .section-banner span { color: var(--orange); font-size: .72rem; font-weight: 950; letter-spacing: .15em; }
            .section-banner h2 { margin: 0; font-size: 1.75rem; }
            .section-banner.compact { margin-top: .4rem; }

            .image-label {
                display: inline-flex;
                margin-bottom: .45rem;
                padding: .3rem .68rem;
                border-radius: 999px;
                font-size: .76rem;
                font-weight: 900;
            }
            .image-label.source { color: #075c65; background: #d8fffa; }
            .image-label.result { color: #97300d; background: #fff0c2; }

            div[data-testid="stImage"] img {
                border-radius: 24px;
                border: 1px solid rgba(8,47,59,.12);
                box-shadow: 0 18px 42px rgba(8,47,59,.12);
            }

            .step-card-title {
                display: flex;
                align-items: center;
                gap: .55rem;
                margin-bottom: .4rem;
            }
            .step-card-title span {
                display: grid;
                place-items: center;
                width: 29px;
                height: 29px;
                border-radius: 9px;
                color: #06333c;
                background: var(--yellow);
                font-weight: 950;
            }

            .quick-export-line {
                margin-top: 1rem;
                padding: .9rem 1rem;
                border-radius: 14px;
                color: #07545d;
                background: linear-gradient(90deg, #dffff8, #fff5c5);
                font-weight: 750;
                text-align: center;
            }

            .export-hero {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1.35rem 1.5rem;
                margin-bottom: 1rem;
                border-radius: 23px;
                color: #fff;
                background: linear-gradient(110deg, #007d78, #00a896);
                box-shadow: 0 16px 36px rgba(0,125,120,.16);
            }
            .export-hero span { color: #cafff6 !important; font-size: .7rem; font-weight: 900; letter-spacing: .13em; }
            .export-hero h2 { color: #fff; margin: .25rem 0 0; }
            .export-badge {
                padding: .7rem .9rem;
                border-radius: 15px;
                color: #06343e !important;
                background: var(--yellow);
                font-weight: 950;
            }
            .download-copy {
                min-height: 135px;
                padding: 1.2rem;
                margin-bottom: .75rem;
                border-radius: 21px;
                background: #fff;
                border: 1px solid var(--line);
            }
            .download-copy h3 { margin: .3rem 0; }
            .download-copy p { color: var(--muted); margin: 0; }
            .download-icon {
                display: grid;
                place-items: center;
                width: 38px;
                height: 38px;
                border-radius: 12px;
                color: #06343e;
                background: var(--yellow);
                font-weight: 950;
            }
            .gif-copy .download-icon { background: var(--cyan); }

            .stTabs [data-baseweb="tab-list"] {
                gap: .4rem;
                padding: .38rem;
                margin: .25rem 0 1rem;
                border-radius: 17px;
                border: 1px solid var(--line);
                background: rgba(255,255,255,.76);
            }
            .stTabs [data-baseweb="tab"] {
                min-height: 45px;
                padding: .55rem 1rem;
                border-radius: 12px;
                color: var(--muted);
                font-weight: 800;
            }
            .stTabs [aria-selected="true"] {
                color: #fff !important;
                background: linear-gradient(135deg, var(--teal), #00897d);
            }

            .stButton > button,
            .stDownloadButton > button {
                min-height: 2.85rem;
                border-radius: 13px;
                font-weight: 850;
                transition: transform .15s ease, box-shadow .15s ease;
            }
            .stButton > button:hover,
            .stDownloadButton > button:hover { transform: translateY(-1px); }
            .stDownloadButton > button[kind="primary"],
            .main .stButton > button[kind="primary"] {
                border: 0;
                color: #06343e;
                background: linear-gradient(135deg, var(--yellow), var(--orange));
                box-shadow: 0 11px 25px rgba(255,107,53,.22);
            }

            @media (max-width: 900px) {
                .energy-hero { padding: 1.8rem; min-height: 220px; }
                .hero-spark { display: none; }
                .energy-copy h1 { font-size: 3rem; }
                .launch-zone { flex-direction: column; text-align: center; }
                .launch-zone h2, .launch-zone p { text-align: center; }
                .export-hero { align-items: flex-start; gap: 1rem; }
            }

            @media (prefers-color-scheme: dark) {
                .stApp {
                    color: #eafffb;
                    background:
                        radial-gradient(circle at 92% 5%, rgba(255,210,63,.12), transparent 19rem),
                        radial-gradient(circle at 4% 20%, rgba(0,200,232,.12), transparent 25rem),
                        #061b22;
                }
                .journey-card,
                .info-tile,
                .download-copy,
                .launch-zone,
                .stTabs [data-baseweb="tab-list"] {
                    background: rgba(9, 44, 53, .82);
                    border-color: rgba(255,255,255,.10);
                }
                .journey-card small,
                .download-copy p,
                .launch-zone p,
                .info-tile span { color: rgba(232,255,251,.64); }
                .section-banner h2,
                .download-copy h3,
                .launch-zone h2 { color: #f2fffd; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
