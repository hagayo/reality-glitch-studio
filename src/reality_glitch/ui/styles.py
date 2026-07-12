import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
            :root {
                --surface: rgba(255, 255, 255, 0.72);
                --surface-soft: rgba(255, 255, 255, 0.46);
                --border: rgba(17, 24, 39, 0.10);
                --text-soft: rgba(17, 24, 39, 0.68);
                --accent: #f97316;
                --accent-dark: #c2410c;
            }

            .stApp {
                direction: rtl;
                background:
                    radial-gradient(circle at 85% 5%, rgba(14, 165, 233, 0.12), transparent 28rem),
                    radial-gradient(circle at 10% 20%, rgba(249, 115, 22, 0.10), transparent 25rem),
                    #f8fafc;
            }

            .block-container {
                max-width: 1380px;
                padding-top: 1.4rem;
                padding-bottom: 4rem;
            }

            h1, h2, h3, h4, p, label {
                text-align: right;
            }

            [data-testid="stSidebar"] {
                border-left: 1px solid var(--border);
                background: rgba(248, 250, 252, 0.94);
            }

            [data-testid="stSidebar"] > div:first-child {
                padding-top: 1.4rem;
            }

            .sidebar-title {
                font-size: 1.35rem;
                font-weight: 800;
                margin-bottom: 1rem;
            }

            .hero-shell {
                display: flex;
                align-items: flex-end;
                justify-content: space-between;
                gap: 2rem;
                padding: 2rem 2.2rem;
                margin-bottom: 1.4rem;
                border: 1px solid var(--border);
                border-radius: 28px;
                background: linear-gradient(135deg, rgba(255,255,255,.92), rgba(255,255,255,.62));
                box-shadow: 0 18px 55px rgba(15, 23, 42, 0.08);
                backdrop-filter: blur(14px);
            }

            .hero-copy h1 {
                font-size: clamp(2rem, 4vw, 4rem);
                line-height: 1;
                margin: .55rem 0 .8rem;
                letter-spacing: -0.04em;
            }

            .hero-copy p {
                margin: 0;
                color: var(--text-soft);
                font-size: 1.08rem;
            }

            .eyebrow {
                display: inline-block;
                font-size: .75rem;
                font-weight: 800;
                letter-spacing: .18em;
                color: var(--accent-dark);
            }

            .hero-stats {
                display: flex;
                gap: .7rem;
                flex-wrap: wrap;
            }

            .stat-card {
                min-width: 100px;
                padding: .85rem 1rem;
                border-radius: 18px;
                border: 1px solid var(--border);
                background: rgba(255,255,255,.72);
                text-align: center;
            }

            .stat-card strong,
            .stat-card span {
                display: block;
            }

            .stat-card strong {
                font-size: 1.1rem;
            }

            .stat-card span {
                color: var(--text-soft);
                font-size: .78rem;
                margin-top: .15rem;
            }

            .pipeline-box {
                padding: .85rem 1rem;
                border: 1px solid rgba(249, 115, 22, 0.20);
                border-radius: 15px;
                margin: .75rem 0 1rem;
                background: rgba(255, 247, 237, 0.92);
                color: #9a3412;
                font-weight: 700;
                font-size: .9rem;
                line-height: 1.5;
            }

            .empty-state {
                padding: 4rem 2rem 3rem;
                text-align: center;
                border: 1px dashed rgba(15, 23, 42, 0.18);
                border-radius: 26px;
                background: rgba(255,255,255,.55);
            }

            .empty-state h2,
            .empty-state p {
                text-align: center;
            }

            .empty-state p {
                color: var(--text-soft);
            }

            .empty-icon {
                font-size: 2.7rem;
                color: var(--accent);
            }

            .feature-card {
                display: flex;
                flex-direction: column;
                gap: .35rem;
                padding: 1.2rem 1.3rem;
                margin-top: 1rem;
                border: 1px solid var(--border);
                border-radius: 18px;
                background: rgba(255,255,255,.72);
            }

            .feature-card span {
                color: var(--text-soft);
                font-size: .88rem;
            }

            .step-number {
                display: inline-block;
                padding: .25rem .6rem;
                border-radius: 999px;
                background: #fff7ed;
                color: #c2410c;
                font-size: .75rem;
                font-weight: 800;
                margin-bottom: .25rem;
            }

            div[data-testid="stImage"] img {
                border-radius: 20px;
                border: 1px solid var(--border);
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
            }

            [data-testid="stMetric"] {
                padding: .75rem 1rem;
                border: 1px solid var(--border);
                border-radius: 16px;
                background: rgba(255,255,255,.7);
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: .45rem;
                background: rgba(255,255,255,.65);
                border: 1px solid var(--border);
                border-radius: 16px;
                padding: .35rem;
            }

            .stTabs [data-baseweb="tab"] {
                border-radius: 12px;
                padding: .65rem 1rem;
            }

            .stTabs [aria-selected="true"] {
                background: #fff7ed;
                color: #c2410c;
            }

            .stButton > button,
            .stDownloadButton > button {
                border-radius: 12px;
                min-height: 2.7rem;
                font-weight: 700;
            }

            [data-testid="stFileUploader"] {
                border-radius: 16px;
            }

            @media (max-width: 800px) {
                .hero-shell {
                    flex-direction: column;
                    align-items: stretch;
                    padding: 1.5rem;
                }

                .hero-stats {
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                }

                .stat-card {
                    min-width: 0;
                    padding: .7rem .45rem;
                }
            }

            @media (prefers-color-scheme: dark) {
                :root {
                    --surface: rgba(15, 23, 42, 0.72);
                    --surface-soft: rgba(15, 23, 42, 0.52);
                    --border: rgba(255, 255, 255, 0.12);
                    --text-soft: rgba(226, 232, 240, 0.72);
                }

                .stApp {
                    background:
                        radial-gradient(circle at 85% 5%, rgba(14, 165, 233, 0.12), transparent 28rem),
                        radial-gradient(circle at 10% 20%, rgba(249, 115, 22, 0.10), transparent 25rem),
                        #07111f;
                }

                [data-testid="stSidebar"] {
                    background: rgba(7, 17, 31, .96);
                }

                .hero-shell,
                .feature-card,
                .stat-card,
                [data-testid="stMetric"],
                .stTabs [data-baseweb="tab-list"] {
                    background: rgba(15, 23, 42, .72);
                }

                .empty-state {
                    background: rgba(15, 23, 42, .48);
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
