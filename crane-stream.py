import streamlit as st
import random

def initialize_game():
    """ゲームの初期化"""
    field = [(x, y) for x in range(1, 11) for y in range(1, 11)]
    pc_place = random.sample(field, 20)
    remain_field = list(set(field) - set(pc_place))
    pk_place = random.sample(remain_field, 15)
    remain_field = list(set(remain_field) - set(pk_place))
    rc_place = random.sample(remain_field, 15)

    keihinPlace = {pos: "ヒチュー" for pos in pc_place}
    keihinPlace.update({pos: "ヒカチュウ" for pos in pk_place})
    keihinPlace.update({pos: "ハイチュウ" for pos in rc_place})

    return {
        "syojiPrice": 1000,
        "getList": [],
        "keihinPlace": keihinPlace,
        "count": 0
    }

def win(i):
    """クレーンの動作エフェクト"""
    if i > 9:
        return "ウィ～～～ン"
    elif i > 6:
        return "ウィ～～ン"
    elif i > 3:
        return "ウィ～ン"
    elif i > 1:
        return "ウィン"
    else:
        return "ｳｨﾝ"

def sell(syojiPrice, getList):
    """景品を売る処理"""
    urine = {"ヒチュー": 200, "ヒカチュウ": 500, "ハイチュウ": 7}
    getMoney = sum(urine[item] for item in getList)
    new_price = syojiPrice + getMoney
    profit = new_price - 1000
    return new_price, getMoney, profit

# StreamlitのUI部分
st.title("クレーンゲーム")

# セッション状態の初期化
if "game" not in st.session_state:
    st.session_state.game = initialize_game()

game = st.session_state.game

st.write(f"### 所持金: {game['syojiPrice']}円")
st.write(f"### 獲得アイテム: {', '.join(game['getList']) if game['getList'] else 'なし'}")

if game["syojiPrice"] >= 100:
    if st.button("クレーンゲームをプレイする (100円)"):
        game["syojiPrice"] -= 100
        game["count"] += 1
        st.write(f"{game['count']}回目のプレイ！")
        
        x = st.number_input("右に何マス進みますか？", min_value=1, max_value=10, step=1)
        y = st.number_input("奥に何マス進みますか？", min_value=1, max_value=10, step=1)
        position = (x, y)
        
        st.write(win(x))
        st.write(win(y))

        if position in game["keihinPlace"]:
            st.write(f"クレーンは座標{position}に移動し、腕を降ろした…。")
            st.write("ウィ～～ン……ガシッ！")
            st.write(f"あなたは{game['keihinPlace'][position]}をゲットした！")
            game["getList"].append(game['keihinPlace'][position])
            del game["keihinPlace"][position]
        else:
            st.write(f"クレーンは座標{position}に移動し、腕を降ろした…。")
            st.write("ウィ～～ン……スカッ！")
            st.write("あなたは何も手に入れることが出来なかった…。")
else:
    st.write("所持金が足りません…。ゲームを終了します。")
    new_price, getMoney, profit = sell(game["syojiPrice"], game["getList"])
    st.write(f"売却価格: {getMoney}円")
    st.write(f"最終所持金: {new_price}円 ({'利益' if profit >= 0 else '損失'}: {abs(profit)}円)")
