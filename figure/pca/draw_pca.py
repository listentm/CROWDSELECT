import json
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
# 加载自定义字体
simhei_font_path = "../SimHei.ttf"
simhei_font = fm.FontProperties(fname=simhei_font_path)

MT_Bench_path = "mtbench_embedding.json"
arena_hard_path = "ah_embedding.json"

with open(MT_Bench_path, 'r') as f:
     mt_bench_embeddings = np.array(json.load(f))

with open(arena_hard_path, 'r') as f:
    arena_hard_embeddings = np.array(json.load(f))

# 合并数据用于 PCA 拟合
combined_embeddings = np.vstack([mt_bench_embeddings, arena_hard_embeddings])

# 执行 PCA
pca = PCA(n_components=2)
combined_pca = pca.fit_transform(combined_embeddings)

# 分离转换后的数据
mt_bench_pca = combined_pca[:len(mt_bench_embeddings)]
arena_hard_pca = combined_pca[len(mt_bench_embeddings):]

# 绘制散点图
plt.figure(figsize=(10, 8))
plt.scatter(mt_bench_pca[:, 0], mt_bench_pca[:, 1], alpha=0.6, label='MT-Bench', c='blue')
plt.scatter(arena_hard_pca[:, 0], arena_hard_pca[:, 1], alpha=0.6, label='Arena-Hard', c='red')


# plt.xlabel('First Principal Component', fontproperties=simhei_font, fontsize=22, fontweight='bold')
# plt.ylabel('Second Principal Component', fontproperties=simhei_font, fontsize=22, fontweight='bold')
plt.title('PCA Analysis of MT-Bench and Arena-Hard', fontproperties=simhei_font, fontsize=25, fontweight='bold')
plt.legend(fontsize=15)
plt.grid(True)
#
# # 添加方差解释率信息
# explained_var_ratio = pca.explained_variance_ratio_
# plt.text(0.02, 0.98,
# f'Explained variance ratio:\nPC1: {explained_var_ratio[0]:.3f}\nPC2: {explained_var_ratio[1]:.3f}',
# transform=plt.gca().transAxes,
# verticalalignment='top')

plt.tight_layout()
plt.savefig(f"pca.jpg", dpi=300, bbox_inches='tight')
plt.savefig(f"pca.pdf", dpi=300, bbox_inches='tight')
plt.show()