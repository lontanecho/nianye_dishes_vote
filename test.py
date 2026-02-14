import streamlit as st
import sqlite3
import pandas as pd
import os

@st.cache_resource
def init_db():
    con=sqlite3.connect('dishes.db',check_same_thread=False)
    c=con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS dishes (id INTEGER PRIMARY KEY,name TEXT UNIQUE,votes INTEGER DEFAULT '0',intro TEXT,image_url TEXT)")

    default_dishes=[
        (
            "土豆炖牛腩",0,
            "牛腩软烂入味，土豆绵密吸汁，酱香浓郁，暖身下饭，经典家常硬菜越炖越香。",
            "d:/vscode/code/test_streamlit/resource/土豆炖牛腩.jpg"
        ),
        (
            "糖醋排骨",0,
            "色泽红亮，酸甜适口，排骨外酥里嫩，汁浓味美，经典开胃家常菜，大人小孩都爱吃。",
            "d:/vscode/code/test_streamlit/resource/糖醋排骨.jpg"
        ),
        (
            "干锅鸡翅虾",0,
            "鸡翅焦香、大虾鲜辣，麻香入味越吃越香，干香不腻，下酒又下饭。",
            "d:/vscode/code/test_streamlit/resource/干锅鸡翅虾.jpg"
        ),
        (
            "葱油手撕鸡",0,
            "皮滑肉嫩，葱香浓郁，鲜香不腻，清爽入味，简单又好吃的家常凉菜。",
            "d:/vscode/code/test_streamlit/resource/葱油手撕鸡.jpg"
        ),
        (
            "红烧鸡",0,
            "鸡肉软烂入味，酱香浓郁不柴，汤汁浓稠下饭，家常做法简单又香。",
            "d:/vscode/code/test_streamlit/resource/红烧鸡.jpg"
        ),
        (
            "白切鸡",0,
            "无需多言",
            "d:/vscode/code/test_streamlit/resource/白切鸡.jpg"
        ),
        (
            "花开富贵",0,
            "冬瓜清甜软嫩，肉馅鲜香多汁，清淡不腻，蒸制健康又入味，老少皆宜。",
            "d:/vscode/code/test_streamlit/resource/冬瓜酿肉.jpg"
        ),
        (
            "白灼生菜",0,
            "翠绿生菜快速焯烫，淋上豉油热油，“啫啫”声中香气四溢。口感爽脆，味道清鲜，是粤菜里“清爽不寡淡”的经典代表",
            "d:/vscode/code/test_streamlit/resource/生菜.jpg"
        ),
        (
            "醋溜白菜",0,
            "脆嫩爽口，酸甜微辣，热锅快炒，酸香开胃，家常快手素菜，下饭一绝。",
            "d:/vscode/code/test_streamlit/resource/醋溜白菜.jpg"
        ),
        (
            "白菜豆腐煲",0,
            "慢炖出鲜醇滋味，白菜软甜、豆腐滑嫩，暖乎乎一锅，清淡又治愈。",
            "d:/vscode/code/test_streamlit/resource/白菜豆腐煲.jpg"
        ),
        (
            "白灼西兰花",0,
            "清淡少油，脆嫩爽口，淋上酱汁鲜香解腻，简单又健康。",
            "d:/vscode/code/test_streamlit/resource/白灼西兰花.jpg"
        ),
        (
            "炒合菜",0,
            "多种鲜蔬同锅快炒，色彩鲜亮口感丰富，咸香适口，家常快手好菜。",
            "d:/vscode/code/test_streamlit/resource/炒合菜.jpg"
        ),
        (
            "葱烧豆腐",0,
            "葱段煸出焦香，豆腐煎至金黄，吸饱酱汁软嫩入味，家常小炒也能香到舔盘。",
            "d:/vscode/code/test_streamlit/resource/葱烧豆腐.jpg"
        ),
        (
            "菠菜蒸蛋",0,
            "蛋羹滑嫩如布丁，菠菜鲜软清甜，清淡少油、温润养胃，老少皆宜的家常软嫩菜。",
            "d:/vscode/code/test_streamlit/resource/菠菜蒸蛋.jpg"
        ),
        (
            "青椒炒蛋",0,
            "鲜椒爽脆微辣，鸡蛋蓬松鲜香，简单快手，香气扑鼻，下饭又解馋。",
            "d:/vscode/code/test_streamlit/resource/青椒炒蛋.jpg"
        ),
        (
            "素菜菌菇汤",0,
            "鲜菌慢煮出清甜，汤清味鲜，温润不腻，喝完整个人都舒服。",
            "d:/vscode/code/test_streamlit/resource/素菜菌菇汤.jpg"
        )
    ]

    for dish in default_dishes:
        try:
            c.execute(
                "INSERT INTO dishes(name,votes,intro,image_url)VALUES(?,?,?,?)",
                dish
            )
        except sqlite3.IntegrityError:
            pass
    
    con.commit()
    return con

con=init_db()

def vote_dish(dish_id):
    c=con.cursor()
    c.execute(
        "UPDATE dishes SET votes = votes+1 WHERE id=?",
        (dish_id,)
        )
    con.commit()
    return True

def vote_back(dish_id):
    c=con.cursor()
    c.execute(
        "UPDATE dishes SET votes =  CASE WHEN votes > 0 THEN votes-1 ELSE 0 END WHERE id=?",
        (dish_id,)
        )
    con.commit()
    return True

def get_dishes_sorted():
    """查询所有菜品，按票数降序排列（从高到低）"""
    return pd.read_sql_query(
        "SELECT * FROM dishes ORDER BY votes DESC",  # DESC = 降序（从多到少）
        con # 数据库连接
    )

st.set_page_config(
    page_title="年夜团圆饭",  # 浏览器标签页标题
    page_icon="",  # 标签页图标（emoji/图片URL）
    layout="wide"  # 宽屏布局（适配大屏展示）
)

st.title("年夜团圆饭")
st.header("此乃人间烟火色，且以美食慰风尘")
st.subheader("\n")
dishes_df = get_dishes_sorted()

if not dishes_df.empty:
    for _, dish in dishes_df.iterrows():
        col1, col2, col3,col4= st.columns([2, 5, 1,1])
        with col1:
            # 图片不存在时显示占位图
            try:
                st.image(dish["image_url"], width=200)
            except:
                st.image("https://via.placeholder.com/100x80?text=暂无图片", width=200)
        with col2:
            st.subheader(dish["name"])
            st.write(f"简介：{dish['intro'] if dish['intro'] else '暂无介绍'}")
            st.metric("心动值", dish["votes"])
        with col3:
            if st.button("想吃😍 ", key=f"vote_up{dish['id']}"):
                if vote_dish(dish["id"]):
                    st.success(f"成功为【{dish['name']}】投票！")
                    st.rerun()
        with col4:
            if st.button("算喽🙃", key=f"vote_down{dish['id']}"):
                if vote_back(dish["id"]):
                    st.success(f"成功为【{dish['name']}】撤票！")
                    st.rerun()
else:
    st.warning("暂无菜品数据！")

st.divider()
st.subheader("⚙️ 管理员操作")

reset_pwd = st.text_input("输入密码", type="password")
if st.button("🔁 "):
    if reset_pwd == "1123":  
        try:
            c = con.cursor()
            c.execute("UPDATE dishes SET votes = 0")
            con.commit()
            st.success("✅ 所有票数已成功重置为 0！")
            st.rerun()
        except Exception as e:
            st.error(f"重置失败：{e}")
    else:
        st.error("❌ 密码错误，无法重置！")