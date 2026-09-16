import base64
import io
import math
import struct
import wave

import streamlit as st
import streamlit.components.v1 as components


# ---------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="거지 탈출 RPG",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f5ead7 0%, #ead6b8 100%);
    }

    .game-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        color: #4d321d;
        text-shadow: 2px 2px 0px #ffffff;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #765538;
        margin-top: -8px;
        margin-bottom: 18px;
    }

    .stage-card {
        background: rgba(255,255,255,0.82);
        border: 3px solid #8d6745;
        border-radius: 18px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 5px 12px rgba(80,50,20,0.15);
        margin-bottom: 8px;
    }

    .money {
        font-size: 36px;
        font-weight: 900;
        color: #9b5b00;
    }

    .click-area {
        background: rgba(255,255,255,0.72);
        border: 3px dashed #a87b4d;
        border-radius: 22px;
        padding: 10px;
        text-align: center;
        margin: 5px 0 8px 0;
    }

    .stat-box {
        background: rgba(255,255,255,0.78);
        border-radius: 14px;
        padding: 7px;
        text-align: center;
        border: 2px solid #c29b70;
        margin-bottom: 5px;
    }

    .stat-number {
        font-size: 23px;
        font-weight: 800;
        color: #55371e;
    }

    .shop-card {
        background: rgba(255,255,255,0.8);
        border-radius: 16px;
        padding: 9px;
        border: 2px solid #b98b5d;
        margin-bottom: 5px;
    }

    .floating {
        position: fixed;
        left: 50%;
        top: 42%;
        transform: translate(-50%, -50%);
        z-index: 99999;
        pointer-events: none;
        font-size: 32px;
        font-weight: 900;
        color: #20a020;
        animation: floatUp 0.8s ease-out forwards;
        text-shadow: 1px 1px white;
    }

    @keyframes floatUp {
        0% {
            opacity: 1;
            transform: translate(-50%, -10%);
        }
        100% {
            opacity: 0;
            transform: translate(-50%, -170%);
        }
    }

    .click-button {
        font-size: 28px !important;
        font-weight: 900 !important;
        min-height: 90px !important;
    }

    .clear-box {
        background: linear-gradient(135deg, #fff7c7, #ffe38b);
        border: 4px solid #d59b00;
        border-radius: 22px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 7px 18px rgba(100,70,0,0.2);
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 900px;
    }
    div[data-testid="stVerticalBlock"] {
        gap: 0.35rem;
    }
    h1, h2, h3 {
        margin-top: 0.2rem !important;
        margin-bottom: 0.3rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# 효과음: 별도 파일 없이 간단한 클릭음 생성
# ---------------------------------------------------------
@st.cache_data
def make_click_sound():
    sample_rate = 22050
    duration = 0.09
    frequency = 880

    frames = bytearray()
    total = int(sample_rate * duration)

    for i in range(total):
        envelope = 1.0 - (i / total)
        value = int(
            10000
            * envelope
            * math.sin(2 * math.pi * frequency * i / sample_rate)
        )
        frames += struct.pack("<h", value)

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(frames)

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


CLICK_SOUND = make_click_sound()


def play_click_effect(amount):
    """+금액 표시와 클릭 효과음 재생"""
    components.html(
        f"""
        <audio id="clickSound" preload="auto">
            <source src="data:audio/wav;base64,{CLICK_SOUND}" type="audio/wav">
        </audio>

        <div class="floating">+{amount:,}원</div>

        <script>
            const audio = document.getElementById("clickSound");
            if (audio) {{
                audio.volume = 0.35;
                audio.currentTime = 0;
                const promise = audio.play();
                if (promise !== undefined) {{
                    promise.catch(() => {{}});
                }}
            }}
        </script>
        """,
        height=1,
    )



# ---------------------------------------------------------
# 게임 데이터
# ---------------------------------------------------------
STAGES = [
    {
        "name": "시골 탈출",
        "emoji": "🌾",
        "description": "시골에서 시작된 인생 역전 프로젝트!",
        "target": 1_000_000,
        "background": "시골",
    },
    {
        "name": "길거리 탈출",
        "emoji": "🚶",
        "description": "이제 인도에서 돈을 모아 다음 단계로!",
        "target": 5_000_000,
        "background": "인도 (Sidewalk)",
    },
    {
        "name": "반지하 탈출",
        "emoji": "🏚️",
        "description": "반지하 생활을 벗어나 더 큰 목표를 향해!",
        "target": 50_000_000,
        "background": "반지하",
    },
    {
        "name": "1층 탈출",
        "emoji": "🏠",
        "description": "드디어 1층! 하지만 목표는 아직 남았다.",
        "target": 250_000_000,
        "background": "1층",
    },
    {
        "name": "지방 도시 탈출",
        "emoji": "🏙️",
        "description": "최종 목표를 향한 마지막 도전!",
        "target": 1_250_000_000,
        "background": "지방 도시",
    },
]

BASE_CLICK = 1_000
START_UPGRADE_PRICE = 1_000


# ---------------------------------------------------------
# 세션 상태
# ---------------------------------------------------------
if "money" not in st.session_state:
    st.session_state.money = 0

if "stage" not in st.session_state:
    st.session_state.stage = 0

if "click_power" not in st.session_state:
    st.session_state.click_power = BASE_CLICK

if "click_count" not in st.session_state:
    st.session_state.click_count = 0

if "extra_clicks" not in st.session_state:
    st.session_state.extra_clicks = 0

if "power_upgrade_count" not in st.session_state:
    st.session_state.power_upgrade_count = 0

if "extra_click_upgrade_count" not in st.session_state:
    st.session_state.extra_click_upgrade_count = 0

if "cleared" not in st.session_state:
    st.session_state.cleared = [False] * 5


def power_upgrade_price():
    return math.ceil(
        START_UPGRADE_PRICE * (1.5 ** st.session_state.power_upgrade_count)
    )


def extra_click_upgrade_price():
    return math.ceil(
        START_UPGRADE_PRICE * (1.5 ** st.session_state.extra_click_upgrade_count)
    )


def format_money(value):
    if value >= 100_000_000:
        return f"{value / 100_000_000:.2f}억원"
    if value >= 10_000:
        return f"{value / 10_000:.1f}만원"
    return f"{value:,}원"


def current_click_income():
    return st.session_state.click_power * (1 + st.session_state.extra_clicks)


def check_stage_clear():
    current_stage = st.session_state.stage

    if current_stage >= len(STAGES):
        return

    target = STAGES[current_stage]["target"]

    if st.session_state.money >= target:
        st.session_state.cleared[current_stage] = True

        if current_stage < len(STAGES) - 1:
            st.session_state.stage += 1


# ---------------------------------------------------------
# 제목
# ---------------------------------------------------------
st.markdown('<div class="game-title">💰 거지 탈출 RPG</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">클릭 한 번으로 인생 역전! 나만의 부자 탈출기를 시작하자.</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# 게임 클리어 화면
# ---------------------------------------------------------
if st.session_state.stage >= 5:
    st.markdown(
        """
        <div class="clear-box">
            <h1>🎉 모든 스테이지 클리어! 🎉</h1>
            <h2>🏆 지방 도시 탈출 성공!</h2>
            <p>당신은 12억 5천만원의 목표를 달성했습니다.</p>
            <h2>💰 최종 자산: {}</h2>
        </div>
        """.format(format_money(st.session_state.money)),
        unsafe_allow_html=True,
    )

    st.write("")
    st.success("축하합니다! 이제 진짜 부자입니다.")

    if st.button("🔄 처음부터 다시 시작", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.stop()


stage = STAGES[st.session_state.stage]
target = stage["target"]
progress = min(st.session_state.money / target, 1.0)


# ---------------------------------------------------------
# 스테이지 정보
# ---------------------------------------------------------
st.markdown(
    f"""
    <div class="stage-card">
        <div style="font-size:45px">{stage["emoji"]}</div>
        <h2>STAGE {st.session_state.stage + 1} · {stage["name"]}</h2>
        <p>{stage["description"]}</p>
        <p>📍 배경: <b>{stage["background"]}</b></p>
        <p>🎯 스테이지 목표: <b>{format_money(target)}</b></p>
        <div class="money">{format_money(st.session_state.money)}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.progress(progress)

st.caption(
    f"현재 {format_money(st.session_state.money)} / 목표 {format_money(target)}"
)


# ---------------------------------------------------------
# 능력치
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class="stat-box">
            <div>💵 클릭 수익</div>
            <div class="stat-number">{st.session_state.click_power:,}원</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="stat-box">
            <div>🖱️ 추가 클릭</div>
            <div class="stat-number">+{st.session_state.extra_clicks}회</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""
        <div class="stat-box">
            <div>🔥 실제 클릭 수익</div>
            <div class="stat-number">{current_click_income():,}원</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# 게임 캐릭터
# ---------------------------------------------------------
CHARACTERS = [
    ("🧑‍🦱", "초보 거지", "아직 가진 것은 없지만 돈을 벌기 시작했다!"),
    ("🧑", "거리의 생존자", "조금씩 생활이 나아지고 있다."),
    ("🧑‍💼", "자립 준비생", "이제 안정적인 생활을 꿈꾼다."),
    ("👨‍💼", "성공한 시민", "목표를 향해 빠르게 성장 중이다."),
    ("🕴️", "도시의 부자", "마지막 탈출을 향해 달려간다."),
]

character_emoji, character_name, character_desc = CHARACTERS[st.session_state.stage]

st.markdown(
    f"""
    <div class="stage-card" style="padding:8px; margin-bottom:8px;">
        <div style="font-size:72px; line-height:1.0;">{character_emoji}</div>
        <h3 style="margin:2px 0;">{character_name}</h3>
        <p style="margin:2px 0;">{character_desc}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 메인 클릭
# ---------------------------------------------------------
st.markdown(
    """
    <div class="click-area">
        <h2>🪙 돈을 벌어보자!</h2>
        <p>버튼을 누를 때마다 돈을 획득합니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button(
    f"💰 돈 벌기  +{current_click_income():,}원",
    use_container_width=True,
    type="primary",
):
    income = current_click_income()
    st.session_state.money += income
    st.session_state.click_count += 1
    check_stage_clear()
    play_click_effect(income)
    st.rerun()


# ---------------------------------------------------------
# 상점
# ---------------------------------------------------------
st.divider()
st.header("🛒 상점")

shop1, shop2 = st.columns(2)

with shop1:
    price = power_upgrade_price()

    st.markdown(
        f"""
        <div class="shop-card">
            <h3>💪 클릭 수익 강화</h3>
            <p>클릭 1회당 수익을 +1,000원 올립니다.</p>
            <p>현재: <b>{st.session_state.click_power:,}원/클릭</b></p>
            <p>다음 가격: <b>{price:,}원</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        f"💪 +1,000원 업그레이드 ({price:,}원)",
        disabled=st.session_state.money < price,
        use_container_width=True,
    ):
        st.session_state.money -= price
        st.session_state.click_power += 1_000
        st.session_state.power_upgrade_count += 1
        st.rerun()

with shop2:
    price = extra_click_upgrade_price()

    st.markdown(
        f"""
        <div class="shop-card">
            <h3>🖱️ 추가 클릭</h3>
            <p>한 번 누를 때 클릭 1회만큼의 수익을 추가합니다.</p>
            <p>현재: <b>기본 클릭 × {1 + st.session_state.extra_clicks}</b></p>
            <p>다음 가격: <b>{price:,}원</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        f"🖱️ 클릭 +1회 취급 ({price:,}원)",
        disabled=st.session_state.money < price,
        use_container_width=True,
    ):
        st.session_state.money -= price
        st.session_state.extra_clicks += 1
        st.session_state.extra_click_upgrade_count += 1
        st.rerun()


# ---------------------------------------------------------
# 게임 정보
# ---------------------------------------------------------
with st.expander("📖 게임 정보"):
    st.write("• 이 게임은 클릭커 방식의 간단한 RPG 게임입니다.")
    st.write("• 총 5개의 스테이지가 있습니다.")
    st.write("• 돈을 모아 각 스테이지의 목표 금액에 도달하면 다음 스테이지로 이동합니다.")
    st.write("• 상점에서 클릭 수익과 추가 클릭 능력을 강화할 수 있습니다.")
    st.write("• 업그레이드 가격은 구매할 때마다 50%씩 증가합니다.")
    st.write("• 게임의 기본 콘셉트는 '가난한 상태에서 시작해 돈을 벌며 탈출한다'는 클릭커 RPG입니다.")
    st.caption("※ 특정 게임의 이미지·음원·코드를 그대로 복제하지 않고 독자적인 게임 요소로 구성했습니다.")


# ---------------------------------------------------------
# 리셋
# ---------------------------------------------------------
st.divider()

if st.button("🔄 게임 초기화", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()