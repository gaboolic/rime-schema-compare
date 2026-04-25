# Rime 评测结果

- 生成时间: 2026-04-25 16:49:02 +08:00
- 来源文件: `benchmark_all_corpus_20260425T084722Z_report.txt`

## Vendor 子模块版本

- `vendor/rime-frost`: `d57f35b37b95a885ce36ef58fd539a7fa98b89f1`
- `vendor/rime-ice`: `2bd2983c6c74ea49b3a013f150ade7f3b8a27515`
- `vendor/rime_wanxiang` (`wanxiang`): `618fb082dac7b7e9bb45820811202e881be92bff`
- `vendor/rime-wubi-sentence`: `c3b26af601e41de49227f86633df00985e8d8a77`

## 评测摘要

```text
========================================================================
Rime 多方案整句评测 — 摘要报告
========================================================================
生成时间 (UTC): 20260425T084722Z
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
    文字正确率: 93.25%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.24%

  [rime_frost_with_gram]
    句子正确率: 69.11%  (170/246 句完全匹配)
    文字正确率: 95.09%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.11%

  [wanxiang]
    句子正确率: 48.37%  (119/246 句完全匹配)
    文字正确率: 88.89%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.14%

  [rime_wanxiang_with_gram]
    句子正确率: 67.07%  (165/246 句完全匹配)
    文字正确率: 94.88%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.83%

  [rime_wubi_sentens_wubi86]
    句子正确率: 50.41%  (124/246 句完全匹配)
    文字正确率: 91.09%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.36%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 69.92%  (172/246 句完全匹配)
    文字正确率: 95.85%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.93%

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
    文字正确率: 96.06%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.91%

  [rime_frost_with_gram]
    句子正确率: 88.89%  (32/36 句完全匹配)
    文字正确率: 97.46%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.98%

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
    句子正确率: 80.56%  (29/36 句完全匹配)
    文字正确率: 96.34%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.54%

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
    句子正确率: 65.44%  (89/136 句完全匹配)
    文字正确率: 94.26%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.24%

  [wanxiang]
    句子正确率: 44.12%  (60/136 句完全匹配)
    文字正确率: 88.66%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 88.6%

  [rime_wanxiang_with_gram]
    句子正确率: 63.97%  (87/136 句完全匹配)
    文字正确率: 94.26%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.21%

  [rime_wubi_sentens_wubi86]
    句子正确率: 50.74%  (69/136 句完全匹配)
    文字正确率: 91.01%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.28%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 64.71%  (88/136 句完全匹配)
    文字正确率: 94.67%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.83%

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
    句子正确率: 52.63%  (20/38 句完全匹配)
    文字正确率: 93.9%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.97%

  [wanxiang]
    句子正确率: 34.21%  (13/38 句完全匹配)
    文字正确率: 84.55%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.21%

  [rime_wanxiang_with_gram]
    句子正确率: 50.0%  (19/38 句完全匹配)
    文字正确率: 93.7%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.51%

  [rime_wubi_sentens_wubi86]
    句子正确率: 47.37%  (18/38 句完全匹配)
    文字正确率: 90.65%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.81%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 63.16%  (24/38 句完全匹配)
    文字正确率: 96.54%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.67%

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
    句子正确率: 77.42%  (24/31 句完全匹配)
    文字正确率: 96.63%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.23%

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
    句子正确率: 87.1%  (27/31 句完全匹配)
    文字正确率: 98.56%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 98.79%

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
【总耗时】全流程墙钟约 99576.8 ms（多语料）

【各语料耗时】
  · news
    读取文件: 0.1 ms
    分句: 0.16 ms
    预过滤: 0.83 ms
    [mingyuepinyin] 输入串: 2.26 ms, librime 加载: 359.12 ms, 开会话+选方案: 30.26 ms, 逐句解码: 108.2 ms
    [mingyuepinyin_with_gram] 输入串: 1.97 ms, librime 加载: 340.2 ms, 开会话+选方案: 13.39 ms, 逐句解码: 125.8 ms
    [rime_frost] 输入串: 2.01 ms, librime 加载: 10717.14 ms, 开会话+选方案: 78.76 ms, 逐句解码: 593.31 ms
    [rime_frost_with_gram] 输入串: 2.33 ms, librime 加载: 749.78 ms, 开会话+选方案: 77.5 ms, 逐句解码: 580.6 ms
    [rime_ice] 输入串: 2.04 ms, librime 加载: 1087.76 ms, 开会话+选方案: 33.2 ms, 逐句解码: 101.16 ms
    [rime_ice_with_gram] 输入串: 1.88 ms, librime 加载: 1070.64 ms, 开会话+选方案: 33.72 ms, 逐句解码: 114.68 ms
    [rime_wanxiang_with_gram] 输入串: 2.31 ms, librime 加载: 371.34 ms, 开会话+选方案: 1296.63 ms, 逐句解码: 988.38 ms
    [rime_wubi_sentens_wubi86] 输入串: 96.76 ms, librime 加载: 831.34 ms, 开会话+选方案: 387.64 ms, 逐句解码: 109.11 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 80.29 ms, librime 加载: 830.86 ms, 开会话+选方案: 366.87 ms, 逐句解码: 125.49 ms
    [wanxiang] 输入串: 1.94 ms, librime 加载: 369.65 ms, 开会话+选方案: 1304.69 ms, 逐句解码: 965.79 ms
  · novel
    读取文件: 0.14 ms
    分句: 0.48 ms
    预过滤: 0.32 ms
    [mingyuepinyin] 输入串: 9.77 ms, librime 加载: 341.64 ms, 开会话+选方案: 27.95 ms, 逐句解码: 215.26 ms
    [mingyuepinyin_with_gram] 输入串: 7.44 ms, librime 加载: 343.37 ms, 开会话+选方案: 33.75 ms, 逐句解码: 252.58 ms
    [rime_frost] 输入串: 7.56 ms, librime 加载: 819.48 ms, 开会话+选方案: 82.25 ms, 逐句解码: 1829.03 ms
    [rime_frost_with_gram] 输入串: 7.29 ms, librime 加载: 740.05 ms, 开会话+选方案: 73.42 ms, 逐句解码: 1803.13 ms
    [rime_ice] 输入串: 7.22 ms, librime 加载: 1074.25 ms, 开会话+选方案: 31.09 ms, 逐句解码: 259.55 ms
    [rime_ice_with_gram] 输入串: 7.66 ms, librime 加载: 1066.97 ms, 开会话+选方案: 29.97 ms, 逐句解码: 294.06 ms
    [rime_wanxiang_with_gram] 输入串: 20.02 ms, librime 加载: 592.8 ms, 开会话+选方案: 2815.35 ms, 逐句解码: 4807.48 ms
    [rime_wubi_sentens_wubi86] 输入串: 57.71 ms, librime 加载: 1448.94 ms, 开会话+选方案: 762.93 ms, 逐句解码: 685.86 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 73.83 ms, librime 加载: 1442.58 ms, 开会话+选方案: 758.09 ms, 逐句解码: 753.69 ms
    [wanxiang] 输入串: 7.61 ms, librime 加载: 383.85 ms, 开会话+选方案: 1256.85 ms, 逐句解码: 2633.6 ms
  · prose
    读取文件: 0.22 ms
    分句: 0.26 ms
    预过滤: 0.49 ms
    [mingyuepinyin] 输入串: 6.57 ms, librime 加载: 561.94 ms, 开会话+选方案: 35.2 ms, 逐句解码: 167.19 ms
    [mingyuepinyin_with_gram] 输入串: 5.66 ms, librime 加载: 531.34 ms, 开会话+选方案: 46.22 ms, 逐句解码: 188.88 ms
    [rime_frost] 输入串: 5.63 ms, librime 加载: 1162.14 ms, 开会话+选方案: 152.61 ms, 逐句解码: 1116.47 ms
    [rime_frost_with_gram] 输入串: 8.86 ms, librime 加载: 1139.61 ms, 开会话+选方案: 174.27 ms, 逐句解码: 1086.83 ms
    [rime_ice] 输入串: 6.6 ms, librime 加载: 1685.28 ms, 开会话+选方案: 52.18 ms, 逐句解码: 167.59 ms
    [rime_ice_with_gram] 输入串: 6.67 ms, librime 加载: 1636.15 ms, 开会话+选方案: 46.89 ms, 逐句解码: 182.71 ms
    [rime_wanxiang_with_gram] 输入串: 5.74 ms, librime 加载: 599.49 ms, 开会话+选方案: 2731.56 ms, 逐句解码: 1267.92 ms
    [rime_wubi_sentens_wubi86] 输入串: 22.53 ms, librime 加载: 1422.89 ms, 开会话+选方案: 544.67 ms, 逐句解码: 128.59 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 6.13 ms, librime 加载: 825.17 ms, 开会话+选方案: 388.49 ms, 逐句解码: 158.64 ms
    [wanxiang] 输入串: 5.75 ms, librime 加载: 655.23 ms, 开会话+选方案: 2949.49 ms, 逐句解码: 1319.98 ms
  · tech
    读取文件: 0.19 ms
    分句: 0.11 ms
    预过滤: 0.09 ms
    [mingyuepinyin] 输入串: 2.27 ms, librime 加载: 336.48 ms, 开会话+选方案: 19.92 ms, 逐句解码: 41.06 ms
    [mingyuepinyin_with_gram] 输入串: 2.17 ms, librime 加载: 326.82 ms, 开会话+选方案: 24.69 ms, 逐句解码: 97.45 ms
    [rime_frost] 输入串: 2.44 ms, librime 加载: 772.83 ms, 开会话+选方案: 60.46 ms, 逐句解码: 371.01 ms
    [rime_frost_with_gram] 输入串: 2.55 ms, librime 加载: 763.83 ms, 开会话+选方案: 57.81 ms, 逐句解码: 382.7 ms
    [rime_ice] 输入串: 2.43 ms, librime 加载: 1087.17 ms, 开会话+选方案: 29.09 ms, 逐句解码: 67.83 ms
    [rime_ice_with_gram] 输入串: 2.1 ms, librime 加载: 1090.62 ms, 开会话+选方案: 36.74 ms, 逐句解码: 81.69 ms
    [rime_wanxiang_with_gram] 输入串: 2.71 ms, librime 加载: 358.24 ms, 开会话+选方案: 1300.29 ms, 逐句解码: 428.58 ms
    [rime_wubi_sentens_wubi86] 输入串: 5.08 ms, librime 加载: 829.59 ms, 开会话+选方案: 385.04 ms, 逐句解码: 116.22 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 5.54 ms, librime 加载: 834.12 ms, 开会话+选方案: 388.72 ms, 逐句解码: 130.21 ms
    [wanxiang] 输入串: 2.33 ms, librime 加载: 386.03 ms, 开会话+选方案: 1282.43 ms, 逐句解码: 414.41 ms
  · test
    读取文件: 0.13 ms
    分句: 0.02 ms
    预过滤: 0.02 ms
    [mingyuepinyin] 输入串: 0.44 ms, librime 加载: 327.37 ms, 开会话+选方案: 29.07 ms, 逐句解码: 9.64 ms
    [mingyuepinyin_with_gram] 输入串: 0.43 ms, librime 加载: 335.84 ms, 开会话+选方案: 18.14 ms, 逐句解码: 10.53 ms
    [rime_frost] 输入串: 0.4 ms, librime 加载: 759.06 ms, 开会话+选方案: 77.32 ms, 逐句解码: 93.77 ms
    [rime_frost_with_gram] 输入串: 0.42 ms, librime 加载: 748.21 ms, 开会话+选方案: 59.47 ms, 逐句解码: 64.63 ms
    [rime_ice] 输入串: 0.39 ms, librime 加载: 1060.44 ms, 开会话+选方案: 32.34 ms, 逐句解码: 25.88 ms
    [rime_ice_with_gram] 输入串: 0.42 ms, librime 加载: 1055.59 ms, 开会话+选方案: 27.33 ms, 逐句解码: 25.69 ms
    [rime_wanxiang_with_gram] 输入串: 0.4 ms, librime 加载: 372.22 ms, 开会话+选方案: 1255.34 ms, 逐句解码: 69.14 ms
    [rime_wubi_sentens_wubi86] 输入串: 1.03 ms, librime 加载: 845.87 ms, 开会话+选方案: 397.8 ms, 逐句解码: 23.97 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 1.32 ms, librime 加载: 823.39 ms, 开会话+选方案: 398.29 ms, 逐句解码: 31.46 ms
    [wanxiang] 输入串: 0.45 ms, librime 加载: 391.58 ms, 开会话+选方案: 1278.18 ms, 逐句解码: 67.3 ms

========================================================================
同义词归一化（句级完全匹配与 CER 计算前）: 其它→其他；他/她/它→他；的/地/得→的

说明: 分句后仅「纯汉字」且不含 ASCII 数字/英文字母、汉字不少于 5 字的片段参与评测；其它片段已过滤。句子正确率 = 归一化后预测与金句完全一致的比例；文字正确率 = 全语料 (归一化后总字数−总编辑距离)/归一化后总字数。输入串按各 vendor 自身配置生成，可能是连续拼音，也可能是形码前缀串。
```

