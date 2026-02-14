import streamlit as st
import sqlite3
import pandas as pd
import os  # 新增：处理路径和文件判断
from PIL import Image  # 新增：兼容图片加载

# -------------------------- 1. 初始化数据库（修改图片路径为相对路径） --------------------------
@st.cache_resource
def init_db():
    con = sqlite3.connect('dishes.db', check_same_thread=False)
    c = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS dishes (id INTEGER PRIMARY KEY,name TEXT UNIQUE,votes INTEGER DEFAULT '0',intro TEXT,image_url TEXT)")

    # 核心修改：图片路径改为【相对路径】，而非本地绝对路径
    default_dishes = [
        (
            "土豆炖牛腩",0,
            "牛腩软烂入味，土豆绵密吸汁，酱香浓郁，暖身下饭，经典家常硬菜越炖越香。",
            "resource/土豆炖牛腩.jpg"  # 相对路径：项目根目录/resource/图片名
        ),
        (
            "糖醋排骨",0,
            "色泽红亮，酸甜适口，排骨外酥里嫩，汁浓味美，经典开胃家常菜，大人小孩都爱吃。",
            "resource/糖醋排骨.jpg"
        ),
        (
            "干锅鸡翅虾",0,
            "鸡翅焦香、大虾鲜辣，麻香入味越吃越香，干香不腻，下酒又下饭。",
            "resource/干锅鸡翅虾.jpg"
        ),
        (
            "葱油手撕鸡",0,
            "皮滑肉嫩，葱香浓郁，鲜香不腻，清爽入味，简单又好吃的家常凉菜。",
            "resource/葱油手撕鸡.jpg"
        ),
        (
            "红烧鸡",0,
            "鸡肉软烂入味，酱香浓郁不柴，汤汁浓稠下饭，家常做法简单又香。",
            "resource/红烧鸡.jpg"
        ),
        (
            "白切鸡",0,
            "无需多言",
            "resource/白切鸡.jpg"
        ),
        (
            "花开富贵",0,
            "冬瓜清甜软嫩，肉馅鲜香多汁，清淡不腻，蒸制健康又入味，老少皆宜。",
            "resource/冬瓜酿肉.jpg"
        ),
        (
            "白灼生菜",0,
            "翠绿生菜快速焯烫，淋上豉油热油，“啫啫”声中香气四溢。口感爽脆，味道清鲜，是粤菜里“清爽不寡淡”的经典代表",
            "resource/生菜.jpg"
        ),
        (
            "醋溜白菜",0,
            "脆嫩爽口，酸甜微辣，热锅快炒，酸香开胃，家常快手素菜，下饭一绝。",
            "resource/醋溜白菜.jpg"
        ),
        (
            "白菜豆腐煲",0,
            "慢炖出鲜醇滋味，白菜软甜、豆腐滑嫩，暖乎乎一锅，清淡又治愈。",
            "resource/白菜豆腐煲.jpg"
        ),
        (
            "白灼西兰花",0,
            "清淡少油，脆嫩爽口，淋上酱汁鲜香解腻，简单又健康。",
            "resource/白灼西兰花.jpg"
        ),
        (
            "炒合菜",0,
            "多种鲜蔬同锅快炒，色彩鲜亮口感丰富，咸香适口，家常快手好菜。",
            "resource/炒合菜.jpg"
        ),
        (
            "葱烧豆腐",0,
            "葱段煸出焦香，豆腐煎至金黄，吸饱酱汁软嫩入味，家常小炒也能香到舔盘。",
            "resource/葱烧豆腐.jpg"
        ),
        (
            "菠菜蒸蛋",0,
            "蛋羹滑嫩如布丁，菠菜鲜软清甜，清淡少油、温润养胃，老少皆宜的家常软嫩菜。",
            "resource/菠菜蒸蛋.jpg"
        ),
        (
            "青椒炒蛋",0,
            "鲜椒爽脆微辣，鸡蛋蓬松鲜香，简单快手，香气扑鼻，下饭又解馋。",
            "resource/青椒炒蛋.jpg"
        ),
        (
            "素菜菌菇汤",0,
            "鲜菌慢煮出清甜，汤清味鲜，温润不腻，喝完整个人都舒服。",
            "resource/素菜菌菇汤.jpg"
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

con = init_db()

# -------------------------- 2. 核心功能函数（保留原有逻辑） --------------------------
def vote_dish(dish_id):
    c = con.cursor()
    c.execute(
        "UPDATE dishes SET votes = votes+1 WHERE id=?",
        (dish_id,)
    )
    con.commit()
    return True

def vote_back(dish_id):
    c = con.cursor()
    c.execute(
        "UPDATE dishes SET votes =  CASE WHEN votes > 0 THEN votes-1 ELSE 0 END WHERE id=?",
        (dish_id,)
    )
    con.commit()
    return True

def get_dishes_sorted():
    """查询所有菜品，按票数降序排列（从高到低）"""
    return pd.read_sql_query(
        "SELECT * FROM dishes ORDER BY votes DESC",
        con
    )

# -------------------------- 3. 页面配置 + 图片显示优化 --------------------------
st.set_page_config(
    page_title="年夜团圆饭",
    page_icon="",  
    layout="wide"
)

# 新增：安全加载图片的函数（兼容本地+公网）
def safe_load_image(image_path, width=200):
    """
    安全加载图片：优先加载本地相对路径，失败则显示占位图
    """
    # 拼接完整路径（兼容不同环境）
    full_path = os.path.join(os.getcwd(), image_path)
    try:
        # 先尝试用PIL打开（更稳定）
        img = Image.open(full_path)
        st.image(img, width=width)
    except:
        # 失败则显示占位图
        st.image("https://via.placeholder.com/200x200?text=暂无图片", width=width)

# -------------------------- 4. 页面展示逻辑 --------------------------
st.title(" 年夜团圆饭")
st.header("此乃人间烟火色，且以美食慰风尘")
st.subheader("\n")
dishes_df = get_dishes_sorted()

if not dishes_df.empty:
    for _, dish in dishes_df.iterrows():
        col1, col2, col3, col4 = st.columns([2, 5, 1, 1])
        with col1:
            # 调用安全加载图片函数（核心修改）
            safe_load_image(dish["image_url"], width=200)
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
if st.button("🔁 重置所有票数"):  # 补充按钮文字，更清晰
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