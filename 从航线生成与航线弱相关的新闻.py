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

# 定义搜索函数（保持原有逻辑）
def contains_keyword(row, keyword):
    return row.astype(str).str.contains(keyword, case=False, na=False).any()

for flight_file in flight_files:
    # 读取航班数据
    df_flight = pd.read_csv(flight_file)

    # 提取所有唯一船名（新增逻辑）
    ship_names = df_flight["Name"].dropna().unique().tolist()

    # 解析港口信息（保持原有逻辑）
    start_port_dict = ast.literal_eval(df_flight["Start Port"].iloc[0])
    end_port_dict = ast.literal_eval(df_flight["End Port"].iloc[0])
    start_port_name = start_port_dict.get("Main Port Name", "")
    end_port_name = end_port_dict.get("Main Port Name", "")

    print(f"处理 {flight_file}: 船名列表 = {ship_names}, 起始港口 = {start_port_name}, 终点港口 = {end_port_name}")

    # ================== 船名相关新闻处理 ==================
    if not ship_names:
        ship_news = pd.DataFrame(columns=df_news.columns)  # 空数据框
    else:
        # 生成正则表达式模式（新增逻辑）
        pattern = '|'.join(map(re.escape, ship_names))
        # 创建掩码检查所有列（优化逻辑）
        mask = df_news.astype(str).apply(
            lambda col: col.str.contains(pattern, case=False, regex=True, na=False)
        ).any(axis=1)
        ship_news = df_news[mask].drop_duplicates()

    # ================== 港口相关新闻处理 ==================
    # 起始港口（保持原有逻辑）
    start_port_mask = df_news.apply(
        lambda row: contains_keyword(row, start_port_name), axis=1
    )
    start_port_news = df_news[start_port_mask]

    # 终点港口（保持原有逻辑）
    end_port_mask = df_news.apply(
        lambda row: contains_keyword(row, end_port_name), axis=1
    )
    end_port_news = df_news[end_port_mask]

    # 生成文件名并保存（保持原有逻辑）
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
