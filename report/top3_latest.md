# Rime 评测结果

- 生成时间: 2026-04-26 17:48:20 +08:00
- 来源文件: `benchmark_all_corpus_20260426T094631Z_report.txt`
- 句子正确判定: Top 3 候选中任一项与 gold 完全一致即判对

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
生成时间 (UTC): 20260426T094631Z
rime.dll: D:\vscode\rime_projs\rime-schema-compare\lib\rime222.dll
模式: 全部语料 (data/corpus/*.txt)

语料文件:
  - news: D:\vscode\rime_projs\rime-schema-compare\data\corpus\news.txt
  - novel: D:\vscode\rime_projs\rime-schema-compare\data\corpus\novel.txt
  - prose: D:\vscode\rime_projs\rime-schema-compare\data\corpus\prose.txt
  - tech: D:\vscode\rime_projs\rime-schema-compare\data\corpus\tech.txt
  - test: D:\vscode\rime_projs\rime-schema-compare\data\corpus\test.txt

【总体】
  [mingyuepinyin]
    句子正确率: 63.82%  (157/246 句完全匹配)
    文字正确率: 89.68%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.78%

  [mingyuepinyin_with_gram]
    句子正确率: 50.0%  (123/246 句完全匹配)
    文字正确率: 86.51%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 86.5%

  [rime_ice]
    句子正确率: 71.95%  (177/246 句完全匹配)
    文字正确率: 91.96%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.37%

  [rime_ice_with_gram]
    句子正确率: 74.39%  (183/246 句完全匹配)
    文字正确率: 94.48%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.54%

  [rime_frost]
    句子正确率: 76.02%  (187/246 句完全匹配)
    文字正确率: 93.22%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.21%

  [rime_frost_with_gram]
    句子正确率: 80.89%  (199/246 句完全匹配)
    文字正确率: 95.31%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.29%

  [wanxiang]
    句子正确率: 59.35%  (146/246 句完全匹配)
    文字正确率: 88.89%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.14%

  [rime_wanxiang_with_gram]
    句子正确率: 75.2%  (185/246 句完全匹配)
    文字正确率: 94.73%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.67%

  [rime_wubi_sentens_wubi86]
    句子正确率: 69.51%  (171/246 句完全匹配)
    文字正确率: 90.98%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.29%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 86.18%  (212/246 句完全匹配)
    文字正确率: 96.1%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.25%

------------------------------------------------------------------------
【语料: news】
  [mingyuepinyin]
    句子正确率: 77.78%  (28/36 句完全匹配)
    文字正确率: 91.27%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.24%

  [mingyuepinyin_with_gram]
    句子正确率: 61.11%  (22/36 句完全匹配)
    文字正确率: 84.23%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.82%

  [rime_ice]
    句子正确率: 100.0%  (36/36 句完全匹配)
    文字正确率: 97.46%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.68%

  [rime_ice_with_gram]
    句子正确率: 94.44%  (34/36 句完全匹配)
    文字正确率: 97.46%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.75%

  [rime_frost]
    句子正确率: 94.44%  (34/36 句完全匹配)
    文字正确率: 95.77%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.72%

  [rime_frost_with_gram]
    句子正确率: 94.44%  (34/36 句完全匹配)
    文字正确率: 96.62%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.1%

  [wanxiang]
    句子正确率: 83.33%  (30/36 句完全匹配)
    文字正确率: 91.55%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.03%

  [rime_wanxiang_with_gram]
    句子正确率: 91.67%  (33/36 句完全匹配)
    文字正确率: 96.9%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.27%

  [rime_wubi_sentens_wubi86]
    句子正确率: 83.33%  (30/36 句完全匹配)
    文字正确率: 91.27%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.94%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 94.44%  (34/36 句完全匹配)
    文字正确率: 94.65%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.43%

------------------------------------------------------------------------
【语料: novel】
  [mingyuepinyin]
    句子正确率: 60.29%  (82/136 句完全匹配)
    文字正确率: 87.83%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 87.93%

  [mingyuepinyin_with_gram]
    句子正确率: 49.26%  (67/136 句完全匹配)
    文字正确率: 87.55%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 87.16%

  [rime_ice]
    句子正确率: 63.97%  (87/136 句完全匹配)
    文字正确率: 90.39%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 90.75%

  [rime_ice_with_gram]
    句子正确率: 72.79%  (99/136 句完全匹配)
    文字正确率: 94.19%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.18%

  [rime_frost]
    句子正确率: 68.38%  (93/136 句完全匹配)
    文字正确率: 91.08%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 90.91%

  [rime_frost_with_gram]
    句子正确率: 77.94%  (106/136 句完全匹配)
    文字正确率: 94.61%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.54%

  [wanxiang]
    句子正确率: 55.88%  (76/136 句完全匹配)
    文字正确率: 88.66%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 88.6%

  [rime_wanxiang_with_gram]
    句子正确率: 72.79%  (99/136 句完全匹配)
    文字正确率: 94.19%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.99%

  [rime_wubi_sentens_wubi86]
    句子正确率: 66.18%  (90/136 句完全匹配)
    文字正确率: 90.8%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.15%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 81.62%  (111/136 句完全匹配)
    文字正确率: 95.44%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.66%

------------------------------------------------------------------------
【语料: prose】
  [mingyuepinyin]
    句子正确率: 52.63%  (20/38 句完全匹配)
    文字正确率: 89.84%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 90.28%

  [mingyuepinyin_with_gram]
    句子正确率: 36.84%  (14/38 句完全匹配)
    文字正确率: 84.76%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.95%

  [rime_ice]
    句子正确率: 63.16%  (24/38 句完全匹配)
    文字正确率: 90.04%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.56%

  [rime_ice_with_gram]
    句子正确率: 55.26%  (21/38 句完全匹配)
    文字正确率: 91.67%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.55%

  [rime_frost]
    句子正确率: 71.05%  (27/38 句完全匹配)
    文字正确率: 93.5%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.52%

  [rime_frost_with_gram]
    句子正确率: 68.42%  (26/38 句完全匹配)
    文字正确率: 94.11%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.35%

  [wanxiang]
    句子正确率: 42.11%  (16/38 句完全匹配)
    文字正确率: 84.55%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.21%

  [rime_wanxiang_with_gram]
    句子正确率: 63.16%  (24/38 句完全匹配)
    文字正确率: 92.89%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.0%

  [rime_wubi_sentens_wubi86]
    句子正确率: 65.79%  (25/38 句完全匹配)
    文字正确率: 90.65%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.81%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 84.21%  (32/38 句完全匹配)
    文字正确率: 96.34%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.43%

------------------------------------------------------------------------
【语料: tech】
  [mingyuepinyin]
    句子正确率: 77.42%  (24/31 句完全匹配)
    文字正确率: 94.23%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.89%

  [mingyuepinyin_with_gram]
    句子正确率: 54.84%  (17/31 句完全匹配)
    文字正确率: 86.06%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 86.21%

  [rime_ice]
    句子正确率: 83.87%  (26/31 句完全匹配)
    文字正确率: 95.43%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.64%

  [rime_ice_with_gram]
    句子正确率: 80.65%  (25/31 句完全匹配)
    文字正确率: 95.67%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.39%

  [rime_frost]
    句子正确率: 90.32%  (28/31 句完全匹配)
    文字正确率: 97.12%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.79%

  [rime_frost_with_gram]
    句子正确率: 90.32%  (28/31 句完全匹配)
    文字正确率: 97.36%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.85%

  [wanxiang]
    句子正确率: 70.97%  (22/31 句完全匹配)
    文字正确率: 93.27%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.91%

  [rime_wanxiang_with_gram]
    句子正确率: 80.65%  (25/31 句完全匹配)
    文字正确率: 96.39%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.96%

  [rime_wubi_sentens_wubi86]
    句子正确率: 77.42%  (24/31 句完全匹配)
    文字正确率: 92.79%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.73%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 100.0%  (31/31 句完全匹配)
    文字正确率: 99.28%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 99.26%

------------------------------------------------------------------------
【语料: test】
  [mingyuepinyin]
    句子正确率: 60.0%  (3/5 句完全匹配)
    文字正确率: 92.06%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.13%

  [mingyuepinyin_with_gram]
    句子正确率: 60.0%  (3/5 句完全匹配)
    文字正确率: 92.06%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.36%

  [rime_ice]
    句子正确率: 80.0%  (4/5 句完全匹配)
    文字正确率: 88.89%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.16%

  [rime_ice_with_gram]
    句子正确率: 80.0%  (4/5 句完全匹配)
    文字正确率: 98.41%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 98.57%

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
    句子正确率: 80.0%  (4/5 句完全匹配)
    文字正确率: 98.41%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 98.95%

  [rime_wubi_sentens_wubi86]
    句子正确率: 40.0%  (2/5 句完全匹配)
    文字正确率: 84.13%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 83.58%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 80.0%  (4/5 句完全匹配)
    文字正确率: 96.83%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.89%

========================================================================
【总耗时】全流程墙钟约 108670.8 ms（多语料）

【各语料耗时】
  · news
    读取文件: 0.16 ms
    分句: 0.16 ms
    预过滤: 0.91 ms
    [mingyuepinyin] 输入串: 2.13 ms, librime 加载: 330.71 ms, 开会话+选方案: 39.92 ms, 逐句解码: 147.67 ms
    [mingyuepinyin_with_gram] 输入串: 2.02 ms, librime 加载: 333.17 ms, 开会话+选方案: 62.72 ms, 逐句解码: 134.31 ms
    [rime_frost] 输入串: 5.09 ms, librime 加载: 1254.18 ms, 开会话+选方案: 110.75 ms, 逐句解码: 1317.26 ms
    [rime_frost_with_gram] 输入串: 11.53 ms, librime 加载: 1245.66 ms, 开会话+选方案: 103.87 ms, 逐句解码: 1396.51 ms
    [rime_ice] 输入串: 2.18 ms, librime 加载: 1091.73 ms, 开会话+选方案: 31.99 ms, 逐句解码: 133.35 ms
    [rime_ice_with_gram] 输入串: 1.85 ms, librime 加载: 1274.16 ms, 开会话+选方案: 59.22 ms, 逐句解码: 260.0 ms
    [rime_wanxiang_with_gram] 输入串: 1.9 ms, librime 加载: 361.66 ms, 开会话+选方案: 1262.75 ms, 逐句解码: 1019.6 ms
    [rime_wubi_sentens_wubi86] 输入串: 79.6 ms, librime 加载: 808.02 ms, 开会话+选方案: 383.75 ms, 逐句解码: 165.23 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 80.04 ms, librime 加载: 806.97 ms, 开会话+选方案: 371.37 ms, 逐句解码: 135.4 ms
    [wanxiang] 输入串: 5.18 ms, librime 加载: 797.59 ms, 开会话+选方案: 2832.74 ms, 逐句解码: 1084.73 ms
  · novel
    读取文件: 0.14 ms
    分句: 0.39 ms
    预过滤: 0.29 ms
    [mingyuepinyin] 输入串: 7.32 ms, librime 加载: 374.19 ms, 开会话+选方案: 31.89 ms, 逐句解码: 339.88 ms
    [mingyuepinyin_with_gram] 输入串: 7.01 ms, librime 加载: 398.21 ms, 开会话+选方案: 19.36 ms, 逐句解码: 286.44 ms
    [rime_frost] 输入串: 7.59 ms, librime 加载: 796.22 ms, 开会话+选方案: 70.25 ms, 逐句解码: 1846.44 ms
    [rime_frost_with_gram] 输入串: 7.23 ms, librime 加载: 768.91 ms, 开会话+选方案: 84.26 ms, 逐句解码: 1892.59 ms
    [rime_ice] 输入串: 8.28 ms, librime 加载: 1057.62 ms, 开会话+选方案: 30.48 ms, 逐句解码: 375.13 ms
    [rime_ice_with_gram] 输入串: 7.12 ms, librime 加载: 1066.85 ms, 开会话+选方案: 31.56 ms, 逐句解码: 330.55 ms
    [rime_wanxiang_with_gram] 输入串: 15.55 ms, librime 加载: 661.3 ms, 开会话+选方案: 3254.54 ms, 逐句解码: 2317.68 ms
    [rime_wubi_sentens_wubi86] 输入串: 22.88 ms, librime 加载: 810.91 ms, 开会话+选方案: 694.33 ms, 逐句解码: 624.87 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 22.74 ms, librime 加载: 818.42 ms, 开会话+选方案: 762.99 ms, 逐句解码: 478.66 ms
    [wanxiang] 输入串: 7.72 ms, librime 加载: 393.31 ms, 开会话+选方案: 3159.53 ms, 逐句解码: 5208.73 ms
  · prose
    读取文件: 0.32 ms
    分句: 0.12 ms
    预过滤: 0.11 ms
    [mingyuepinyin] 输入串: 2.55 ms, librime 加载: 337.83 ms, 开会话+选方案: 17.87 ms, 逐句解码: 126.05 ms
    [mingyuepinyin_with_gram] 输入串: 2.61 ms, librime 加载: 368.57 ms, 开会话+选方案: 43.84 ms, 逐句解码: 86.58 ms
    [rime_frost] 输入串: 2.73 ms, librime 加载: 763.59 ms, 开会话+选方案: 60.75 ms, 逐句解码: 510.41 ms
    [rime_frost_with_gram] 输入串: 2.53 ms, librime 加载: 817.22 ms, 开会话+选方案: 58.87 ms, 逐句解码: 535.64 ms
    [rime_ice] 输入串: 2.51 ms, librime 加载: 1059.02 ms, 开会话+选方案: 43.05 ms, 逐句解码: 128.35 ms
    [rime_ice_with_gram] 输入串: 2.5 ms, librime 加载: 1046.11 ms, 开会话+选方案: 34.65 ms, 逐句解码: 113.79 ms
    [rime_wanxiang_with_gram] 输入串: 2.76 ms, librime 加载: 363.19 ms, 开会话+选方案: 1806.75 ms, 逐句解码: 646.35 ms
    [rime_wubi_sentens_wubi86] 输入串: 6.27 ms, librime 加载: 803.95 ms, 开会话+选方案: 671.17 ms, 逐句解码: 237.91 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 6.11 ms, librime 加载: 821.09 ms, 开会话+选方案: 848.72 ms, 逐句解码: 184.03 ms
    [wanxiang] 输入串: 2.51 ms, librime 加载: 360.59 ms, 开会话+选方案: 1868.79 ms, 逐句解码: 636.17 ms
  · tech
    读取文件: 0.25 ms
    分句: 0.12 ms
    预过滤: 0.08 ms
    [mingyuepinyin] 输入串: 2.17 ms, librime 加载: 398.93 ms, 开会话+选方案: 22.98 ms, 逐句解码: 77.89 ms
    [mingyuepinyin_with_gram] 输入串: 2.28 ms, librime 加载: 319.04 ms, 开会话+选方案: 32.1 ms, 逐句解码: 71.99 ms
    [rime_frost] 输入串: 2.15 ms, librime 加载: 993.43 ms, 开会话+选方案: 146.69 ms, 逐句解码: 851.2 ms
    [rime_frost_with_gram] 输入串: 5.58 ms, librime 加载: 1186.39 ms, 开会话+选方案: 105.13 ms, 逐句解码: 1086.12 ms
    [rime_ice] 输入串: 2.14 ms, librime 加载: 1113.2 ms, 开会话+选方案: 38.34 ms, 逐句解码: 105.33 ms
    [rime_ice_with_gram] 输入串: 2.32 ms, librime 加载: 1054.34 ms, 开会话+选方案: 53.73 ms, 逐句解码: 91.7 ms
    [rime_wanxiang_with_gram] 输入串: 8.56 ms, librime 加载: 581.42 ms, 开会话+选方案: 3766.34 ms, 逐句解码: 930.51 ms
    [rime_wubi_sentens_wubi86] 输入串: 16.56 ms, librime 加载: 1485.02 ms, 开会话+选方案: 783.75 ms, 逐句解码: 414.11 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 14.02 ms, librime 加载: 1488.33 ms, 开会话+选方案: 755.97 ms, 逐句解码: 337.9 ms
    [wanxiang] 输入串: 4.58 ms, librime 加载: 657.9 ms, 开会话+选方案: 3505.59 ms, 逐句解码: 862.59 ms
  · test
    读取文件: 0.23 ms
    分句: 0.03 ms
    预过滤: 0.03 ms
    [mingyuepinyin] 输入串: 1.19 ms, librime 加载: 592.21 ms, 开会话+选方案: 65.88 ms, 逐句解码: 31.5 ms
    [mingyuepinyin_with_gram] 输入串: 0.79 ms, librime 加载: 615.44 ms, 开会话+选方案: 68.96 ms, 逐句解码: 47.33 ms
    [rime_frost] 输入串: 1.36 ms, librime 加载: 1286.07 ms, 开会话+选方案: 126.07 ms, 逐句解码: 132.8 ms
    [rime_frost_with_gram] 输入串: 0.89 ms, librime 加载: 1261.66 ms, 开会话+选方案: 120.4 ms, 逐句解码: 130.04 ms
    [rime_ice] 输入串: 1.4 ms, librime 加载: 2024.12 ms, 开会话+选方案: 59.82 ms, 逐句解码: 63.93 ms
    [rime_ice_with_gram] 输入串: 1.11 ms, librime 加载: 1705.5 ms, 开会话+选方案: 74.15 ms, 逐句解码: 76.59 ms
    [rime_wanxiang_with_gram] 输入串: 0.76 ms, librime 加载: 618.2 ms, 开会话+选方案: 2886.96 ms, 逐句解码: 179.53 ms
    [rime_wubi_sentens_wubi86] 输入串: 4.2 ms, librime 加载: 1486.85 ms, 开会话+选方案: 719.01 ms, 逐句解码: 66.2 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 2.68 ms, librime 加载: 1459.84 ms, 开会话+选方案: 731.47 ms, 逐句解码: 57.82 ms
    [wanxiang] 输入串: 1.52 ms, librime 加载: 592.82 ms, 开会话+选方案: 2944.97 ms, 逐句解码: 138.27 ms

========================================================================
句子正确判定: Top 3 候选中任一项与 gold 完全一致即判对。

同义词归一化（句级完全匹配与 CER 计算前）: 其它→其他；他/她/它→他；的/地/得→的

说明: 分句后仅「纯汉字」且不含 ASCII 数字/英文字母、汉字不少于 5 字的片段参与评测；其它片段已过滤。句子正确率 = 归一化后预测与金句完全一致的比例；文字正确率 = 全语料 (归一化后总字数−总编辑距离)/归一化后总字数。输入串按各 vendor 自身配置生成，可能是连续拼音，也可能是形码前缀串。
```

