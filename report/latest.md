# Rime 评测结果

- 生成时间: 2026-11-23 07:20:40 +00:00
- 来源文件: `benchmark_public_articles_2026-11-23_20261123T071846201907Z_report.txt`

## 自动采集与验证

- 语料日期（北京时间）：2026-11-23；采集：2026-11-23T15:18:00.739365+08:00。
- 来源：科技爱好者周刊（GitHub原始整期正文）；选择日期：2026-11-23。
- 源码最近更新时间：2026-11-21T15:21:30Z（不冒充当日发表；最多允许 14 天）。
- 固定源码提交：`27f0a24d48d35251e49ff8ec87174a0dee51ee78`。
- 实际正文：1 期完整原始 Markdown；包含原刊自带的资讯摘编，不代表外链文章全文；摘要回退 0。
- 署名及使用声明：阮一峰《科技爱好者周刊》，原始Markdown未改写；非商业研究评测用途；版权及许可遵循原作者声明。
- 评测：11 个方案、每方案 195 句；解码失败 0。
- [正文语料](../data/corpus/public_articles_2026-11-23.txt) / [来源元数据](../data/corpus/public_articles_2026-11-23.meta.json)。
- 语料 SHA-256：`388cb072e9aea69aac0822fea6837557f712c21cbd685c89219e33fb13d86419`。

| 方案 | 整句正确率 | 文字正确率 |
|------|-----------:|-----------:|
| `mingyuepinyin` | 59.49% | 91.10% |
| `mingyuepinyin_with_gram` | 48.72% | 86.02% |
| `luna_pinyin_with_octagram` | 69.74% | 93.99% |
| `rime_ice` | 65.13% | 92.38% |
| `rime_ice_with_gram` | 73.85% | 95.36% |
| `rime_frost` | 69.23% | 93.70% |
| `rime_frost_with_gram` | 79.49% | 96.19% |
| `wanxiang` | 67.18% | 92.91% |
| `rime_wanxiang_with_gram` | 77.44% | 95.70% |
| `rime_wubi_sentens_wubi86` | 71.28% | 95.65% |
| `rime_wubi_sentens_wubi86_with_gram` | 84.10% | 97.80% |

### 已验证的语言模型

- `mingyuepinyin_with_gram`：`wanxiang-lts-zh-hans.gram`，390786092 字节，SHA-256 `e9ddd501b7d536bc5ea1346f8f900ae49a719a05be349e0a17cb27e717143ca5`。
- `luna_pinyin_with_octagram`：`zh-hant-t-essay-bgw.gram`，41415724 字节，SHA-256 `0488ebd6688f900a39200f2b794f2f99bcbf1e8fc27280ae4a2324b08b1559c1`。
- `rime_ice_with_gram`：`wanxiang-lts-zh-hans.gram`，390786092 字节，SHA-256 `e9ddd501b7d536bc5ea1346f8f900ae49a719a05be349e0a17cb27e717143ca5`。
- `rime_frost_with_gram`：`wanxiang-lts-zh-hans.gram`，390786092 字节，SHA-256 `e9ddd501b7d536bc5ea1346f8f900ae49a719a05be349e0a17cb27e717143ca5`。
- `rime_wanxiang_with_gram`：`wanxiang-lts-zh-hans.gram`，390786092 字节，SHA-256 `e9ddd501b7d536bc5ea1346f8f900ae49a719a05be349e0a17cb27e717143ca5`。
- `rime_wubi_sentens_wubi86_with_gram`：`wanxiang-lts-zh-hans.gram`，390786092 字节，SHA-256 `e9ddd501b7d536bc5ea1346f8f900ae49a719a05be349e0a17cb27e717143ca5`。

公开网页、上游方案和词库随时间变化；以本次保存的语料、来源和提交版本为准。

## Vendor 子模块版本

