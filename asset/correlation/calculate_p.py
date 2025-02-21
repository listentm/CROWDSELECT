import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pdb
from scipy.stats import pearsonr  # 计算相关性和 p 值
from matplotlib.colors import LinearSegmentedColormap

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

    # 计算 p 值矩阵
    p_value_matrix = np.zeros_like(correlation_matrix)
    for row in range(len(df_numeric.columns)):
        for col in range(len(df_numeric.columns)):
            if row != col:
                try:
                    r, p = pearsonr(df_numeric.iloc[:, row], df_numeric.iloc[:, col])
                except Exception as e:
                    print(f"*****{sheet_name}")
                    print(f"Error in pearsonr at row {df_numeric.iloc[:, row]}, col {df_numeric.iloc[:, col]}: {e}")
                    #pdb.set_trace()
                p_value_matrix[row, col] = p
            else:
                p_value_matrix[row, col] = 1.0  # 自相关 p 值设为 1

    # 创建热力图
    sns.heatmap(
        correlation_matrix, annot=True, cmap=cmap, vmin=0, vmax=1,
        linewidths=0.5, square=True, ax=ax, fmt=".2f"
    )

    for row in range(len(df_numeric.columns)):
        for col in range(row + 1, len(df_numeric.columns)):  # 确保 p 值在右上角
            if not np.isnan(p_value_matrix[row, col]):
                ax.text(col + 0.5, row + 0.2, f"p={p_value_matrix[row, col]:.3f}",
                        ha='center', va='center', fontsize=8, color='red')

    # 设置标题
    ax.set_title(f"Correlation - {sheet_name}", fontsize=14, fontweight='bold')

    # 设置 x 和 y 轴标签
    ax.set_xticks(np.arange(4) + 0.5)
    ax.set_xticklabels(df.iloc[:4, 0], rotation=45, ha="right", fontsize=10)

    ax.set_yticks(np.arange(4) + 0.5)
    ax.set_yticklabels(df.iloc[:4, 0], rotation=0, fontsize=10)

# 调整布局，避免重叠
plt.tight_layout()

# 保存图表
plt.savefig("correlation_matrices_with_p_values.jpg", dpi=300, bbox_inches='tight')
plt.savefig("correlation_matrices_with_p_values.pdf", dpi=300, bbox_inches='tight')
plt.show()

print("所有相关性矩阵图已生成，p 值已显示！")
