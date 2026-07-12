from __future__ import annotations

import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --ink: #10233d;
                --muted: #61708a;
                --paper: #fffdf9;
                --white: #ffffff;
                --blue: #4f7cff;
                --cyan: #34d5ff;
                --mint: #56e6bf;
                --yellow: #ffd65a;
                --coral: #ff6f91;
                --orange: #ff9f43;
                --violet: #8b6cff;
                --line: rgba(16, 35, 61, .10);
                --soft-shadow: 0 18px 60px rgba(36, 62, 112, .11);
                --card-shadow: 0 12px 34px rgba(36, 62, 112, .10);
            }

            html, body, [class*="css"] {
                font-family: Inter, Arial, sans-serif;
            }

            .stApp {
                direction: rtl;
                color: var(--ink);
                background:
                    radial-gradient(circle at 10% 8%, rgba(52, 213, 255, .20), transparent 23rem),
                    radial-gradient(circle at 92% 15%, rgba(255, 111, 145, .18), transparent 22rem),
                    radial-gradient(circle at 70% 88%, rgba(86, 230, 191, .16), transparent 25rem),
                    linear-gradient(145deg, #f8fbff 0%, #fffdf9 48%, #fff7fb 100%);
                background-attachment: fixed;
            }

            .block-container {
                max-width: 1480px;
                padding-top: 1.15rem;
                padding-bottom: 5rem;
            }

            h1, h2, h3, h4, p, label { text-align: right; }

            /* Sidebar */
            [data-testid="stSidebar"] {
                width: 25rem !important;
                background:
                    radial-gradient(circle at 15% 5%, rgba(255, 214, 90, .36), transparent 15rem),
                    radial-gradient(circle at 85% 18%, rgba(52, 213, 255, .30), transparent 17rem),
                    linear-gradient(165deg, #172b56 0%, #163c69 48%, #125a72 100%);
                border-left: 1px solid rgba(255,255,255,.18);
                box-shadow: 16px 0 48px rgba(24, 49, 89, .18);
            }

            [data-testid="stSidebar"] > div:first-child {
                padding-top: .75rem;
            }

            [data-testid="stSidebar"] hr {
                border-color: rgba(255,255,255,.14);
            }

            .sidebar-brand {
                display: flex;
                align-items: center;
                gap: .85rem;
                padding: .6rem .2rem .9rem;
            }

            .brand-mark {
                width: 48px;
                height: 48px;
                display: grid;
                place-items: center;
                border-radius: 17px;
                color: #14284e !important;
                font-size: 1.32rem;
                font-weight: 950;
                background: linear-gradient(135deg, var(--yellow), #fff0a7 48%, var(--coral));
                box-shadow: 0 14px 30px rgba(255, 159, 67, .30);
                transform: rotate(-4deg);
            }

            .sidebar-brand strong {
                display: block;
                color: #fff !important;
                font-size: 1.08rem;
                font-weight: 900;
            }

            .sidebar-brand span {
                display: block;
                margin-top: .12rem;
                color: rgba(255,255,255,.68) !important;
                font-size: .78rem;
            }

            .start-here {
                display: flex;
                align-items: center;
                gap: .65rem;
                margin: .15rem 0 1.25rem;
                padding: .82rem .9rem;
                border-radius: 17px;
                color: #173150 !important;
                font-weight: 900;
                font-size: .88rem;
                background: linear-gradient(135deg, #fff6bf, #d9fff4);
                box-shadow: 0 12px 26px rgba(9, 39, 72, .18);
            }

            .start-dot {
                width: 10px;
                height: 10px;
                flex: 0 0 auto;
                border-radius: 50%;
                background: var(--coral);
                box-shadow: 0 0 0 0 rgba(255,111,145,.45);
                animation: modernPulse 1.8s infinite;
            }

            @keyframes modernPulse {
                70% { box-shadow: 0 0 0 10px rgba(255,111,145,0); }
                100% { box-shadow: 0 0 0 0 rgba(255,111,145,0); }
            }

            .control-heading {
                display: flex;
                align-items: center;
                gap: .75rem;
                margin: 1.25rem 0 .68rem;
            }

            .control-heading > span {
                min-width: 34px;
                height: 34px;
                display: grid;
                place-items: center;
                border-radius: 12px;
                color: #163252 !important;
                font-weight: 950;
                background: linear-gradient(135deg, var(--cyan), var(--mint));
                box-shadow: 0 8px 20px rgba(52,213,255,.25);
            }

            .control-heading strong {
                display: block;
                color: #fff !important;
                font-size: 1rem;
                font-weight: 900;
            }

            .control-heading small {
                display: block;
                margin-top: .08rem;
                color: rgba(255,255,255,.62) !important;
                font-size: .75rem;
            }

            [data-testid="stFileUploader"] section {
                padding: .7rem;
                border: 2px dashed rgba(255,255,255,.52);
                border-radius: 20px;
                background: rgba(255,255,255,.10);
                transition: background .18s ease, border-color .18s ease, transform .18s ease;
            }

            [data-testid="stFileUploader"] section:hover {
                border-color: var(--yellow);
                background: rgba(255,255,255,.16);
                transform: translateY(-1px);
            }

            [data-testid="stFileUploader"] button {
                color: #173150 !important;
                border: 0 !important;
                background: linear-gradient(135deg, var(--yellow), #ffeaa0) !important;
                font-weight: 900 !important;
                border-radius: 12px !important;
            }

            [data-testid="stSidebar"] .stButton > button {
                min-height: 2.75rem;
                border-radius: 14px;
                border: 1px solid rgba(255,255,255,.22);
                color: #fff !important;
                background: rgba(255,255,255,.09);
                font-weight: 900 !important;
                transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
            }

            [data-testid="stSidebar"] .stButton > button:hover {
                color: #172d4e !important;
                border-color: transparent;
                background: linear-gradient(135deg, var(--cyan), var(--mint));
                box-shadow: 0 10px 25px rgba(52,213,255,.22);
                transform: translateY(-2px);
            }

            [data-testid="stSidebar"] .stButton > button[kind="primary"] {
                color: #182d4b !important;
                border: 0 !important;
                background: linear-gradient(135deg, var(--yellow), var(--orange));
                box-shadow: 0 12px 27px rgba(255,159,67,.26);
            }

            [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #ffe477, var(--coral));
            }

            [data-testid="stSidebar"] .stButton > button:disabled {
                opacity: .38;
                transform: none;
            }

            /* Sidebar widget contrast */
            /* Form readability */
            input,
            textarea {
                color: navy !important;
                -webkit-text-fill-color: navy !important;
                opacity: 1 !important;
            }

            [data-testid="stSidebar"] div[data-baseweb="select"] > div,
            [data-testid="stSidebar"] [data-baseweb="input"] > div,
            [data-testid="stSidebar"] [data-baseweb="base-input"],
            [data-testid="stSidebar"] [data-baseweb="textarea"] > div {
                min-height: 44px;
                color: #082f3b !important;
                background: #ffffff !important;
                border: 1px solid rgba(255,255,255,.50) !important;
                border-radius: 14px !important;
                box-shadow: 0 8px 22px rgba(8, 36, 70, .12);
            }

            [data-testid="stSidebar"] div[data-baseweb="select"] > div *,
            [data-testid="stSidebar"] [role="combobox"],
            [data-testid="stSidebar"] [role="combobox"] *,
            [data-testid="stSidebar"] input,
            [data-testid="stSidebar"] textarea {
                color: #082f3b !important;
                -webkit-text-fill-color: #082f3b !important;
                opacity: 1 !important;
            }

            [data-testid="stSidebar"] input::placeholder,
            [data-testid="stSidebar"] textarea::placeholder {
                color: rgba(8,47,59,.45) !important;
                -webkit-text-fill-color: rgba(8,47,59,.45) !important;
            }

            [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
            [data-testid="stSidebar"] .stCaption,
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
                color: rgba(255,255,255,.78) !important;
            }

            [role="listbox"] {
                color: #10233d !important;
                background: #fff !important;
            }

            [data-baseweb="popover"] [role="option"] {
                color: #10233d !important;
                background: #fff !important;
            }

            [data-baseweb="popover"] [role="option"]:hover,
            [data-baseweb="popover"] [aria-selected="true"] {
                color: #10233d !important;
                background: #eaf9ff !important;
            }

            [data-testid="stSidebar"] details {
                margin-top: .45rem;
                border: 1px solid rgba(255,255,255,.16);
                border-radius: 17px;
                background: rgba(255,255,255,.08);
                overflow: hidden;
            }

            [data-testid="stSidebar"] details[open] {
                border-color: rgba(52,213,255,.42);
                background: rgba(255,255,255,.12);
                box-shadow: 0 10px 26px rgba(4, 31, 56, .15);
            }

            [data-testid="stSidebar"] details > summary {
                color: #fff !important;
                font-weight: 900;
                background: transparent !important;
            }

            [data-testid="stSidebar"] details p,
            [data-testid="stSidebar"] details label,
            [data-testid="stSidebar"] details span,
            [data-testid="stSidebar"] details div {
                color: #fff;
            }

            [data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] {
                color: #173150 !important;
                background: var(--yellow) !important;
                border-radius: 9px;
                font-weight: 900;
            }

            [data-testid="stSidebar"] [data-testid="stCheckbox"] label,
            [data-testid="stSidebar"] [role="radiogroup"] label {
                color: #fff !important;
            }

            .pipeline-ribbon {
                margin: .75rem 0 .9rem;
                padding: .85rem .9rem;
                border-radius: 16px;
                color: #163250 !important;
                font-size: .82rem;
                font-weight: 900;
                line-height: 1.65;
                background: linear-gradient(135deg, #d9fff5, #fff3b7 65%, #ffd9e3);
                box-shadow: 0 10px 24px rgba(10, 39, 72, .14);
            }

            .effect-card {
                margin: .9rem 0;
                padding: .85rem;
                border-radius: 19px;
                border: 1px solid rgba(255,255,255,.17);
                background: rgba(255,255,255,.08);
                box-shadow: inset 0 1px 0 rgba(255,255,255,.08);
            }

            .effect-card-title {
                display: flex;
                align-items: center;
                gap: .65rem;
                margin-bottom: .7rem;
            }

            .effect-card-index {
                width: 30px;
                height: 30px;
                display: grid;
                place-items: center;
                border-radius: 11px;
                color: #173150 !important;
                font-weight: 950;
                background: linear-gradient(135deg, var(--yellow), #fff2ad);
            }

            .effect-card-name {
                color: #fff !important;
                font-size: .96rem;
                font-weight: 950;
            }

            .sidebar-tip {
                margin-top: 1rem;
                padding: .9rem;
                border-radius: 15px;
                border: 1px solid rgba(255,255,255,.14);
                color: rgba(255,255,255,.78) !important;
                background: rgba(255,111,145,.12);
                font-size: .8rem;
                line-height: 1.55;
            }

            .sidebar-tip b { color: #fff0a5 !important; }

            /* Hero */
            .energy-hero {
                position: relative;
                display: flex;
                align-items: center;
                justify-content: space-between;
                min-height: 270px;
                margin-bottom: 1.35rem;
                padding: 2.15rem 2.4rem;
                overflow: hidden;
                border-radius: 32px;
                border: 1px solid rgba(255,255,255,.70);
                background:
                    linear-gradient(120deg, rgba(255,255,255,.92), rgba(255,255,255,.62)),
                    linear-gradient(135deg, #d9f8ff, #fff7bf 48%, #ffdce7);
                box-shadow: var(--soft-shadow);
                isolation: isolate;
            }

            .energy-hero::before {
                content: "";
                position: absolute;
                inset: 0;
                opacity: .26;
                background-image:
                    linear-gradient(rgba(16,35,61,.08) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(16,35,61,.08) 1px, transparent 1px);
                background-size: 30px 30px;
                mask-image: linear-gradient(to left, black, transparent 75%);
            }

            .energy-copy {
                position: relative;
                z-index: 3;
                max-width: 760px;
            }

            .energy-kicker {
                display: inline-flex;
                padding: .42rem .72rem;
                border-radius: 999px;
                color: #1f4d6d;
                font-size: .72rem;
                font-weight: 950;
                letter-spacing: .13em;
                background: rgba(52,213,255,.18);
            }

            .energy-copy h1 {
                margin: .55rem 0 .35rem;
                color: var(--ink);
                font-size: clamp(3rem, 6vw, 5.4rem);
                line-height: .96;
                letter-spacing: -.065em;
                font-weight: 950;
                text-align: right;
            }

            .energy-copy h1 em {
                display: inline-block;
                color: transparent;
                font-style: normal;
                background: linear-gradient(135deg, var(--blue), var(--violet), var(--coral));
                -webkit-background-clip: text;
                background-clip: text;
            }

            .energy-copy p {
                margin: .9rem 0 1.1rem;
                color: #52647e;
                font-size: 1.08rem;
                font-weight: 650;
            }

            .hero-pills {
                display: flex;
                flex-wrap: wrap;
                gap: .55rem;
            }

            .hero-pills span {
                padding: .48rem .72rem;
                border-radius: 999px;
                color: #243a5b;
                font-size: .78rem;
                font-weight: 900;
                background: rgba(255,255,255,.78);
                border: 1px solid rgba(16,35,61,.08);
                box-shadow: 0 6px 16px rgba(36,62,112,.08);
            }

            .hero-spark {
                position: relative;
                z-index: 2;
                display: grid;
                place-items: center;
                width: 145px;
                height: 145px;
                border-radius: 40px;
                color: #18304e;
                font-size: 4rem;
                background: linear-gradient(135deg, var(--yellow), var(--coral));
                box-shadow:
                    0 25px 55px rgba(255,111,145,.28),
                    inset 0 1px 0 rgba(255,255,255,.7);
                transform: rotate(8deg);
                animation: floatSpark 4s ease-in-out infinite;
            }

            @keyframes floatSpark {
                50% { transform: rotate(4deg) translateY(-8px); }
            }

            .hero-orb {
                position: absolute;
                border-radius: 50%;
                filter: blur(2px);
                opacity: .55;
            }

            .orb-one {
                width: 240px;
                height: 240px;
                top: -90px;
                left: -60px;
                background: var(--cyan);
            }

            .orb-two {
                width: 180px;
                height: 180px;
                right: 22%;
                bottom: -100px;
                background: var(--mint);
            }

            /* Empty state */
            .launch-zone {
                display: flex;
                align-items: center;
                gap: 1.3rem;
                padding: 1.55rem 1.7rem;
                border-radius: 25px;
                border: 1px solid rgba(255,255,255,.8);
                background: rgba(255,255,255,.72);
                box-shadow: var(--card-shadow);
                backdrop-filter: blur(16px);
            }

            .launch-symbol {
                width: 62px;
                height: 62px;
                display: grid;
                place-items: center;
                border-radius: 20px;
                color: #1a3150;
                font-size: 2rem;
                font-weight: 950;
                background: linear-gradient(135deg, var(--cyan), var(--mint));
            }

            .launch-label {
                color: var(--coral);
                font-size: .75rem;
                font-weight: 950;
                letter-spacing: .08em;
            }

            .launch-zone h2 {
                margin: .2rem 0 .18rem;
                color: var(--ink);
                font-size: 1.65rem;
                font-weight: 950;
            }

            .launch-zone p { margin: 0; color: var(--muted); }

            .journey-card {
                min-height: 138px;
                margin-top: 1rem;
                padding: 1.15rem;
                border-radius: 22px;
                border: 1px solid rgba(255,255,255,.78);
                background: rgba(255,255,255,.72);
                box-shadow: var(--card-shadow);
                backdrop-filter: blur(14px);
                transition: transform .18s ease, box-shadow .18s ease;
            }

            .journey-card:hover {
                transform: translateY(-4px) rotate(-.5deg);
                box-shadow: 0 18px 42px rgba(36,62,112,.14);
            }

            .journey-card span {
                color: var(--blue);
                font-size: .75rem;
                font-weight: 950;
            }

            .journey-card strong {
                display: block;
                margin: .45rem 0 .22rem;
                color: var(--ink);
                font-size: 1.08rem;
                font-weight: 950;
            }

            .journey-card small { color: var(--muted); line-height: 1.45; }

            /* Metadata and content cards */
            .info-tile {
                min-height: 88px;
                margin-bottom: .9rem;
                padding: 1rem 1.1rem;
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,.78);
                background: rgba(255,255,255,.72);
                box-shadow: var(--card-shadow);
                backdrop-filter: blur(14px);
            }

            .info-tile span {
                display: block;
                color: var(--muted);
                font-size: .74rem;
                font-weight: 800;
            }

            .info-tile strong {
                display: block;
                margin-top: .25rem;
                color: var(--ink);
                font-size: 1.1rem;
                font-weight: 950;
            }

            .section-banner {
                display: flex;
                align-items: flex-end;
                justify-content: space-between;
                margin: .2rem 0 .9rem;
                padding: 1rem 1.2rem;
                border-radius: 20px;
                background: linear-gradient(135deg, rgba(79,124,255,.10), rgba(52,213,255,.12), rgba(255,111,145,.10));
                border: 1px solid rgba(79,124,255,.10);
            }

            .section-banner span {
                color: var(--blue);
                font-size: .72rem;
                font-weight: 950;
                letter-spacing: .1em;
            }

            .section-banner h2 {
                margin: .15rem 0 0;
                color: var(--ink);
                font-size: 1.45rem;
                font-weight: 950;
            }

            .section-banner.compact { margin-top: .25rem; }

            div[data-testid="stImage"] img {
                border-radius: 24px;
                box-shadow: 0 18px 45px rgba(36,62,112,.16);
            }

            .image-label {
                display: inline-flex;
                margin-bottom: .55rem;
                padding: .42rem .72rem;
                border-radius: 999px;
                color: #173150;
                font-size: .78rem;
                font-weight: 950;
            }

            .image-label.source { background: #dff6ff; }
            .image-label.result { background: #ffe0e8; }

            .step-card-title {
                display: flex;
                align-items: center;
                gap: .55rem;
                margin: .4rem 0 .55rem;
            }

            .step-card-title span {
                width: 29px;
                height: 29px;
                display: grid;
                place-items: center;
                border-radius: 10px;
                color: #173150;
                font-weight: 950;
                background: var(--yellow);
            }

            .step-card-title strong { color: var(--ink); font-weight: 950; }

            .quick-export-line {
                margin-top: 1rem;
                padding: .85rem 1rem;
                border-radius: 16px;
                color: #24415e;
                font-weight: 850;
                background: linear-gradient(135deg, #e6fbff, #fff4c8);
                border: 1px solid rgba(52,213,255,.14);
            }

            .export-hero {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 1rem;
                padding: 1.2rem 1.35rem;
                border-radius: 23px;
                color: var(--ink);
                background: linear-gradient(135deg, #dffaff, #fff6c7 55%, #ffdce6);
                box-shadow: var(--card-shadow);
            }

            .export-hero span {
                color: var(--blue);
                font-size: .72rem;
                font-weight: 950;
                letter-spacing: .08em;
            }

            .export-hero h2 {
                margin: .18rem 0 0;
                color: var(--ink);
                font-size: 1.45rem;
                font-weight: 950;
            }

            .export-badge {
                padding: .65rem .82rem;
                border-radius: 15px;
                color: #fff;
                font-weight: 950;
                background: linear-gradient(135deg, var(--blue), var(--violet));
                box-shadow: 0 10px 22px rgba(79,124,255,.24);
            }

            .download-copy {
                min-height: 122px;
                margin-bottom: .75rem;
                padding: 1rem 1.1rem;
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,.76);
                background: rgba(255,255,255,.72);
                box-shadow: var(--card-shadow);
            }

            .download-copy h3 {
                margin: .35rem 0 .15rem;
                color: var(--ink);
                font-weight: 950;
            }

            .download-copy p { margin: 0; color: var(--muted); }

            .download-icon {
                width: 38px;
                height: 38px;
                display: grid;
                place-items: center;
                border-radius: 13px;
                color: #173150;
                font-weight: 950;
                background: var(--yellow);
            }

            .gif-copy .download-icon { background: var(--cyan); }

            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: .55rem;
                margin: .2rem 0 1rem;
                padding: .45rem;
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,.78);
                background: rgba(255,255,255,.70);
                box-shadow: var(--card-shadow);
                backdrop-filter: blur(16px);
            }

            .stTabs [data-baseweb="tab"] {
                justify-content: center;
                min-height: 52px;
                padding: .7rem 1rem;
                border-radius: 15px;
                color: #28425f;
                background: transparent;
                font-size: .95rem;
                font-weight: 950 !important;
                transition: transform .16s ease, background .16s ease, color .16s ease, box-shadow .16s ease;
            }

            .stTabs [data-baseweb="tab"]:hover {
                color: #173150 !important;
                background: linear-gradient(135deg, #dffaff, #fff5c7);
                box-shadow: 0 9px 22px rgba(36,62,112,.10);
                transform: translateY(-2px);
            }

            .stTabs [aria-selected="true"] {
                color: #fff !important;
                background: linear-gradient(135deg, var(--blue), var(--violet), var(--coral));
                box-shadow: 0 12px 28px rgba(79,124,255,.26);
            }

            .stTabs [data-baseweb="tab-highlight"] { display: none; }

            /* Main buttons */
            .main .stButton > button,
            .main .stDownloadButton > button {
                min-height: 3rem;
                border-radius: 15px;
                font-weight: 950;
                transition: transform .15s ease, box-shadow .15s ease;
            }

            .main .stButton > button:hover,
            .main .stDownloadButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 26px rgba(36,62,112,.14);
            }

            .main .stButton > button[kind="primary"],
            .main .stDownloadButton > button[kind="primary"] {
                color: #fff;
                border: 0;
                background: linear-gradient(135deg, var(--blue), var(--violet), var(--coral));
                box-shadow: 0 12px 28px rgba(79,124,255,.24);
            }


            .mask-preview-heading {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                margin: 1.35rem 0 .75rem;
                padding: .85rem 1rem;
                border-radius: 16px;
                background: linear-gradient(135deg, rgba(0,215,255,.14), rgba(255,213,79,.14));
                border: 1px solid rgba(0,170,210,.20);
            }
            .mask-preview-heading span {
                font-size: .72rem;
                font-weight: 950;
                letter-spacing: .11em;
                color: #007f9b;
            }
            .mask-preview-heading strong {
                color: #0b3140;
                font-size: 1rem;
            }

            @media (max-width: 1050px) {
                [data-testid="stSidebar"] { width: 22rem !important; }
                .energy-hero { min-height: 230px; padding: 1.7rem; }
                .hero-spark { width: 110px; height: 110px; font-size: 3rem; }
            }

            @media (max-width: 780px) {
                .block-container { padding-left: .75rem; padding-right: .75rem; }
                .energy-hero { padding: 1.45rem; border-radius: 24px; }
                .energy-copy h1 { font-size: 2.8rem; }
                .hero-spark, .hero-orb { display: none; }
                .stTabs [data-baseweb="tab-list"] { grid-template-columns: 1fr; }
                .launch-zone { flex-direction: column; align-items: flex-start; }
                .export-hero { align-items: flex-start; gap: .8rem; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
