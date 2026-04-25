# Rime 评测结果

- 生成时间: 2026-04-25 20:59:35 +08:00
- 来源文件: `benchmark_all_corpus_20260425T125812Z_report.txt`

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
生成时间 (UTC): 20260425T125812Z
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
【总耗时】全流程墙钟约 82760.59 ms（多语料）

【各语料耗时】
  · news
    读取文件: 0.2 ms
    分句: 0.18 ms
    预过滤: 0.87 ms
    [mingyuepinyin] 输入串: 2.11 ms, librime 加载: 378.9 ms, 开会话+选方案: 28.3 ms, 逐句解码: 109.14 ms
    [mingyuepinyin_with_gram] 输入串: 1.91 ms, librime 加载: 369.2 ms, 开会话+选方案: 16.66 ms, 逐句解码: 153.44 ms
    [rime_frost] 输入串: 1.88 ms, librime 加载: 899.27 ms, 开会话+选方案: 62.05 ms, 逐句解码: 593.71 ms
    [rime_frost_with_gram] 输入串: 1.9 ms, librime 加载: 10260.97 ms, 开会话+选方案: 73.27 ms, 逐句解码: 676.42 ms
    [rime_ice] 输入串: 1.88 ms, librime 加载: 1083.1 ms, 开会话+选方案: 36.61 ms, 逐句解码: 105.63 ms
    [rime_ice_with_gram] 输入串: 1.99 ms, librime 加载: 1104.44 ms, 开会话+选方案: 29.25 ms, 逐句解码: 114.46 ms
    [rime_wanxiang_with_gram] 输入串: 1.97 ms, librime 加载: 365.71 ms, 开会话+选方案: 1284.27 ms, 逐句解码: 1022.54 ms
    [rime_wubi_sentens_wubi86] 输入串: 79.41 ms, librime 加载: 820.01 ms, 开会话+选方案: 407.37 ms, 逐句解码: 101.63 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 79.99 ms, librime 加载: 814.23 ms, 开会话+选方案: 397.61 ms, 逐句解码: 116.45 ms
    [wanxiang] 输入串: 2.11 ms, librime 加载: 372.57 ms, 开会话+选方案: 1328.45 ms, 逐句解码: 995.93 ms
  · novel
    读取文件: 0.4 ms
    分句: 0.53 ms
    预过滤: 0.3 ms
    [mingyuepinyin] 输入串: 7.46 ms, librime 加载: 343.23 ms, 开会话+选方案: 19.08 ms, 逐句解码: 214.41 ms
    [mingyuepinyin_with_gram] 输入串: 7.07 ms, librime 加载: 338.31 ms, 开会话+选方案: 16.42 ms, 逐句解码: 260.74 ms
    [rime_frost] 输入串: 9.07 ms, librime 加载: 773.8 ms, 开会话+选方案: 62.09 ms, 逐句解码: 1942.32 ms
    [rime_frost_with_gram] 输入串: 7.95 ms, librime 加载: 839.52 ms, 开会话+选方案: 56.47 ms, 逐句解码: 1982.84 ms
    [rime_ice] 输入串: 7.47 ms, librime 加载: 1088.94 ms, 开会话+选方案: 27.71 ms, 逐句解码: 259.11 ms
    [rime_ice_with_gram] 输入串: 7.31 ms, librime 加载: 1098.8 ms, 开会话+选方案: 30.22 ms, 逐句解码: 298.63 ms
    [rime_wanxiang_with_gram] 输入串: 7.75 ms, librime 加载: 372.55 ms, 开会话+选方案: 1291.74 ms, 逐句解码: 2288.36 ms
    [rime_wubi_sentens_wubi86] 输入串: 22.76 ms, librime 加载: 857.6 ms, 开会话+选方案: 373.55 ms, 逐句解码: 351.09 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 22.25 ms, librime 加载: 847.29 ms, 开会话+选方案: 405.91 ms, 逐句解码: 389.94 ms
    [wanxiang] 输入串: 7.76 ms, librime 加载: 398.4 ms, 开会话+选方案: 1314.85 ms, 逐句解码: 2260.99 ms
  · prose
    读取文件: 0.16 ms
    分句: 0.12 ms
    预过滤: 0.09 ms
    [mingyuepinyin] 输入串: 2.62 ms, librime 加载: 363.38 ms, 开会话+选方案: 20.24 ms, 逐句解码: 75.8 ms
    [mingyuepinyin_with_gram] 输入串: 2.44 ms, librime 加载: 324.5 ms, 开会话+选方案: 31.31 ms, 逐句解码: 76.94 ms
    [rime_frost] 输入串: 2.57 ms, librime 加载: 788.75 ms, 开会话+选方案: 66.16 ms, 逐句解码: 544.73 ms
    [rime_frost_with_gram] 输入串: 2.94 ms, librime 加载: 789.56 ms, 开会话+选方案: 58.62 ms, 逐句解码: 579.08 ms
    [rime_ice] 输入串: 2.6 ms, librime 加载: 1085.9 ms, 开会话+选方案: 28.96 ms, 逐句解码: 87.62 ms
    [rime_ice_with_gram] 输入串: 2.9 ms, librime 加载: 1097.05 ms, 开会话+选方案: 33.57 ms, 逐句解码: 101.58 ms
    [rime_wanxiang_with_gram] 输入串: 2.46 ms, librime 加载: 358.69 ms, 开会话+选方案: 1300.06 ms, 逐句解码: 639.45 ms
    [rime_wubi_sentens_wubi86] 输入串: 6.11 ms, librime 加载: 836.57 ms, 开会话+选方案: 371.26 ms, 逐句解码: 126.98 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 7.0 ms, librime 加载: 834.3 ms, 开会话+选方案: 400.75 ms, 逐句解码: 142.91 ms
    [wanxiang] 输入串: 2.7 ms, librime 加载: 370.66 ms, 开会话+选方案: 1304.98 ms, 逐句解码: 620.54 ms
  · tech
    读取文件: 0.15 ms
    分句: 0.11 ms
    预过滤: 0.08 ms
    [mingyuepinyin] 输入串: 2.28 ms, librime 加载: 353.72 ms, 开会话+选方案: 16.2 ms, 逐句解码: 40.55 ms
    [mingyuepinyin_with_gram] 输入串: 2.34 ms, librime 加载: 319.6 ms, 开会话+选方案: 24.78 ms, 逐句解码: 67.96 ms
    [rime_frost] 输入串: 2.1 ms, librime 加载: 762.34 ms, 开会话+选方案: 58.2 ms, 逐句解码: 389.22 ms
    [rime_frost_with_gram] 输入串: 2.15 ms, librime 加载: 763.97 ms, 开会话+选方案: 59.45 ms, 逐句解码: 401.11 ms
    [rime_ice] 输入串: 2.21 ms, librime 加载: 1088.02 ms, 开会话+选方案: 29.35 ms, 逐句解码: 67.69 ms
    [rime_ice_with_gram] 输入串: 2.24 ms, librime 加载: 1094.22 ms, 开会话+选方案: 31.93 ms, 逐句解码: 82.28 ms
    [rime_wanxiang_with_gram] 输入串: 2.18 ms, librime 加载: 363.14 ms, 开会话+选方案: 1301.86 ms, 逐句解码: 424.78 ms
    [rime_wubi_sentens_wubi86] 输入串: 5.38 ms, librime 加载: 861.16 ms, 开会话+选方案: 386.21 ms, 逐句解码: 116.71 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 5.04 ms, librime 加载: 828.36 ms, 开会话+选方案: 371.2 ms, 逐句解码: 133.68 ms
    [wanxiang] 输入串: 2.51 ms, librime 加载: 398.58 ms, 开会话+选方案: 1322.18 ms, 逐句解码: 413.25 ms
  · test
    读取文件: 0.14 ms
    分句: 0.02 ms
    预过滤: 0.02 ms
    [mingyuepinyin] 输入串: 0.42 ms, librime 加载: 347.07 ms, 开会话+选方案: 19.77 ms, 逐句解码: 9.3 ms
    [mingyuepinyin_with_gram] 输入串: 0.41 ms, librime 加载: 324.02 ms, 开会话+选方案: 39.66 ms, 逐句解码: 10.72 ms
    [rime_frost] 输入串: 0.39 ms, librime 加载: 762.71 ms, 开会话+选方案: 72.46 ms, 逐句解码: 98.79 ms
    [rime_frost_with_gram] 输入串: 0.4 ms, librime 加载: 771.8 ms, 开会话+选方案: 62.88 ms, 逐句解码: 66.53 ms
    [rime_ice] 输入串: 0.43 ms, librime 加载: 1088.0 ms, 开会话+选方案: 36.22 ms, 逐句解码: 23.85 ms
    [rime_ice_with_gram] 输入串: 0.51 ms, librime 加载: 1089.98 ms, 开会话+选方案: 29.51 ms, 逐句解码: 26.06 ms
    [rime_wanxiang_with_gram] 输入串: 0.61 ms, librime 加载: 364.59 ms, 开会话+选方案: 1289.53 ms, 逐句解码: 71.08 ms
    [rime_wubi_sentens_wubi86] 输入串: 1.11 ms, librime 加载: 848.75 ms, 开会话+选方案: 391.83 ms, 逐句解码: 22.56 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 1.0 ms, librime 加载: 838.82 ms, 开会话+选方案: 402.12 ms, 逐句解码: 26.34 ms
    [wanxiang] 输入串: 0.39 ms, librime 加载: 367.67 ms, 开会话+选方案: 1281.34 ms, 逐句解码: 66.76 ms

========================================================================
同义词归一化（句级完全匹配与 CER 计算前）: 其它→其他；他/她/它→他；的/地/得→的

说明: 分句后仅「纯汉字」且不含 ASCII 数字/英文字母、汉字不少于 5 字的片段参与评测；其它片段已过滤。句子正确率 = 归一化后预测与金句完全一致的比例；文字正确率 = 全语料 (归一化后总字数−总编辑距离)/归一化后总字数。输入串按各 vendor 自身配置生成，可能是连续拼音，也可能是形码前缀串。
```

