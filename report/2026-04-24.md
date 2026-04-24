# Rime 评测结果

- 生成时间: 2026-04-24 23:53:45 +08:00
- 来源文件: `benchmark_all_corpus_20260424T155207Z_report.txt`

## Vendor 子模块版本

- `vendor/rime-frost`: `bb9365e0b32da3038de43d30bd016d22ad184270`
- `vendor/rime-ice`: `2bd2983c6c74ea49b3a013f150ade7f3b8a27515`
- `vendor/rime_wanxiang` (`wanxiang`): `618fb082dac7b7e9bb45820811202e881be92bff`
- `vendor/rime-wubi-sentence`: `c3b26af601e41de49227f86633df00985e8d8a77`

## 评测摘要

```text
========================================================================
Rime 多方案整句评测 — 摘要报告
========================================================================
生成时间 (UTC): 20260424T155207Z
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
    句子正确率: 58.13%  (143/246 句完全匹配)
    文字正确率: 91.74%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.84%

  [rime_frost_with_gram]
    句子正确率: 68.7%  (169/246 句完全匹配)
    文字正确率: 94.91%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.98%

  [wanxiang]
    句子正确率: 48.37%  (119/246 句完全匹配)
    文字正确率: 88.89%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.14%

  [rime_wanxiang_with_gram]
    句子正确率: 66.67%  (164/246 句完全匹配)
    文字正确率: 94.84%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.79%

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
    句子正确率: 77.78%  (28/36 句完全匹配)
    文字正确率: 94.65%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.84%

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
    句子正确率: 50.0%  (68/136 句完全匹配)
    文字正确率: 89.7%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.54%

  [rime_frost_with_gram]
    句子正确率: 65.44%  (89/136 句完全匹配)
    文字正确率: 94.05%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.15%

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
    句子正确率: 52.63%  (20/38 句完全匹配)
    文字正确率: 92.07%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.73%

  [rime_frost_with_gram]
    句子正确率: 50.0%  (19/38 句完全匹配)
    文字正确率: 93.5%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.43%

  [wanxiang]
    句子正确率: 34.21%  (13/38 句完全匹配)
    文字正确率: 84.55%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 84.21%

  [rime_wanxiang_with_gram]
    句子正确率: 47.37%  (18/38 句完全匹配)
    文字正确率: 93.5%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.29%

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
    句子正确率: 70.97%  (22/31 句完全匹配)
    文字正确率: 94.71%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.89%

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
【总耗时】全流程墙钟约 97503.09 ms（多语料）

【各语料耗时】
  · news
    读取文件: 0.12 ms
    分句: 0.17 ms
    预过滤: 0.86 ms
    [mingyuepinyin] 输入串: 2.14 ms, librime 加载: 370.34 ms, 开会话+选方案: 34.21 ms, 逐句解码: 106.92 ms
    [mingyuepinyin_with_gram] 输入串: 1.9 ms, librime 加载: 349.25 ms, 开会话+选方案: 16.94 ms, 逐句解码: 124.16 ms
    [rime_frost] 输入串: 1.92 ms, librime 加载: 10412.55 ms, 开会话+选方案: 70.56 ms, 逐句解码: 657.87 ms
    [rime_frost_with_gram] 输入串: 1.93 ms, librime 加载: 620.68 ms, 开会话+选方案: 62.23 ms, 逐句解码: 593.52 ms
    [rime_ice] 输入串: 1.97 ms, librime 加载: 1145.64 ms, 开会话+选方案: 31.62 ms, 逐句解码: 101.74 ms
    [rime_ice_with_gram] 输入串: 1.98 ms, librime 加载: 1097.27 ms, 开会话+选方案: 39.99 ms, 逐句解码: 122.9 ms
    [rime_wanxiang_with_gram] 输入串: 1.96 ms, librime 加载: 374.38 ms, 开会话+选方案: 2796.22 ms, 逐句解码: 1094.44 ms
    [rime_wubi_sentens_wubi86] 输入串: 81.4 ms, librime 加载: 847.5 ms, 开会话+选方案: 388.41 ms, 逐句解码: 118.02 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 80.0 ms, librime 加载: 811.55 ms, 开会话+选方案: 402.28 ms, 逐句解码: 131.55 ms
    [wanxiang] 输入串: 2.11 ms, librime 加载: 14579.08 ms, 开会话+选方案: 1367.7 ms, 逐句解码: 1126.37 ms
  · novel
    读取文件: 0.18 ms
    分句: 0.4 ms
    预过滤: 0.31 ms
    [mingyuepinyin] 输入串: 12.52 ms, librime 加载: 354.6 ms, 开会话+选方案: 21.69 ms, 逐句解码: 212.35 ms
    [mingyuepinyin_with_gram] 输入串: 7.14 ms, librime 加载: 310.18 ms, 开会话+选方案: 36.27 ms, 逐句解码: 255.33 ms
    [rime_frost] 输入串: 7.58 ms, librime 加载: 839.23 ms, 开会话+选方案: 59.99 ms, 逐句解码: 1837.4 ms
    [rime_frost_with_gram] 输入串: 7.7 ms, librime 加载: 621.21 ms, 开会话+选方案: 63.09 ms, 逐句解码: 1850.94 ms
    [rime_ice] 输入串: 7.29 ms, librime 加载: 1125.09 ms, 开会话+选方案: 36.55 ms, 逐句解码: 264.53 ms
    [rime_ice_with_gram] 输入串: 7.86 ms, librime 加载: 1093.77 ms, 开会话+选方案: 33.88 ms, 逐句解码: 313.21 ms
    [rime_wanxiang_with_gram] 输入串: 7.08 ms, librime 加载: 367.98 ms, 开会话+选方案: 1267.69 ms, 逐句解码: 2203.75 ms
    [rime_wubi_sentens_wubi86] 输入串: 22.49 ms, librime 加载: 826.93 ms, 开会话+选方案: 380.89 ms, 逐句解码: 333.38 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 23.02 ms, librime 加载: 829.8 ms, 开会话+选方案: 370.34 ms, 逐句解码: 391.31 ms
    [wanxiang] 输入串: 7.1 ms, librime 加载: 422.24 ms, 开会话+选方案: 1279.42 ms, 逐句解码: 2222.27 ms
  · prose
    读取文件: 0.2 ms
    分句: 0.12 ms
    预过滤: 0.1 ms
    [mingyuepinyin] 输入串: 5.28 ms, librime 加载: 334.9 ms, 开会话+选方案: 31.93 ms, 逐句解码: 72.32 ms
    [mingyuepinyin_with_gram] 输入串: 2.5 ms, librime 加载: 344.82 ms, 开会话+选方案: 18.79 ms, 逐句解码: 77.57 ms
    [rime_frost] 输入串: 2.57 ms, librime 加载: 833.75 ms, 开会话+选方案: 85.36 ms, 逐句解码: 564.99 ms
    [rime_frost_with_gram] 输入串: 2.52 ms, librime 加载: 596.97 ms, 开会话+选方案: 58.87 ms, 逐句解码: 521.54 ms
    [rime_ice] 输入串: 2.51 ms, librime 加载: 1062.03 ms, 开会话+选方案: 31.6 ms, 逐句解码: 86.09 ms
    [rime_ice_with_gram] 输入串: 2.56 ms, librime 加载: 1093.27 ms, 开会话+选方案: 30.24 ms, 逐句解码: 108.91 ms
    [rime_wanxiang_with_gram] 输入串: 2.48 ms, librime 加载: 362.98 ms, 开会话+选方案: 1261.44 ms, 逐句解码: 639.11 ms
    [rime_wubi_sentens_wubi86] 输入串: 6.28 ms, librime 加载: 866.74 ms, 开会话+选方案: 374.99 ms, 逐句解码: 127.97 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 6.29 ms, librime 加载: 839.09 ms, 开会话+选方案: 403.86 ms, 逐句解码: 146.38 ms
    [wanxiang] 输入串: 2.62 ms, librime 加载: 388.62 ms, 开会话+选方案: 1237.04 ms, 逐句解码: 625.2 ms
  · tech
    读取文件: 0.12 ms
    分句: 0.11 ms
    预过滤: 0.07 ms
    [mingyuepinyin] 输入串: 2.29 ms, librime 加载: 318.13 ms, 开会话+选方案: 21.0 ms, 逐句解码: 55.03 ms
    [mingyuepinyin_with_gram] 输入串: 2.94 ms, librime 加载: 320.55 ms, 开会话+选方案: 15.19 ms, 逐句解码: 63.9 ms
    [rime_frost] 输入串: 2.3 ms, librime 加载: 752.05 ms, 开会话+选方案: 58.03 ms, 逐句解码: 391.39 ms
    [rime_frost_with_gram] 输入串: 2.15 ms, librime 加载: 592.32 ms, 开会话+选方案: 71.78 ms, 逐句解码: 399.95 ms
    [rime_ice] 输入串: 2.36 ms, librime 加载: 1088.26 ms, 开会话+选方案: 29.42 ms, 逐句解码: 67.65 ms
    [rime_ice_with_gram] 输入串: 2.13 ms, librime 加载: 1083.81 ms, 开会话+选方案: 38.3 ms, 逐句解码: 107.32 ms
    [rime_wanxiang_with_gram] 输入串: 2.18 ms, librime 加载: 383.19 ms, 开会话+选方案: 1288.61 ms, 逐句解码: 428.25 ms
    [rime_wubi_sentens_wubi86] 输入串: 5.68 ms, librime 加载: 857.75 ms, 开会话+选方案: 372.02 ms, 逐句解码: 116.21 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 5.99 ms, librime 加载: 831.76 ms, 开会话+选方案: 392.72 ms, 逐句解码: 141.78 ms
    [wanxiang] 输入串: 2.16 ms, librime 加载: 367.99 ms, 开会话+选方案: 1301.22 ms, 逐句解码: 391.3 ms
  · test
    读取文件: 0.13 ms
    分句: 0.02 ms
    预过滤: 0.02 ms
    [mingyuepinyin] 输入串: 0.47 ms, librime 加载: 342.03 ms, 开会话+选方案: 35.38 ms, 逐句解码: 8.26 ms
    [mingyuepinyin_with_gram] 输入串: 0.41 ms, librime 加载: 336.09 ms, 开会话+选方案: 33.14 ms, 逐句解码: 10.77 ms
    [rime_frost] 输入串: 0.46 ms, librime 加载: 778.3 ms, 开会话+选方案: 60.64 ms, 逐句解码: 62.96 ms
    [rime_frost_with_gram] 输入串: 0.4 ms, librime 加载: 617.94 ms, 开会话+选方案: 67.27 ms, 逐句解码: 64.47 ms
    [rime_ice] 输入串: 0.4 ms, librime 加载: 1087.74 ms, 开会话+选方案: 37.36 ms, 逐句解码: 26.44 ms
    [rime_ice_with_gram] 输入串: 0.42 ms, librime 加载: 1092.25 ms, 开会话+选方案: 37.89 ms, 逐句解码: 37.16 ms
    [rime_wanxiang_with_gram] 输入串: 0.51 ms, librime 加载: 390.82 ms, 开会话+选方案: 1281.23 ms, 逐句解码: 71.94 ms
    [rime_wubi_sentens_wubi86] 输入串: 2.36 ms, librime 加载: 830.35 ms, 开会话+选方案: 411.63 ms, 逐句解码: 31.92 ms
    [rime_wubi_sentens_wubi86_with_gram] 输入串: 1.32 ms, librime 加载: 822.72 ms, 开会话+选方案: 406.85 ms, 逐句解码: 25.08 ms
    [wanxiang] 输入串: 0.41 ms, librime 加载: 370.31 ms, 开会话+选方案: 1294.25 ms, 逐句解码: 66.08 ms

========================================================================
同义词归一化（句级完全匹配与 CER 计算前）: 其它→其他；他/她/它→他；的/地/得→的

说明: 分句后仅「纯汉字」且不含 ASCII 数字/英文字母、汉字不少于 5 字的片段参与评测；其它片段已过滤。句子正确率 = 归一化后预测与金句完全一致的比例；文字正确率 = 全语料 (归一化后总字数−总编辑距离)/归一化后总字数。输入串按各 vendor 自身配置生成，可能是连续拼音，也可能是形码前缀串。
```

