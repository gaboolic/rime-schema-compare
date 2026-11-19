# Rime 评测结果

- 生成时间: 2026-11-19 09:02:45 +00:00
- 来源文件: `benchmark_public_articles_2026-11-19_20261119T090007875892Z_report.txt`

## 自动采集与验证

- 语料日期（北京时间）：2026-11-19；采集：2026-11-19T16:59:18.436416+08:00。
- 来源：科技爱好者周刊（GitHub原始整期正文）；选择日期：2026-11-19。
- 源码最近更新时间：2026-11-13T10:22:34Z（不冒充当日发表；最多允许 14 天）。
- 固定源码提交：`7796ff068f5d4a345f96e673999e5d04b49f838d`。
- 实际正文：1 期完整原始 Markdown；包含原刊自带的资讯摘编，不代表外链文章全文；摘要回退 0。
- 署名及使用声明：阮一峰《科技爱好者周刊》，原始Markdown未改写；非商业研究评测用途；版权及许可遵循原作者声明。
- 评测：11 个方案、每方案 199 句；解码失败 0。
- [正文语料](../data/corpus/public_articles_2026-11-19.txt) / [来源元数据](../data/corpus/public_articles_2026-11-19.meta.json)。
- 语料 SHA-256：`1a8edab312ea68a350b85c545ba0f03d0ea767e249443a10055bd8560d9ce7a2`。

| 方案 | 整句正确率 | 文字正确率 |
|------|-----------:|-----------:|
| `mingyuepinyin` | 63.32% | 92.15% |
| `mingyuepinyin_with_gram` | 53.77% | 89.48% |
| `luna_pinyin_with_octagram` | 66.83% | 93.78% |
| `rime_ice` | 69.35% | 93.93% |
| `rime_ice_with_gram` | 74.37% | 95.95% |
| `rime_frost` | 70.85% | 94.27% |
| `rime_frost_with_gram` | 82.91% | 97.38% |
| `wanxiang` | 69.35% | 94.02% |
| `rime_wanxiang_with_gram` | 78.89% | 96.84% |
| `rime_wubi_sentens_wubi86` | 72.36% | 94.72% |
| `rime_wubi_sentens_wubi86_with_gram` | 79.40% | 96.99% |

### 已验证的语言模型

- `mingyuepinyin_with_gram`：`wanxiang-lts-zh-hans.gram`，390786092 字节，SHA-256 `e9ddd501b7d536bc5ea1346f8f900ae49a719a05be349e0a17cb27e717143ca5`。
- `luna_pinyin_with_octagram`：`zh-hant-t-essay-bgw.gram`，41415724 字节，SHA-256 `0488ebd6688f900a39200f2b794f2f99bcbf1e8fc27280ae4a2324b08b1559c1`。
- `rime_ice_with_gram`：`wanxiang-lts-zh-hans.gram`，390786092 字节，SHA-256 `e9ddd501b7d536bc5ea1346f8f900ae49a719a05be349e0a17cb27e717143ca5`。
- `rime_frost_with_gram`：`wanxiang-lts-zh-hans.gram`，390786092 字节，SHA-256 `e9ddd501b7d536bc5ea1346f8f900ae49a719a05be349e0a17cb27e717143ca5`。
- `rime_wanxiang_with_gram`：`wanxiang-lts-zh-hans.gram`，390786092 字节，SHA-256 `e9ddd501b7d536bc5ea1346f8f900ae49a719a05be349e0a17cb27e717143ca5`。
- `rime_wubi_sentens_wubi86_with_gram`：`wanxiang-lts-zh-hans.gram`，390786092 字节，SHA-256 `e9ddd501b7d536bc5ea1346f8f900ae49a719a05be349e0a17cb27e717143ca5`。

公开网页、上游方案和词库随时间变化；以本次保存的语料、来源和提交版本为准。

## Vendor 子模块版本

- `vendor/rime-frost`: `6c2542122acbe325726a2f5a3eb0750b2b6f2109`
- `vendor/rime-ice`: `927e1cf1d3eeb9bf4be85e3f684dba4dd485b6f6`
- `vendor/rime_wanxiang` (`wanxiang`): `386258dd10de102dced6944353380d22d355d553`
- `vendor/rime-wubi-sentence`: `edb9437d18d7d45239fd8f8303ddd836efa69749`
- `vendor/rime-frost_with_gram`: `6c2542122acbe325726a2f5a3eb0750b2b6f2109`
- `vendor/rime_wanxiang_with_gram` (`wanxiang`): `386258dd10de102dced6944353380d22d355d553`

## 评测摘要

