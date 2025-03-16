import os

import pandas as pd
import ast

#目前我把起始港口和终点港口相同定义为同一个航线,用selected_trips生成一个表,包含与航班同航线的所有航班
# 读取全量数据（明确Tab分隔）
data_folder = r"C:\Users\y7327\Documents\WeChat Files\wxid_sk5ejos2ggmv22\FileStorage\File\2025-03\data\data"
file_list = ["0_9.csv", "10_19.csv"]  # 需要合并的文件

# **读取并合并所有 CSV 文件**
df_list = []
for file in file_list:
    file_path = os.path.join(data_folder, file)
    df_temp = pd.read_csv(file_path, sep=",")
    df_temp.columns = df_temp.columns.str.strip()  # 清除列名空格
    df_list.append(df_temp)

# **合并数据**
df_full = pd.concat(df_list, ignore_index=True)
print("全量数据的列名：", df_full.columns.tolist())

# 读取随机选取的 3 行数据
selected_trips_path = "selected_trips.csv"
df_selected = pd.read_csv(selected_trips_path,sep=",")
df_selected.columns = df_selected.columns.str.strip()  # 清除列名两边的空格
print("随机选取数据的列名：", df_selected.columns.tolist())

# **检查 df_selected 的结构**
print("df_selected 前几行：\n", df_selected.head())

# 确保 'Start Port' 和 'End Port' 存在
if "Start Port" not in df_full.columns or "End Port" not in df_full.columns:
    print("错误: 'Start Port' 或 'End Port' 列不存在，检查分隔符或列名格式")
    exit()

# 处理匹配问题：去除空格、转换为字符串格式
df_full["Start Port"] = df_full["Start Port"].astype(str).str.strip()
df_full["End Port"] = df_full["End Port"].astype(str).str.strip()
df_selected["Start Port"] = df_selected["Start Port"].astype(str).str.strip()
df_selected["End Port"] = df_selected["End Port"].astype(str).str.strip()

# **检查 df_selected 的起止港口值**
print("df_selected['Start Port']:\n", df_selected["Start Port"])
print("df_selected['End Port']:\n", df_selected["End Port"])

# 遍历 df_selected 的每一行，根据起止港口筛选匹配的航班
for idx, row in df_selected.iterrows():
    # 解析 Start Port 和 End Port 字段（转换为字典）
    start_port_dict = ast.literal_eval(row['Start Port'])
    end_port_dict = ast.literal_eval(row['End Port'])

    # 只匹配 Main Port Name
    start_port_name = start_port_dict['Main Port Name']
    end_port_name = end_port_dict['Main Port Name']

    # **筛选全量数据**
    filtered = df_full[
        (df_full['Start Port'].str.contains(start_port_name, na=False)) &
        (df_full['End Port'].str.contains(end_port_name, na=False))
    ]

    # **保存 CSV 文件**
    output_file = rf"航线_{idx + 1}.csv"
    filtered.to_csv(output_file, sep=",", index=False)

    print(f"第 {idx + 1} 组：起始港口 = {start_port_name}，终点港口 = {end_port_name}，记录数 = {len(filtered)}，文件保存为：{output_file}")
