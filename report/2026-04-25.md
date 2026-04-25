# Rime 评测结果

- 生成时间: 2026-04-25 21:30:36 +08:00
- 来源文件: `benchmark_all_corpus_20260425T132924Z_report.txt`

## Vendor 子模块版本

- `vendor/rime-frost`: `29b41fdeeedcb6f31b26b8408aec8e1448988a26`
- `vendor/rime-ice`: `2bd2983c6c74ea49b3a013f150ade7f3b8a27515`
- `vendor/rime_wanxiang` (`wanxiang`): `618fb082dac7b7e9bb45820811202e881be92bff`
- `vendor/rime-wubi-sentence`: `c3b26af601e41de49227f86633df00985e8d8a77`

## 评测摘要

```text
========================================================================
Rime 多方案整句评测 — 摘要报告
========================================================================
生成时间 (UTC): 20260425T132924Z
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
    句子正确率: 49.59%  (122/246 句完全匹配)
    文字正确率: 89.83%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.87%

  [mingyuepinyin_with_gram]
    句子正确率: 36.99%  (91/246 句完全匹配)
    文字正确率: 86.15%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 86.18%

  [rime_ice]
    句子正确率: 59.35%  (146/246 句完全匹配)
    文字正确率: 92.28%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.67%

  [rime_ice_with_gram]
    句子正确率: 64.23%  (158/246 句完全匹配)
    文字正确率: 94.23%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.38%

  [rime_frost]
    句子正确率: 61.79%  (152/246 句完全匹配)
    文字正确率: 93.22%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.21%

  [rime_frost_with_gram]
    句子正确率: 71.54%  (176/246 句完全匹配)
    文字正确率: 95.45%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.45%

  [wanxiang]
    句子正确率: 48.37%  (119/246 句完全匹配)
    文字正确率: 88.89%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.14%

  [rime_wanxiang_with_gram]
    句子正确率: 66.67%  (164/246 句完全匹配)
    文字正确率: 94.7%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.62%

  [rime_wubi_sentens_wubi86]
    句子正确率: 50.41%  (124/246 句完全匹配)
    文字正确率: 91.09%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.36%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 71.14%  (175/246 句完全匹配)
    文字正确率: 95.96%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.14%

------------------------------------------------------------------------
【语料: news】
  [mingyuepinyin]
    句子正确率: 58.33%  (21/36 句完全匹配)
    文字正确率: 91.27%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.24%

  [mingyuepinyin_with_gram]
    句子正确率: 47.22%  (17/36 句完全匹配)
    文字正确率: 84.23%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.82%

  [rime_ice]
    句子正确率: 91.67%  (33/36 句完全匹配)
    文字正确率: 98.87%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 98.74%

  [rime_ice_with_gram]
    句子正确率: 88.89%  (32/36 句完全匹配)
    文字正确率: 97.18%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.54%

  [rime_frost]
    句子正确率: 80.56%  (29/36 句完全匹配)
    文字正确率: 95.77%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.72%

  [rime_frost_with_gram]
    句子正确率: 88.89%  (32/36 句完全匹配)
    文字正确率: 96.62%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.1%

  [wanxiang]
    句子正确率: 72.22%  (26/36 句完全匹配)
    文字正确率: 91.55%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.03%

  [rime_wanxiang_with_gram]
    句子正确率: 86.11%  (31/36 句完全匹配)
    文字正确率: 96.9%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.27%

  [rime_wubi_sentens_wubi86]
    句子正确率: 50.0%  (18/36 句完全匹配)
    文字正确率: 91.27%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.94%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 77.78%  (28/36 句完全匹配)
    文字正确率: 94.65%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.43%

------------------------------------------------------------------------
【语料: novel】
  [mingyuepinyin]
    句子正确率: 44.12%  (60/136 句完全匹配)
    文字正确率: 87.83%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 87.93%

  [mingyuepinyin_with_gram]
    句子正确率: 36.76%  (50/136 句完全匹配)
    文字正确率: 87.28%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 86.88%

  [rime_ice]
    句子正确率: 50.74%  (69/136 句完全匹配)
    文字正确率: 90.66%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.02%

  [rime_ice_with_gram]
    句子正确率: 62.5%  (85/136 句完全匹配)
    文字正确率: 93.85%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.96%

  [rime_frost]
    句子正确率: 52.94%  (72/136 句完全匹配)
    文字正确率: 91.08%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 90.91%

  [rime_frost_with_gram]
    句子正确率: 67.65%  (92/136 句完全匹配)
    文字正确率: 94.74%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.69%

  [wanxiang]
    句子正确率: 44.12%  (60/136 句完全匹配)
    文字正确率: 88.66%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 88.6%

  [rime_wanxiang_with_gram]
    句子正确率: 63.24%  (86/136 句完全匹配)
    文字正确率: 94.05%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.89%

  [rime_wubi_sentens_wubi86]
    句子正确率: 50.74%  (69/136 句完全匹配)
    文字正确率: 91.01%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.28%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 67.65%  (92/136 句完全匹配)
    文字正确率: 95.3%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.58%

------------------------------------------------------------------------
【语料: prose】
  [mingyuepinyin]
    句子正确率: 44.74%  (17/38 句完全匹配)
    文字正确率: 90.65%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 90.83%

  [mingyuepinyin_with_gram]
    句子正确率: 23.68%  (9/38 句完全匹配)
    文字正确率: 84.76%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.9%

  [rime_ice]
    句子正确率: 52.63%  (20/38 句完全匹配)
    文字正确率: 90.04%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.56%

  [rime_ice_with_gram]
    句子正确率: 39.47%  (15/38 句完全匹配)
    文字正确率: 91.67%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.61%

  [rime_frost]
    句子正确率: 55.26%  (21/38 句完全匹配)
    文字正确率: 93.5%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.52%

  [rime_frost_with_gram]
    句子正确率: 55.26%  (21/38 句完全匹配)
    文字正确率: 94.51%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.87%

  [wanxiang]
    句子正确率: 34.21%  (13/38 句完全匹配)
    文字正确率: 84.55%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.21%

  [rime_wanxiang_with_gram]
    句子正确率: 50.0%  (19/38 句完全匹配)
    文字正确率: 93.29%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.27%

  [rime_wubi_sentens_wubi86]
    句子正确率: 47.37%  (18/38 句完全匹配)
    文字正确率: 90.65%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.81%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 60.53%  (23/38 句完全匹配)
    文字正确率: 96.14%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.19%

------------------------------------------------------------------------
【语料: tech】
  [mingyuepinyin]
    句子正确率: 70.97%  (22/31 句完全匹配)
    文字正确率: 94.23%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.89%

  [mingyuepinyin_with_gram]
    句子正确率: 38.71%  (12/31 句完全匹配)
    文字正确率: 84.62%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.93%

  [rime_ice]
    句子正确率: 67.74%  (21/31 句完全匹配)
    文字正确率: 95.43%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.64%

  [rime_ice_with_gram]
    句子正确率: 67.74%  (21/31 句完全匹配)
    文字正确率: 95.19%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.02%

  [rime_frost]
    句子正确率: 80.65%  (25/31 句完全匹配)
    文字正确率: 97.12%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.79%

  [rime_frost_with_gram]
    句子正确率: 83.87%  (26/31 句完全匹配)
    文字正确率: 97.36%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.85%

  [wanxiang]
    句子正确率: 58.06%  (18/31 句完全匹配)
    文字正确率: 93.27%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.91%

  [rime_wanxiang_with_gram]
    句子正确率: 74.19%  (23/31 句完全匹配)
    文字正确率: 95.91%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.47%

  [rime_wubi_sentens_wubi86]
    句子正确率: 58.06%  (18/31 句完全匹配)
    文字正确率: 92.79%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.73%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 90.32%  (28/31 句完全匹配)
    文字正确率: 99.04%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 99.05%

------------------------------------------------------------------------
【语料: test】
  [mingyuepinyin]
    句子正确率: 40.0%  (2/5 句完全匹配)
    文字正确率: 92.06%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.13%

  [mingyuepinyin_with_gram]
    句子正确率: 60.0%  (3/5 句完全匹配)
    文字正确率: 92.06%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.36%

  [rime_ice]
    句子正确率: 60.0%  (3/5 句完全匹配)
    文字正确率: 88.89%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.16%

  [rime_ice_with_gram]
    句子正确率: 100.0%  (5/5 句完全匹配)
    文字正确率: 100.0%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 100.0%

  [rime_frost]
    句子正确率: 100.0%  (5/5 句完全匹配)
    文字正确率: 100.0%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 100.0%

  [rime_frost_with_gram]
    句子正确率: 100.0%  (5/5 句完全匹配)
    文字正确率: 100.0%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 100.0%

  [wanxiang]
    句子正确率: 40.0%  (2/5 句完全匹配)
    文字正确率: 84.13%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 83.96%

  [rime_wanxiang_with_gram]
    句子正确率: 100.0%  (5/5 句完全匹配)
    文字正确率: 100.0%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 100.0%

  [rime_wubi_sentens_wubi86]
    句子正确率: 20.0%  (1/5 句完全匹配)
    文字正确率: 84.13%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 83.58%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 80.0%  (4/5 句完全匹配)
    文字正确率: 96.83%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.89%

========================================================================
【总耗时】全流程墙钟约 72134.77 ms（多语料）

【各语料耗时】
  · news
    读取文件: 0.1 ms
    分句: 0.17 ms
    预过滤: 0.82 ms
    [mingyuepinyin] 输入串: 2.99 ms, librime 加载: 348.71 ms, 开会话+选方案: 27.68 ms, 逐句解码: 106.96 ms
    [mingyuepinyin_with_gram] 输入串: 1.9 ms, librime 加载: 356.92 ms, 开会话+选方案: 37.1 ms, 逐句解码: 122.17 ms
    [rime_frost] 输入串: 2.22 ms, librime 加载: 792.27 ms, 开会话+选方案: 68.59 ms, 逐句解码: 573.61 ms
    [rime_frost_with_gram] 输入串: 1.9 ms, librime 加载: 780.43 ms, 开会话+选方案: 62.94 ms, 逐句解码: 601.22 ms
    [rime_ice] 输入串: 2.57 ms, librime 加载: 1076.73 ms, 开会话+选方案: 33.62 ms, 逐句解码: 101.08 ms
    [rime_ice_with_gram] 输入串: 1.99 ms, librime 加载: 1085.15 ms, 开会话+选方案: 38.11 ms, 逐句解码: 114.88 ms
    [rime_wanxiang_with_gram] 输入串: 1.9 ms, librime 加载: 372.41 ms, 开会话+选方案: 1274.96 ms, 逐句解码: 982.46 ms
    [rime_wubi_sentens_wubi86] 输入串: 78.53 ms, librime 加载: 812.03 ms, 开会话+选方案: 391.17 ms, 逐句解码: 100.4 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 79.45 ms, librime 加载: 807.71 ms, 开会话+选方案: 394.66 ms, 逐句解码: 115.34 ms
    [wanxiang] 输入串: 1.9 ms, librime 加载: 384.48 ms, 开会话+选方案: 1317.31 ms, 逐句解码: 959.15 ms
  · novel
    读取文件: 0.17 ms
    分句: 0.42 ms
    预过滤: 0.29 ms
    [mingyuepinyin] 输入串: 7.32 ms, librime 加载: 396.3 ms, 开会话+选方案: 26.59 ms, 逐句解码: 211.45 ms
    [mingyuepinyin_with_gram] 输入串: 7.51 ms, librime 加载: 353.76 ms, 开会话+选方案: 41.32 ms, 逐句解码: 252.01 ms
    [rime_frost] 输入串: 7.09 ms, librime 加载: 768.19 ms, 开会话+选方案: 71.45 ms, 逐句解码: 1783.7 ms
    [rime_frost_with_gram] 输入串: 7.15 ms, librime 加载: 775.99 ms, 开会话+选方案: 69.45 ms, 逐句解码: 1829.24 ms
    [rime_ice] 输入串: 7.02 ms, librime 加载: 1076.93 ms, 开会话+选方案: 32.18 ms, 逐句解码: 256.95 ms
    [rime_ice_with_gram] 输入串: 7.63 ms, librime 加载: 1072.7 ms, 开会话+选方案: 28.72 ms, 逐句解码: 290.94 ms
    [rime_wanxiang_with_gram] 输入串: 7.66 ms, librime 加载: 411.18 ms, 开会话+选方案: 1277.76 ms, 逐句解码: 2253.1 ms
    [rime_wubi_sentens_wubi86] 输入串: 23.36 ms, librime 加载: 863.33 ms, 开会话+选方案: 395.18 ms, 逐句解码: 346.87 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 21.43 ms, librime 加载: 821.97 ms, 开会话+选方案: 377.25 ms, 逐句解码: 369.57 ms
    [wanxiang] 输入串: 7.38 ms, librime 加载: 367.62 ms, 开会话+选方案: 1245.85 ms, 逐句解码: 2197.36 ms
  · prose
    读取文件: 0.14 ms
    分句: 0.15 ms
    预过滤: 0.1 ms
    [mingyuepinyin] 输入串: 2.61 ms, librime 加载: 353.7 ms, 开会话+选方案: 41.94 ms, 逐句解码: 71.6 ms
    [mingyuepinyin_with_gram] 输入串: 2.56 ms, librime 加载: 365.06 ms, 开会话+选方案: 26.52 ms, 逐句解码: 76.68 ms
    [rime_frost] 输入串: 2.45 ms, librime 加载: 759.33 ms, 开会话+选方案: 64.9 ms, 逐句解码: 556.76 ms
    [rime_frost_with_gram] 输入串: 2.57 ms, librime 加载: 756.02 ms, 开会话+选方案: 57.84 ms, 逐句解码: 528.46 ms
    [rime_ice] 输入串: 2.56 ms, librime 加载: 1066.18 ms, 开会话+选方案: 41.34 ms, 逐句解码: 86.71 ms
    [rime_ice_with_gram] 输入串: 2.44 ms, librime 加载: 1071.95 ms, 开会话+选方案: 31.01 ms, 逐句解码: 101.94 ms
    [rime_wanxiang_with_gram] 输入串: 2.54 ms, librime 加载: 366.5 ms, 开会话+选方案: 1298.27 ms, 逐句解码: 630.09 ms
    [rime_wubi_sentens_wubi86] 输入串: 6.6 ms, librime 加载: 852.83 ms, 开会话+选方案: 387.96 ms, 逐句解码: 127.12 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 8.02 ms, librime 加载: 828.43 ms, 开会话+选方案: 405.69 ms, 逐句解码: 143.09 ms
    [wanxiang] 输入串: 2.56 ms, librime 加载: 404.76 ms, 开会话+选方案: 1310.37 ms, 逐句解码: 615.35 ms
  · tech
    读取文件: 0.14 ms
    分句: 0.11 ms
    预过滤: 0.07 ms
    [mingyuepinyin] 输入串: 2.18 ms, librime 加载: 375.73 ms, 开会话+选方案: 35.38 ms, 逐句解码: 48.22 ms
    [mingyuepinyin_with_gram] 输入串: 2.31 ms, librime 加载: 341.11 ms, 开会话+选方案: 25.97 ms, 逐句解码: 63.96 ms
    [rime_frost] 输入串: 2.11 ms, librime 加载: 758.0 ms, 开会话+选方案: 63.66 ms, 逐句解码: 376.93 ms
    [rime_frost_with_gram] 输入串: 2.22 ms, librime 加载: 752.08 ms, 开会话+选方案: 63.3 ms, 逐句解码: 388.28 ms
    [rime_ice] 输入串: 2.39 ms, librime 加载: 1109.12 ms, 开会话+选方案: 26.57 ms, 逐句解码: 69.04 ms
    [rime_ice_with_gram] 输入串: 2.33 ms, librime 加载: 1064.08 ms, 开会话+选方案: 28.69 ms, 逐句解码: 79.87 ms
    [rime_wanxiang_with_gram] 输入串: 2.22 ms, librime 加载: 378.47 ms, 开会话+选方案: 1266.5 ms, 逐句解码: 426.72 ms
    [rime_wubi_sentens_wubi86] 输入串: 9.83 ms, librime 加载: 853.94 ms, 开会话+选方案: 373.18 ms, 逐句解码: 116.04 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 5.54 ms, librime 加载: 808.5 ms, 开会话+选方案: 391.13 ms, 逐句解码: 130.5 ms
    [wanxiang] 输入串: 2.22 ms, librime 加载: 363.0 ms, 开会话+选方案: 1267.72 ms, 逐句解码: 390.13 ms
  · test
    读取文件: 0.14 ms
    分句: 0.02 ms
    预过滤: 0.02 ms
    [mingyuepinyin] 输入串: 0.41 ms, librime 加载: 352.4 ms, 开会话+选方案: 26.86 ms, 逐句解码: 8.38 ms
    [mingyuepinyin_with_gram] 输入串: 0.47 ms, librime 加载: 327.36 ms, 开会话+选方案: 41.28 ms, 逐句解码: 10.84 ms
    [rime_frost] 输入串: 0.47 ms, librime 加载: 763.92 ms, 开会话+选方案: 60.46 ms, 逐句解码: 62.5 ms
    [rime_frost_with_gram] 输入串: 0.4 ms, librime 加载: 757.99 ms, 开会话+选方案: 59.74 ms, 逐句解码: 68.7 ms
    [rime_ice] 输入串: 0.39 ms, librime 加载: 1054.0 ms, 开会话+选方案: 31.83 ms, 逐句解码: 23.52 ms
    [rime_ice_with_gram] 输入串: 0.52 ms, librime 加载: 1096.59 ms, 开会话+选方案: 31.56 ms, 逐句解码: 25.46 ms
    [rime_wanxiang_with_gram] 输入串: 0.43 ms, librime 加载: 360.49 ms, 开会话+选方案: 1250.3 ms, 逐句解码: 68.52 ms
    [rime_wubi_sentens_wubi86] 输入串: 1.11 ms, librime 加载: 852.98 ms, 开会话+选方案: 385.96 ms, 逐句解码: 22.48 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 0.99 ms, librime 加载: 838.37 ms, 开会话+选方案: 420.21 ms, 逐句解码: 24.95 ms
    [wanxiang] 输入串: 0.51 ms, librime 加载: 388.73 ms, 开会话+选方案: 1295.49 ms, 逐句解码: 66.06 ms

========================================================================
同义词归一化（句级完全匹配与 CER 计算前）: 其它→其他；他/她/它→他；的/地/得→的

说明: 分句后仅「纯汉字」且不含 ASCII 数字/英文字母、汉字不少于 5 字的片段参与评测；其它片段已过滤。句子正确率 = 归一化后预测与金句完全一致的比例；文字正确率 = 全语料 (归一化后总字数−总编辑距离)/归一化后总字数。输入串按各 vendor 自身配置生成，可能是连续拼音，也可能是形码前缀串。
```

