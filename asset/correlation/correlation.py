import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pdb

from matplotlib.colors import LinearSegmentedColormap
import re

# 读取 Excel 文件
cleaned_file_path = "correlation_clean.xlsx"
xls = pd.ExcelFile(cleaned_file_path)

# 创建自定义渐变色（0 → #FBF9FA，1 → #507AAF）
cmap = LinearSegmentedColormap.from_list("custom_blue", ["#FBF9FA", "#507AAF"])

# 创建 2×2 子图布局
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
# 遍历每个子表
for i, sheet_name in enumerate(xls.sheet_names[:4]):  # 取前 4 个 sheet（2x2 布局）
    ax = axes[i // 2, i % 2]  # 计算子图位置
    df = pd.read_excel(xls, sheet_name=sheet_name)
    # 选取前 4 行进行相关性计算
    df_numeric = df.iloc[:4, 1:].apply(pd.to_numeric, errors='coerce').T

    # 计算相关性矩阵（4x4）
    correlation_matrix = df_numeric.corr()

    # 画热力图（自定义渐变色）
    sns.heatmap(
        correlation_matrix, annot=True, cmap=cmap, vmin=0, vmax=1, linewidths=0.5, square=True, ax=ax
    )

    # 设置标题
    ax.set_title(f"Correlation - {sheet_name}", fontsize=14, fontweight='bold')
    # 设置 y 轴标签旋转为 0 度
    ax.set_yticklabels(df.iloc[:4, 0], rotation=0, fontsize=10)
    # 设置 x 和 y 轴标签
    ax.set_xticks(np.arange(4) + 0.5)
    ax.set_xticklabels(df.iloc[:4, 0], rotation=45, ha="right", fontsize=10)

    ax.set_yticks(np.arange(4) + 0.5)
    ax.set_yticklabels(df.iloc[:4, 0], rotation=0, fontsize=10)

# 调整布局，避免重叠
plt.tight_layout()

# 保存总图
plt.savefig("correlation_matrices.jpg", dpi=300, bbox_inches='tight')
plt.savefig("correlation_matrices.pdf", dpi=300, bbox_inches='tight')
plt.show()

print("所有相关性矩阵图已生成！")
