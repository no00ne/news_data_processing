import pandas as pd
import numpy as np

# 读取全量数据（原文件为 , 分隔）
file_path = r"C:\Users\y7327\Documents\WeChat Files\wxid_sk5ejos2ggmv22\FileStorage\File\2025-03\data\data\0_9.csv"
df = pd.read_csv(file_path, delimiter=",")
print("全量数据行数：", len(df))

# 随机选择 3 行数据（如果每行代表一组航行信息）
selected_rows = np.random.choice(len(df), 3, replace=False)
new_df = df.iloc[selected_rows]

# 保存生成的 CSV 文件，使用 Tab 分隔符，保持格式一致
new_df.to_csv("selected_trips.csv", sep=",", index=False)

print("已成功生成新的表格，包含 3 行随机航行数据，文件名：selected_trips.csv")

