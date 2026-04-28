# Rime 评测结果

- 生成时间: 2026-04-28 23:09:57 +08:00
- 来源文件: `benchmark_all_corpus_20260428T150845237660Z_report.txt`

## Vendor 子模块版本

- `vendor/rime-frost`: `6e8449d7c2e89d738ce41ddd35d9ef6814bdc6e4`
- `vendor/rime-ice`: `2bd2983c6c74ea49b3a013f150ade7f3b8a27515`
- `vendor/rime_wanxiang` (`wanxiang`): `89f2daa58f8b10afa1d25ff86ddeb283231afa70`
- `vendor/rime-wubi-sentence`: `c3b26af601e41de49227f86633df00985e8d8a77`

## 评测摘要

```text
========================================================================
Rime 多方案整句评测 — 摘要报告
========================================================================
生成时间 (UTC): 20260428T150845237660Z
rime.dll: D:\vscode\rime_projs\rime-schema-compare\lib\rime.dll
模式: 全部语料 (data/corpus/*.txt)

语料文件:
  - news: D:\vscode\rime_projs\rime-schema-compare\data\corpus\news.txt
  - novel: D:\vscode\rime_projs\rime-schema-compare\data\corpus\novel.txt
  - prose: D:\vscode\rime_projs\rime-schema-compare\data\corpus\prose.txt
  - tech: D:\vscode\rime_projs\rime-schema-compare\data\corpus\tech.txt
  - test: D:\vscode\rime_projs\rime-schema-compare\data\corpus\test.txt

【总体】
  [mingyuepinyin]
    句子正确率: 42.35%  (108/255 句完全匹配)
    文字正确率: 84.13%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.19%

  [mingyuepinyin_with_gram]
    句子正确率: 35.69%  (91/255 句完全匹配)
    文字正确率: 82.38%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 81.75%

  [rime_ice]
    句子正确率: 45.49%  (116/255 句完全匹配)
    文字正确率: 85.63%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 85.19%

  [rime_ice_with_gram]
    句子正确率: 52.55%  (134/255 句完全匹配)
    文字正确率: 88.14%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 87.96%

  [rime_frost]
    句子正确率: 50.2%  (128/255 句完全匹配)
    文字正确率: 87.33%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 86.77%

  [rime_frost_with_gram]
    句子正确率: 60.39%  (154/255 句完全匹配)
    文字正确率: 90.3%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.93%

  [wanxiang]
    句子正确率: 50.2%  (128/255 句完全匹配)
    文字正确率: 86.64%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 86.14%

  [rime_wanxiang_with_gram]
    句子正确率: 56.08%  (143/255 句完全匹配)
    文字正确率: 88.51%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 88.2%

  [rime_wubi_sentens_wubi86]
    句子正确率: 47.84%  (122/255 句完全匹配)
    文字正确率: 88.31%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 88.24%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 58.43%  (149/255 句完全匹配)
    文字正确率: 91.84%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 90.99%

------------------------------------------------------------------------
【语料: news】
  [mingyuepinyin]
    句子正确率: 44.93%  (31/69 句完全匹配)
    文字正确率: 88.64%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 88.29%

  [mingyuepinyin_with_gram]
    句子正确率: 40.58%  (28/69 句完全匹配)
    文字正确率: 85.37%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.51%

  [rime_ice]
    句子正确率: 55.07%  (38/69 句完全匹配)
    文字正确率: 91.62%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.96%

  [rime_ice_with_gram]
    句子正确率: 49.28%  (34/69 句完全匹配)
    文字正确率: 89.77%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.14%

  [rime_frost]
    句子正确率: 65.22%  (45/69 句完全匹配)
    文字正确率: 94.6%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.78%

  [rime_frost_with_gram]
    句子正确率: 66.67%  (46/69 句完全匹配)
    文字正确率: 93.89%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.54%

  [wanxiang]
    句子正确率: 66.67%  (46/69 句完全匹配)
    文字正确率: 94.18%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.01%

  [rime_wanxiang_with_gram]
    句子正确率: 62.32%  (43/69 句完全匹配)
    文字正确率: 92.61%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.78%

  [rime_wubi_sentens_wubi86]
    句子正确率: 57.97%  (40/69 句完全匹配)
    文字正确率: 91.9%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.56%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 69.57%  (48/69 句完全匹配)
    文字正确率: 95.6%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.35%

------------------------------------------------------------------------
【语料: novel】
  [mingyuepinyin]
    句子正确率: 32.56%  (14/43 句完全匹配)
    文字正确率: 79.53%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 79.13%

  [mingyuepinyin_with_gram]
    句子正确率: 25.58%  (11/43 句完全匹配)
    文字正确率: 78.35%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 77.51%

  [rime_ice]
    句子正确率: 30.23%  (13/43 句完全匹配)
    文字正确率: 82.12%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 81.92%

  [rime_ice_with_gram]
    句子正确率: 46.51%  (20/43 句完全匹配)
    文字正确率: 84.94%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 85.8%

  [rime_frost]
    句子正确率: 34.88%  (15/43 句完全匹配)
    文字正确率: 82.35%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 81.98%

  [rime_frost_with_gram]
    句子正确率: 51.16%  (22/43 句完全匹配)
    文字正确率: 86.12%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 86.62%

  [wanxiang]
    句子正确率: 37.21%  (16/43 句完全匹配)
    文字正确率: 80.24%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 80.53%

  [rime_wanxiang_with_gram]
    句子正确率: 41.86%  (18/43 句完全匹配)
    文字正确率: 81.18%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 82.57%

  [rime_wubi_sentens_wubi86]
    句子正确率: 37.21%  (16/43 句完全匹配)
    文字正确率: 87.76%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 88.28%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 46.51%  (20/43 句完全匹配)
    文字正确率: 89.41%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.49%

------------------------------------------------------------------------
【语料: prose】
  [mingyuepinyin]
    句子正确率: 40.0%  (42/105 句完全匹配)
    文字正确率: 80.54%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 80.71%

  [mingyuepinyin_with_gram]
    句子正确率: 34.29%  (36/105 句完全匹配)
    文字正确率: 80.0%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 79.36%

  [rime_ice]
    句子正确率: 40.0%  (42/105 句完全匹配)
    文字正确率: 80.97%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 79.92%

  [rime_ice_with_gram]
    句子正确率: 50.48%  (53/105 句完全匹配)
    文字正确率: 85.81%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 85.48%

  [rime_frost]
    句子正确率: 40.0%  (42/105 句完全匹配)
    文字正确率: 81.51%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 80.76%

  [rime_frost_with_gram]
    句子正确率: 54.29%  (57/105 句完全匹配)
    文字正确率: 86.67%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 86.41%

  [wanxiang]
    句子正确率: 41.9%  (44/105 句完全匹配)
    文字正确率: 81.83%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 81.13%

  [rime_wanxiang_with_gram]
    句子正确率: 49.52%  (52/105 句完全匹配)
    文字正确率: 84.84%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.66%

  [rime_wubi_sentens_wubi86]
    句子正确率: 40.0%  (42/105 句完全匹配)
    文字正确率: 83.87%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 83.4%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 47.62%  (50/105 句完全匹配)
    文字正确率: 88.06%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 86.62%

------------------------------------------------------------------------
【语料: tech】
  [mingyuepinyin]
    句子正确率: 57.58%  (19/33 句完全匹配)
    文字正确率: 88.92%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.97%

  [mingyuepinyin_with_gram]
    句子正确率: 39.39%  (13/33 句完全匹配)
    文字正确率: 86.01%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 87.26%

  [rime_ice]
    句子正确率: 63.64%  (21/33 句完全匹配)
    文字正确率: 90.38%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.65%

  [rime_ice_with_gram]
    句子正确率: 66.67%  (22/33 句完全匹配)
    文字正确率: 93.0%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.37%

  [rime_frost]
    句子正确率: 69.7%  (23/33 句完全匹配)
    文字正确率: 93.59%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.69%

  [rime_frost_with_gram]
    句子正确率: 72.73%  (24/33 句完全匹配)
    文字正确率: 96.21%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.4%

  [wanxiang]
    句子正确率: 54.55%  (18/33 句完全匹配)
    文字正确率: 90.09%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.07%

  [rime_wanxiang_with_gram]
    句子正确率: 75.76%  (25/33 句完全匹配)
    文字正确率: 97.08%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.5%

  [rime_wubi_sentens_wubi86]
    句子正确率: 69.7%  (23/33 句完全匹配)
    文字正确率: 94.46%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.33%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 81.82%  (27/33 句完全匹配)
    文字正确率: 96.5%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.69%

------------------------------------------------------------------------
【语料: test】
  [mingyuepinyin]
    句子正确率: 40.0%  (2/5 句完全匹配)
    文字正确率: 91.8%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.89%

  [mingyuepinyin_with_gram]
    句子正确率: 60.0%  (3/5 句完全匹配)
    文字正确率: 91.8%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.12%

  [rime_ice]
    句子正确率: 40.0%  (2/5 句完全匹配)
    文字正确率: 85.25%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 81.13%

  [rime_ice_with_gram]
    句子正确率: 100.0%  (5/5 句完全匹配)
    文字正确率: 100.0%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 100.0%

  [rime_frost]
    句子正确率: 60.0%  (3/5 句完全匹配)
    文字正确率: 91.8%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.36%

  [rime_frost_with_gram]
    句子正确率: 100.0%  (5/5 句完全匹配)
    文字正确率: 100.0%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 100.0%

  [wanxiang]
    句子正确率: 80.0%  (4/5 句完全匹配)
    文字正确率: 98.36%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 98.33%

  [rime_wanxiang_with_gram]
    句子正确率: 100.0%  (5/5 句完全匹配)
    文字正确率: 100.0%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 100.0%

  [rime_wubi_sentens_wubi86]
    句子正确率: 20.0%  (1/5 句完全匹配)
    文字正确率: 83.61%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 83.11%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 80.0%  (4/5 句完全匹配)
    文字正确率: 96.72%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.89%

========================================================================
【总耗时】全流程墙钟约 71856.78 ms（多语料）

【各语料耗时】
  · news
    读取文件: 0.21 ms
    分句: 0.5 ms
    预过滤: 0.93 ms
    [mingyuepinyin] 输入串: 3.65 ms, librime 加载: 344.01 ms, 开会话+选方案: 37.96 ms, 逐句解码: 137.79 ms
    [mingyuepinyin_with_gram] 输入串: 4.12 ms, librime 加载: 331.35 ms, 开会话+选方案: 27.32 ms, 逐句解码: 160.41 ms
    [rime_frost] 输入串: 4.2 ms, librime 加载: 1112.81 ms, 开会话+选方案: 64.78 ms, 逐句解码: 330.76 ms
    [rime_frost_with_gram] 输入串: 3.93 ms, librime 加载: 1070.36 ms, 开会话+选方案: 25.89 ms, 逐句解码: 329.61 ms
    [rime_ice] 输入串: 3.78 ms, librime 加载: 1093.85 ms, 开会话+选方案: 29.33 ms, 逐句解码: 151.69 ms
    [rime_ice_with_gram] 输入串: 4.23 ms, librime 加载: 1081.27 ms, 开会话+选方案: 26.82 ms, 逐句解码: 193.66 ms
    [rime_wanxiang_with_gram] 输入串: 5.78 ms, librime 加载: 377.85 ms, 开会话+选方案: 1299.94 ms, 逐句解码: 1165.39 ms
    [rime_wubi_sentens_wubi86] 输入串: 83.64 ms, librime 加载: 840.34 ms, 开会话+选方案: 404.75 ms, 逐句解码: 273.03 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 84.68 ms, librime 加载: 817.42 ms, 开会话+选方案: 421.09 ms, 逐句解码: 231.98 ms
    [wanxiang] 输入串: 3.61 ms, librime 加载: 378.3 ms, 开会话+选方案: 1275.14 ms, 逐句解码: 1165.27 ms
  · novel
    读取文件: 0.19 ms
    分句: 0.15 ms
    预过滤: 0.13 ms
    [mingyuepinyin] 输入串: 2.25 ms, librime 加载: 370.29 ms, 开会话+选方案: 25.26 ms, 逐句解码: 92.96 ms
    [mingyuepinyin_with_gram] 输入串: 2.28 ms, librime 加载: 343.02 ms, 开会话+选方案: 19.89 ms, 逐句解码: 129.06 ms
    [rime_frost] 输入串: 3.53 ms, librime 加载: 1120.35 ms, 开会话+选方案: 45.01 ms, 逐句解码: 229.02 ms
    [rime_frost_with_gram] 输入串: 2.67 ms, librime 加载: 1090.41 ms, 开会话+选方案: 28.04 ms, 逐句解码: 247.56 ms
    [rime_ice] 输入串: 4.82 ms, librime 加载: 1100.68 ms, 开会话+选方案: 26.51 ms, 逐句解码: 139.76 ms
    [rime_ice_with_gram] 输入串: 2.33 ms, librime 加载: 1041.36 ms, 开会话+选方案: 28.59 ms, 逐句解码: 162.7 ms
    [rime_wanxiang_with_gram] 输入串: 2.85 ms, librime 加载: 355.47 ms, 开会话+选方案: 1332.62 ms, 逐句解码: 893.5 ms
    [rime_wubi_sentens_wubi86] 输入串: 9.49 ms, librime 加载: 847.14 ms, 开会话+选方案: 407.03 ms, 逐句解码: 139.85 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 6.95 ms, librime 加载: 810.96 ms, 开会话+选方案: 380.94 ms, 逐句解码: 144.95 ms
    [wanxiang] 输入串: 2.49 ms, librime 加载: 366.12 ms, 开会话+选方案: 1377.93 ms, 逐句解码: 900.75 ms
  · prose
    读取文件: 0.14 ms
    分句: 0.24 ms
    预过滤: 0.2 ms
    [mingyuepinyin] 输入串: 5.07 ms, librime 加载: 333.6 ms, 开会话+选方案: 52.51 ms, 逐句解码: 188.91 ms
    [mingyuepinyin_with_gram] 输入串: 5.87 ms, librime 加载: 334.85 ms, 开会话+选方案: 36.38 ms, 逐句解码: 269.16 ms
    [rime_frost] 输入串: 5.41 ms, librime 加载: 1114.72 ms, 开会话+选方案: 35.28 ms, 逐句解码: 471.8 ms
    [rime_frost_with_gram] 输入串: 4.98 ms, librime 加载: 1089.36 ms, 开会话+选方案: 24.94 ms, 逐句解码: 480.29 ms
    [rime_ice] 输入串: 5.25 ms, librime 加载: 1101.71 ms, 开会话+选方案: 33.06 ms, 逐句解码: 219.14 ms
    [rime_ice_with_gram] 输入串: 4.93 ms, librime 加载: 1070.97 ms, 开会话+选方案: 29.04 ms, 逐句解码: 243.63 ms
    [rime_wanxiang_with_gram] 输入串: 5.01 ms, librime 加载: 381.39 ms, 开会话+选方案: 1276.44 ms, 逐句解码: 1802.98 ms
    [rime_wubi_sentens_wubi86] 输入串: 17.39 ms, librime 加载: 836.95 ms, 开会话+选方案: 379.74 ms, 逐句解码: 274.2 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 16.33 ms, librime 加载: 811.31 ms, 开会话+选方案: 384.6 ms, 逐句解码: 297.91 ms
    [wanxiang] 输入串: 4.84 ms, librime 加载: 378.98 ms, 开会话+选方案: 1288.05 ms, 逐句解码: 1813.67 ms
  · tech
    读取文件: 0.14 ms
    分句: 0.3 ms
    预过滤: 0.12 ms
    [mingyuepinyin] 输入串: 2.0 ms, librime 加载: 376.98 ms, 开会话+选方案: 32.51 ms, 逐句解码: 73.52 ms
    [mingyuepinyin_with_gram] 输入串: 2.02 ms, librime 加载: 353.54 ms, 开会话+选方案: 33.37 ms, 逐句解码: 96.75 ms
    [rime_frost] 输入串: 1.81 ms, librime 加载: 1082.2 ms, 开会话+选方案: 45.69 ms, 逐句解码: 178.25 ms
    [rime_frost_with_gram] 输入串: 1.88 ms, librime 加载: 1060.66 ms, 开会话+选方案: 28.85 ms, 逐句解码: 187.48 ms
    [rime_ice] 输入串: 2.03 ms, librime 加载: 1070.62 ms, 开会话+选方案: 25.08 ms, 逐句解码: 87.18 ms
    [rime_ice_with_gram] 输入串: 2.03 ms, librime 加载: 1042.48 ms, 开会话+选方案: 26.98 ms, 逐句解码: 102.3 ms
    [rime_wanxiang_with_gram] 输入串: 1.95 ms, librime 加载: 374.88 ms, 开会话+选方案: 1272.86 ms, 逐句解码: 684.93 ms
    [rime_wubi_sentens_wubi86] 输入串: 5.44 ms, librime 加载: 811.02 ms, 开会话+选方案: 388.43 ms, 逐句解码: 95.26 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 5.84 ms, librime 加载: 835.62 ms, 开会话+选方案: 366.57 ms, 逐句解码: 105.12 ms
    [wanxiang] 输入串: 1.88 ms, librime 加载: 373.91 ms, 开会话+选方案: 1278.43 ms, 逐句解码: 678.96 ms
  · test
    读取文件: 0.16 ms
    分句: 0.02 ms
    预过滤: 0.02 ms
    [mingyuepinyin] 输入串: 0.39 ms, librime 加载: 364.06 ms, 开会话+选方案: 37.43 ms, 逐句解码: 9.17 ms
    [mingyuepinyin_with_gram] 输入串: 0.42 ms, librime 加载: 348.03 ms, 开会话+选方案: 19.15 ms, 逐句解码: 10.9 ms
    [rime_frost] 输入串: 0.44 ms, librime 加载: 1061.7 ms, 开会话+选方案: 50.58 ms, 逐句解码: 18.71 ms
    [rime_frost_with_gram] 输入串: 0.38 ms, librime 加载: 1072.82 ms, 开会话+选方案: 29.27 ms, 逐句解码: 19.81 ms
    [rime_ice] 输入串: 0.44 ms, librime 加载: 1062.22 ms, 开会话+选方案: 27.0 ms, 逐句解码: 23.99 ms
    [rime_ice_with_gram] 输入串: 0.45 ms, librime 加载: 1080.2 ms, 开会话+选方案: 29.68 ms, 逐句解码: 26.9 ms
    [rime_wanxiang_with_gram] 输入串: 0.46 ms, librime 加载: 353.62 ms, 开会话+选方案: 1286.42 ms, 逐句解码: 71.6 ms
    [rime_wubi_sentens_wubi86] 输入串: 1.15 ms, librime 加载: 824.15 ms, 开会话+选方案: 406.21 ms, 逐句解码: 26.5 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 1.02 ms, librime 加载: 818.89 ms, 开会话+选方案: 400.48 ms, 逐句解码: 25.67 ms
    [wanxiang] 输入串: 0.39 ms, librime 加载: 365.08 ms, 开会话+选方案: 1313.28 ms, 逐句解码: 64.55 ms

========================================================================
句子正确判定: Top 1 候选中任一项与 gold 完全一致即判对。

同义词归一化（句级完全匹配与 CER 计算前）: 其它→其他；他/她/它→他；的/地/得→的

说明: 分句后仅「纯汉字」且不含 ASCII 数字/英文字母、汉字不少于 5 字的片段参与评测；其它片段已过滤。句子正确率 = 归一化后预测与金句完全一致的比例；文字正确率 = 全语料 (归一化后总字数−总编辑距离)/归一化后总字数。输入串按各 vendor 自身配置生成，可能是连续拼音，也可能是形码前缀串。
```

