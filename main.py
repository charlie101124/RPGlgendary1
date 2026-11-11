import streamlit as st

st.set_page_config(
    page_title="폐쇄된 연구소: 탈출",
    page_icon="🚨",
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #262730;
        color: #ffffff;
        border: 1px solid #41444c;
    }
    .stButton>button:hover {
        background-color: #ff4b4b;
        color: #ffffff;
        border-color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

if "scene" not in st.session_state:
    st.session_state.scene = "start"
    st.session_state.inventory = []
    st.session_state.stamina = 100

def reset_game():
    st.session_state.scene = "start"
    st.session_state.inventory = []
    st.session_state.stamina = 100

def change_scene(next_scene):
    st.session_state.scene = next_scene

st.title("🚨 폐쇄된 연구소: 탈출")
st.caption("당신의 선택에 따라 생존 여부와 엔딩이 결정됩니다.")
st.divider()

with st.sidebar:
    st.header("📊 현재 상태")
    st.progress(st.session_state.stamina / 100, text=f"체력: {st.session_state.stamina}%")
    
    st.subheader("🎒 소지품")
    if st.session_state.inventory:
        for item in st.session_state.inventory:
            st.write(f"- {item}")
    else:
        st.write("비어 있음")
        
    st.divider()
    if st.button("🔄 게임 처음부터 다시 시작"):
        reset_game()
        st.rerun()

current = st.session_state.scene

if current == "start":
    st.subheader("📍 1. 정적 속의 깨어남")
    st.write(
        "눈을 뜨니 차가운 바닥입니다. 붉은 비상등만 켜진 채 경고음이 울리고 있습니다.\n\n"
        "당신은 기억을 잃은 채 심해 연구소의 지하 3층 통제실에서 깨어났습니다. "
        "멀리서 무언가 철문을 긁는 기괴한 소리가 들려옵니다."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 책상 위 반짝이는 보안 카드키를 줍는다"):
            if "보안 카드키" not in st.session_state.inventory:
                st.session_state.inventory.append("보안 카드키")
            change_scene("take_card")
            st.rerun()
    with col2:
        if st.button("🚪 소리가 나기 전에 복도로 곧장 달려나간다"):
            change_scene("hallway_run")
            st.rerun()

elif current == "take_card":
    st.subheader("📍 2. 카드키 획득")
    st.write(
        "보안 카드키를 주머니에 넣었습니다. 그 순간 복도의 철문이 커다란 소리와 함께 일그러집니다.\n\n"
        "시간이 없습니다. 통제실 뒤쪽 비상 통로로 가시겠습니까, 아니면 환기구를 통해 이동하시겠습니까?"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏃‍♂️ 비상 통로 문을 열고 달린다"):
            change_scene("emergency_door")
            st.rerun()
    with col2:
        if st.button("🪜 환기구 덮개를 열고 들어간다"):
            st.session_state.stamina -= 20
            change_scene("vent")
            st.rerun()

elif current == "hallway_run":
    st.subheader("📍 2. 복도로의 뛰어듦")
    st.write(
        "카드키를 챙기지 않고 복도로 뛰어나갔습니다. 복도 끝 보안 게이트가 닫혀 있습니다.\n\n"
        "게이트를 열려면 보안 카드키가 필요합니다! 뒤에서는 정체불명의 그림자가 빠르게 접근해 옵니다."
    )
    
    if st.button("🚪 게이트를 힘으로 부수려고 시도한다"):
        change_scene("ending_caught")
        st.rerun()
    if st.button("🔙 다시 통제실로 들어가 카드키를 찾는다"):
        st.session_state.stamina -= 40
        change_scene("take_card")
        st.rerun()

elif current == "emergency_door":
    st.subheader("📍 3. 비상 통로")
    st.write(
        "카드키로 비상 통로 문을 닫고 잠급니다. 쾅 하는 소리와 함께 문 건너편에서 무언가 부딪히는 소리가 납니다.\n\n"
        "앞에는 [중앙 엘리베이터]와 [잠수정 선착장 표지판]이 보입니다."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛗 엘리베이터를 탄다"):
            change_scene("elevator")
            st.rerun()
    with col2:
        if st.button("⚓ 잠수정 선착장으로 향한다"):
            change_scene("sub_dock")
            st.rerun()

elif current == "vent":
    st.subheader("📍 3. 좁은 환기구")
    st.write(
        "환기구 안은 좁고 매캐한 연기로 가득합니다. 체력이 소모되었습니다.\n\n"
        "기어가다 보니 갈림길이 나옵니다. 무전기 소리가 들리는 오른쪽과 비상등이 보이는 왼쪽 중 어디로 가시겠습니까?"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📻 오른쪽 (무전기 소리)"):
            if "무전기" not in st.session_state.inventory:
                st.session_state.inventory.append("무전기")
            change_scene("radio_room")
            st.rerun()
    with col2:
        if st.button("💡 왼쪽 (비상등)"):
            change_scene("sub_dock")
            st.rerun()

elif current == "radio_room":
    st.subheader("📍 4. 통신실")
    st.write(
        "환기구를 빠져나오니 통신실입니다. 무전기에서 구조대의 목소리가 흘러나옵니다.\n\n"
        "\"여기는 구조대, 심해 연구소의 생존자가 있다면 옥상 헬리패드로 이동하십시오!\""
    )
    
    if st.button("🚁 옥상 헬리패드로 이동한다"):
        change_scene("helipad")
        st.rerun()
    if st.button("⚓ 안전하게 아래쪽 잠수정 선착장으로 이동한다"):
        change_scene("sub_dock")
        st.rerun()

elif current == "elevator":
    st.subheader("📍 4. 작동 중 멈춘 엘리베이터")
    st.write(
        "엘리베이터 버튼을 누르자 위로 올라가기 시작합니다... 하지만 1층에서 콰광 소리와 함께 정전되며 갇히고 맙니다.\n\n"
        "천장 해치가 약간 열려 있습니다."
    )
    if st.button("🧗‍♂️ 해치를 열고 로프를 타 올라간다"):
        change_scene("helipad")
        st.rerun()
    if st.button("⏳ 안에서 문을 강제로 열 때까지 기다린다"):
        change_scene("ending_trapped")
        st.rerun()

elif current == "sub_dock":
    st.subheader("📍 5. 잠수정 선착장")
    st.write(
        "구명 잠수정에 도달했습니다! 하지만 잠수정을 작동하려면 암호 잠금장치를 해제하거나 비상 전원을 켜야 합니다."
    )
    
    if "보안 카드키" in st.session_state.inventory:
        if st.button("💳 보안 카드키로 암호를 우회해 잠수정을 출항시킨다"):
            change_scene("ending_sub_escape")
            st.rerun()
    else:
        st.write("⚠️ 보안 카드키가 없어 자동 출항이 불가능합니다.")
        
    if st.button("⚡ 수동 비상 전원 레버를 당긴다"):
        change_scene("ending_explosion")
        st.rerun()

elif current == "helipad":
    st.subheader("📍 5. 폭풍우 치는 옥상 헬리패드")
    st.write(
        "옥상으로 나오자 강한 바람과 함께 헬리콥터가 접근합니다!\n\n"
        "하지만 추적해 온 괴물도 옥상 문을 부수고 따라 나왔습니다!"
    )
    
    if "무전기" in st.session_state.inventory:
        if st.button("📻 무전기로 위치를 알리고 헬기에 먼저 탑승한다"):
            change_scene("ending_hero_escape")
            st.rerun()
            
    if st.button("🏃‍♂️ 괴물을 유인하고 헬기 줄사다리로 뛰어내린다"):
        change_scene("ending_sacrificial")
        st.rerun()

elif current == "ending_caught":
    st.error("💀 [ENDING 1: 포식자의 먹잇감]")
    st.write("닫힌 게이트 앞에서 괴물에게 붙잡혔습니다. 아무도 당신의 비명을 듣지 못했습니다.")
    if st.button("🎮 다시 도전하기"):
        reset_game()
        st.rerun()

elif current == "ending_trapped":
    st.error("💀 [ENDING 2: 영원한 정적]")
    st.write("엘리베이터 안에서 구조를 기다렸지만, 심해의 수압을 견디지 못한 연구소가 침수되었습니다.")
    if st.button("🎮 다시 도전하기"):
        reset_game()
        st.rerun()

elif current == "ending_explosion":
    st.warning("💥 [ENDING 3: 화염 속의 탈출 실패]")
    st.write("비상 전원 레버를 당기자 가스 누출로 인해 대폭발이 일어났습니다.")
    if st.button("🎮 다시 도전하기"):
        reset_game()
        st.rerun()

elif current == "ending_sub_escape":
    st.success("🎉 [ENDING 4: 심해 침묵 탈출 (True Ending A)]")
    st.write("카드키로 성공적으로 잠수정을 작동시켜 수면 위로 무사히 탈출했습니다. 연구소의 비밀을 세상에 밝힐 수 있게 되었습니다!")
    if st.button("🎮 다시 도전하기"):
        reset_game()
        st.rerun()

elif current == "ending_hero_escape":
    st.success("🎉 [ENDING 5: 하늘에서의 구출 (True Ending B)]")
    st.write("무전기를 통해 정확한 타이밍에 헬기에 올라탔습니다. 옥상 위 괴물을 뒤로한 채 하늘로 탈출에 성공했습니다!")
    if st.button("🎮 다시 도전하기"):
        reset_game()
        st.rerun()

elif current == "ending_sacrificial":
    st.info("☠️ [ENDING 6: 아슬아슬한 추락]")
    st.write("헬기 사다리를 잡았으나, 괴물이 발목을 잡아 끌어내렸습니다. 함께 바다로 추락했습니다.")
    if st.button("🎮 다시 도전하기"):
        reset_game()
        st.rerun()