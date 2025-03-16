import pandas as pd
import glob
import os
import ast
import re

# 读取新闻数据
news_file = "news-process.csv"
df_news = pd.read_csv(news_file)
df_news["assets"] = df_news["assets"].astype(str)

# 获取所有航班文件
flight_files = glob.glob("航线_*.csv")

for flight_file in flight_files:
    # 读取航班数据
    df_flight = pd.read_csv(flight_file)

    # 提取所有唯一船名（去重+去空）
    ship_names = df_flight["Name"].dropna().unique().tolist()

    # 解析港口信息
    start_port_dict = ast.literal_eval(df_flight["Start Port"].iloc[0])
    end_port_dict = ast.literal_eval(df_flight["End Port"].iloc[0])
    start_port_name = start_port_dict.get("Main Port Name", "")
    end_port_name = end_port_dict.get("Main Port Name", "")

    print(f"处理 {flight_file}: 船名列表 = {ship_names}, 起始港口 = {start_port_name}, 终点港口 = {end_port_name}")

    # ================== 船名相关新闻处理 ==================
    if not ship_names:
        ship_news = pd.DataFrame(columns=df_news.columns)
    else:
        # 使用简单匹配模式（移除单词边界）
        pattern = '|'.join(map(re.escape, ship_names))
        mask = df_news["assets"].str.contains(
            pattern,
            case=False,  # 不区分大小写
            regex=True,
            na=False
        )
        ship_news = df_news[mask].drop_duplicates(subset=["assets"])


    # ================== 港口相关新闻处理 ==================
    # 定义通用匹配函数
    def create_port_mask(port_name):
        if not port_name: return pd.Series(False, index=df_news.index)
        return df_news["assets"].str.contains(
            re.escape(port_name),
            case=False,
            regex=True,
            na=False
        )


    start_port_news = df_news[create_port_mask(start_port_name)]
    end_port_news = df_news[create_port_mask(end_port_name)]

    # 生成文件名并保存
    flight_id = os.path.splitext(os.path.basename(flight_file))[0].split("_")[-1]
    ship_news_file = f"ship_news_{flight_id}.csv"
    start_port_news_file = f"start_port_news_{flight_id}.csv"
    end_port_news_file = f"end_port_news_{flight_id}.csv"

    ship_news.to_csv(ship_news_file, index=False)
    start_port_news.to_csv(start_port_news_file, index=False)
    end_port_news.to_csv(end_port_news_file, index=False)

    print(f"  -> 船相关新闻保存: {ship_news_file} ({len(ship_news)} 条)")
    print(f"  -> 起始港相关新闻保存: {start_port_news_file} ({len(start_port_news)} 条)")
    print(f"  -> 终点港相关新闻保存: {end_port_news_file} ({len(end_port_news)} 条)")

print("所有航班处理完毕！")