```text
========================================================================
Rime 多方案整句评测 — 摘要报告
========================================================================
生成时间 (UTC): 20261119T090007875892Z
rime.dll: D:\a\rime-schema-compare\rime-schema-compare\lib\rime.dll
模式: 单语料 (public_articles_2026-11-19)

语料文件:
  - public_articles_2026-11-19: D:\a\rime-schema-compare\rime-schema-compare\data\corpus\public_articles_2026-11-19.txt

【上游版本: mingyuepinyin】
  rime/rime-luna-pinyin@master: 56b934b099dfbeab842320f13aa8b461a6ab3e42
  rime/rime-prelude@master: 082425ea0684bca36474415d4a0e8db9b016487e
  rime/rime-essay@master: d95eeae056df429ecf993038c325a216f0b28c5b
  rime/rime-stroke@master: 1e8fff9b9494ddec23b0cbc526bcfd8171a6fd48

【上游版本: mingyuepinyin_with_gram】
  rime/rime-luna-pinyin@master: 56b934b099dfbeab842320f13aa8b461a6ab3e42
  rime/rime-prelude@master: 082425ea0684bca36474415d4a0e8db9b016487e
  rime/rime-essay@master: d95eeae056df429ecf993038c325a216f0b28c5b
  rime/rime-stroke@master: 1e8fff9b9494ddec23b0cbc526bcfd8171a6fd48

【上游版本: luna_pinyin_with_octagram】
  rime/rime-luna-pinyin@master: 56b934b099dfbeab842320f13aa8b461a6ab3e42
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
  gaboolic/rime-frost@master: 6c2542122acbe325726a2f5a3eb0750b2b6f2109

【上游版本: rime_frost_with_gram】
  gaboolic/rime-frost@master: 6c2542122acbe325726a2f5a3eb0750b2b6f2109

【上游版本: wanxiang】
  amzxyz/rime_wanxiang@wanxiang: 386258dd10de102dced6944353380d22d355d553

【上游版本: rime_wanxiang_with_gram】
  amzxyz/rime_wanxiang@wanxiang: 386258dd10de102dced6944353380d22d355d553

【上游版本: rime_wubi_sentens_wubi86】
  gaboolic/rime-wubi-sentence@master: edb9437d18d7d45239fd8f8303ddd836efa69749

【上游版本: rime_wubi_sentens_wubi86_with_gram】
  gaboolic/rime-wubi-sentence@master: edb9437d18d7d45239fd8f8303ddd836efa69749

【总体】
  [mingyuepinyin]
    句子正确率: 63.32%  (126/199 句完全匹配)
    文字正确率: 92.15%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.55%

  [mingyuepinyin_with_gram]
    句子正确率: 53.77%  (107/199 句完全匹配)
    文字正确率: 89.48%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.77%

  [luna_pinyin_with_octagram]
    句子正确率: 66.83%  (133/199 句完全匹配)
    文字正确率: 93.78%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.98%

  [rime_ice]
    句子正确率: 69.35%  (138/199 句完全匹配)
    文字正确率: 93.93%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.34%

  [rime_ice_with_gram]
    句子正确率: 74.37%  (148/199 句完全匹配)
    文字正确率: 95.95%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.08%

  [rime_frost]
    句子正确率: 70.85%  (141/199 句完全匹配)
    文字正确率: 94.27%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.48%

  [rime_frost_with_gram]
    句子正确率: 82.91%  (165/199 句完全匹配)
    文字正确率: 97.38%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.4%

  [wanxiang]
    句子正确率: 69.35%  (138/199 句完全匹配)
    文字正确率: 94.02%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.49%

  [rime_wanxiang_with_gram]
    句子正确率: 78.89%  (157/199 句完全匹配)
    文字正确率: 96.84%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 96.83%

  [rime_wubi_sentens_wubi86]
    句子正确率: 72.36%  (144/199 句完全匹配)
    文字正确率: 94.72%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 95.28%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 79.4%  (158/199 句完全匹配)
    文字正确率: 96.99%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 97.17%

========================================================================
【耗时】
  读取文件: 0.15 ms
  分句: 2.55 ms
  预过滤: 2.22 ms
  [luna_pinyin_with_octagram] 输入串: 14.67 ms, librime 加载: 5030.91 ms, 开会话+选方案: 12.38 ms, 逐句解码: 561.39 ms
  [mingyuepinyin] 输入串: 13.71 ms, librime 加载: 5088.46 ms, 开会话+选方案: 12.07 ms, 逐句解码: 514.99 ms
  [mingyuepinyin_with_gram] 输入串: 13.38 ms, librime 加载: 5168.82 ms, 开会话+选方案: 12.33 ms, 逐句解码: 620.93 ms
  [rime_frost] 输入串: 14.54 ms, librime 加载: 16244.26 ms, 开会话+选方案: 23.11 ms, 逐句解码: 2573.93 ms
  [rime_frost_with_gram] 输入串: 14.42 ms, librime 加载: 15998.08 ms, 开会话+选方案: 26.26 ms, 逐句解码: 2841.84 ms
  [rime_ice] 输入串: 21.63 ms, librime 加载: 17536.45 ms, 开会话+选方案: 24.51 ms, 逐句解码: 584.27 ms
  [rime_ice_with_gram] 输入串: 16.43 ms, librime 加载: 17472.63 ms, 开会话+选方案: 24.13 ms, 逐句解码: 714.42 ms
  [rime_wanxiang_with_gram] 输入串: 13.89 ms, librime 加载: 21604.84 ms, 开会话+选方案: 523.11 ms, 逐句解码: 3471.54 ms
  [rime_wubi_sentens_wubi86] 输入串: 150.85 ms, librime 加载: 5584.3 ms, 开会话+选方案: 427.43 ms, 逐句解码: 751.17 ms
  [rime_wubi_sentens_wubi86_with_gram] 输入串: 149.74 ms, librime 加载: 5721.38 ms, 开会话+选方案: 427.93 ms, 逐句解码: 832.02 ms
  [wanxiang] 输入串: 14.45 ms, librime 加载: 22444.69 ms, 开会话+选方案: 562.75 ms, 逐句解码: 3323.28 ms
  写出结果文件: 37.45 ms

========================================================================
句子正确判定: Top 1 候选中任一项与 gold 完全一致即判对。

同义词归一化（句级完全匹配与 CER 计算前）: 其它→其他；他/她/它→他；的/地/得→的

说明: 分句后仅「纯汉字」且不含 ASCII 数字/英文字母、汉字不少于 5 字的片段参与评测；其它片段已过滤。句子正确率 = 归一化后预测与金句完全一致的比例；文字正确率 = 全语料 (归一化后总字数−总编辑距离)/归一化后总字数。输入串按各 vendor 自身配置生成，可能是连续拼音，也可能是形码前缀串。
```