- `vendor/rime-frost`: `ef60dadd8bec975279adc13407bb7642472dffce`
- `vendor/rime-ice`: `927e1cf1d3eeb9bf4be85e3f684dba4dd485b6f6`
- `vendor/rime_wanxiang` (`wanxiang`): `54de9584b584b8965963a16d948923f322f95c69`
- `vendor/rime-wubi-sentence`: `edb9437d18d7d45239fd8f8303ddd836efa69749`
- `vendor/rime-frost_with_gram`: `ef60dadd8bec975279adc13407bb7642472dffce`
- `vendor/rime_wanxiang_with_gram` (`wanxiang`): `54de9584b584b8965963a16d948923f322f95c69`

## 评测摘要

```text
========================================================================
Rime 多方案整句评测 — 摘要报告
========================================================================
生成时间 (UTC): 20261123T071846201907Z
rime.dll: D:\a\rime-schema-compare\rime-schema-compare\lib\rime.dll
模式: 单语料 (public_articles_2026-11-23)

语料文件:
  - public_articles_2026-11-23: D:\a\rime-schema-compare\rime-schema-compare\data\corpus\public_articles_2026-11-23.txt

【上游版本: mingyuepinyin】
  rime/rime-luna-pinyin@master: 84685a7e7793e43278ca29368977b79d74d37a03
  rime/rime-prelude@master: 082425ea0684bca36474415d4a0e8db9b016487e
  rime/rime-essay@master: d95eeae056df429ecf993038c325a216f0b28c5b
  rime/rime-stroke@master: 1e8fff9b9494ddec23b0cbc526bcfd8171a6fd48

【上游版本: mingyuepinyin_with_gram】
  rime/rime-luna-pinyin@master: 84685a7e7793e43278ca29368977b79d74d37a03
  rime/rime-prelude@master: 082425ea0684bca36474415d4a0e8db9b016487e
  rime/rime-essay@master: d95eeae056df429ecf993038c325a216f0b28c5b
  rime/rime-stroke@master: 1e8fff9b9494ddec23b0cbc526bcfd8171a6fd48

【上游版本: luna_pinyin_with_octagram】
  rime/rime-luna-pinyin@master: 84685a7e7793e43278ca29368977b79d74d37a03
  rime/rime-prelude@master: 082425ea0684bca36474415d4a0e8db9b016487e
  rime/rime-essay@master: d95eeae056df429ecf993038c325a216f0b28c5b
  rime/rime-stroke@master: 1e8fff9b9494ddec23b0cbc526bcfd8171a6fd48
  lotem/rime-octagram-data@master: 8ceef1b42eb77e86501382a52e85c309c0f2f04c
  lotem/rime-octagram-data@hant: 97bf55046aad163c3d1881abae5312040b1bbed9

【上游版本: rime_ice】
  iDvel/rime-ice@main: 927e1cf1d3eeb9bf4be85e3f684dba4dd485b6f6

【上游版本: rime_ice_with_gram】
  iDvel/rime-ice@main: 927e1cf1d3eeb9bf4be85e3f684dba4dd485b6f6

【上游版本: rime_frost】
  gaboolic/rime-frost@master: ef60dadd8bec975279adc13407bb7642472dffce

【上游版本: rime_frost_with_gram】
  gaboolic/rime-frost@master: ef60dadd8bec975279adc13407bb7642472dffce

【上游版本: wanxiang】
  amzxyz/rime_wanxiang@wanxiang: 54de9584b584b8965963a16d948923f322f95c69

【上游版本: rime_wanxiang_with_gram】
  amzxyz/rime_wanxiang@wanxiang: 54de9584b584b8965963a16d948923f322f95c69

【上游版本: rime_wubi_sentens_wubi86】
  gaboolic/rime-wubi-sentence@master: edb9437d18d7d45239fd8f8303ddd836efa69749

【上游版本: rime_wubi_sentens_wubi86_with_gram】
  gaboolic/rime-wubi-sentence@master: edb9437d18d7d45239fd8f8303ddd836efa69749

【总体】
  [mingyuepinyin]
    句子正确率: 59.49%  (116/195 句完全匹配)
    文字正确率: 91.1%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.91%

  [mingyuepinyin_with_gram]
    句子正确率: 48.72%  (95/195 句完全匹配)
    文字正确率: 86.02%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 86.92%

  [luna_pinyin_with_octagram]
    句子正确率: 69.74%  (136/195 句完全匹配)
    文字正确率: 93.99%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.45%

  [rime_ice]
    句子正确率: 65.13%  (127/195 句完全匹配)
    文字正确率: 92.38%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.65%

  [rime_ice_with_gram]
    句子正确率: 73.85%  (144/195 句完全匹配)
    文字正确率: 95.36%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.35%

  [rime_frost]
    句子正确率: 69.23%  (135/195 句完全匹配)
    文字正确率: 93.7%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.96%

  [rime_frost_with_gram]
    句子正确率: 79.49%  (155/195 句完全匹配)
    文字正确率: 96.19%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.16%

  [wanxiang]
    句子正确率: 67.18%  (131/195 句完全匹配)
    文字正确率: 92.91%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.14%

  [rime_wanxiang_with_gram]
    句子正确率: 77.44%  (151/195 句完全匹配)
    文字正确率: 95.7%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.85%

  [rime_wubi_sentens_wubi86]
    句子正确率: 71.28%  (139/195 句完全匹配)
    文字正确率: 95.65%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.61%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 84.1%  (164/195 句完全匹配)
    文字正确率: 97.8%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.79%

========================================================================
【耗时】
  读取文件: 0.13 ms
  分句: 1.78 ms
  预过滤: 1.51 ms
  [luna_pinyin_with_octagram] 输入串: 15.49 ms, librime 加载: 3922.29 ms, 开会话+选方案: 9.68 ms, 逐句解码: 425.85 ms
  [mingyuepinyin] 输入串: 10.39 ms, librime 加载: 3965.1 ms, 开会话+选方案: 9.52 ms, 逐句解码: 400.9 ms
  [mingyuepinyin_with_gram] 输入串: 10.58 ms, librime 加载: 4004.47 ms, 开会话+选方案: 9.38 ms, 逐句解码: 472.56 ms
  [rime_frost] 输入串: 10.06 ms, librime 加载: 12706.65 ms, 开会话+选方案: 19.99 ms, 逐句解码: 1846.23 ms
  [rime_frost_with_gram] 输入串: 10.46 ms, librime 加载: 12593.36 ms, 开会话+选方案: 18.28 ms, 逐句解码: 1906.64 ms
  [rime_ice] 输入串: 10.24 ms, librime 加载: 14568.05 ms, 开会话+选方案: 20.04 ms, 逐句解码: 404.42 ms
  [rime_ice_with_gram] 输入串: 10.2 ms, librime 加载: 14177.38 ms, 开会话+选方案: 19.28 ms, 逐句解码: 524.27 ms
  [rime_wanxiang_with_gram] 输入串: 10.04 ms, librime 加载: 12626.11 ms, 开会话+选方案: 379.71 ms, 逐句解码: 2444.22 ms
  [rime_wubi_sentens_wubi86] 输入串: 107.54 ms, librime 加载: 4587.45 ms, 开会话+选方案: 327.86 ms, 逐句解码: 524.59 ms
  [rime_wubi_sentens_wubi86_with_gram] 输入串: 105.36 ms, librime 加载: 4540.41 ms, 开会话+选方案: 331.34 ms, 逐句解码: 592.26 ms
  [wanxiang] 输入串: 10.3 ms, librime 加载: 12493.86 ms, 开会话+选方案: 380.49 ms, 逐句解码: 2278.23 ms
  写出结果文件: 24.85 ms

========================================================================
句子正确判定: Top 1 候选中任一项与 gold 完全一致即判对。

同义词归一化（句级完全匹配与 CER 计算前）: 其它→其他；他/她/它→他；的/地/得→的

说明: 分句后仅「纯汉字」且不含 ASCII 数字/英文字母、汉字不少于 5 字的片段参与评测；其它片段已过滤。句子正确率 = 归一化后预测与金句完全一致的比例；文字正确率 = 全语料 (归一化后总字数−总编辑距离)/归一化后总字数。输入串按各 vendor 自身配置生成，可能是连续拼音，也可能是形码前缀串。
```
