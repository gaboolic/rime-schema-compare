# Rime 评测结果

- 生成时间: 2026-11-18 17:47:48 +08:00
- 来源文件: `benchmark_zhihu_hotlist_2026-11-18_20261118T094153649792Z_report.txt`

## 正文语料与核查

本报告已替换此前的标题/摘要初测，使用 **20 个热榜问题标题 + 60 条实际回答正文**（每题 3 条），无摘要回退。正文共 54184 字符；按仓库既有分句、过滤及归一化规则，最终评测 **2762 句、27787 个金文汉字**。

- [正文语料](../data/corpus/zhihu_hotlist_2026-11-18.txt) / [采集元数据及 60 条回答来源](../data/corpus/zhihu_hotlist_2026-11-18.meta.json)。最终采集时间：2026-11-18 17:41:24 +08:00。
- 语料 SHA-256：`e99624cd4f2168770d761bee2c8dd64f48f041d6a1df30e9c1d4892dbac3941e`；大小 157915 字节。
- 热榜来自 [UApi 知乎热榜接口](https://uapis.cn/api/v1/misc/hotboard?type=zhihu)；该接口实际返回 20 个问题。回答来自知乎页面实际渲染的回答 DOM，不是问题摘要或第三方文章。
- 已解决当前环境的匿名正文抓取问题：Playwright 使用本机 Chrome 157、有界面、独立持久化会话、原生 UA/client hints 和首页预热。旧脚本固定 Chrome 126 UA 并伪造多个 JS 属性；仅使用原脚本或普通匿名 HTTP 请求会返回 403。初始 403 也可能在页面 JS 执行后正常渲染，故以回答 DOM 为准。
- 已验证正文提取保留原生文本中的 `<`、`>` 和实体字面量，不把 DOM innerText 当 HTML 再清洗。采集期间回答顺序/内容会变化，以已保存语料及哈希为准。
- 全部 11 项均有 2762 句可用输入、解码失败 0 句；已核对禁用用户词库、编译模型配置及 6 个带模型项的实际加载日志。
- `*_with_gram` 统一使用上游 LTS 当前附件（2026-11-14 更新），大小 407160876 字节，SHA-256：`d4f64356231764ff27b79c9b0db79cd9d665013464cf5544e2fbd9a71e0f1c5a`。原版朙月八股文项仍用原版 hant 参数与模型。
- 环境告警：五笔方案仍报告可选 `big_char_set` 配置及英文/日文词表缺失；此前首次编译白霜时有少量游戏词条编码告警。本次纯汉字解码全部成功，不代表上游所有功能零告警。

## 快速结果

| 方案 | 整句正确率 | 文字正确率 |
|------|-----------:|-----------:|
| 明月拼音（无模型） | 57.06% | 89.82% |
| 明月拼音 + 万象模型 | 49.60% | 87.16% |
| 原版朙月 + 原版八股文 hant | 62.71% | 92.21% |
| 雾凇拼音（无模型） | 60.43% | 91.29% |
| 雾凇拼音 + 万象模型 | 67.96% | 93.06% |
| 白霜拼音（无模型） | 68.90% | 93.78% |
| 白霜拼音 + 万象模型 | **74.48%** | **95.06%** |
| 万象拼音（无模型） | 65.10% | 92.59% |
| 万象拼音 + 万象模型 | 72.34% | 94.43% |
| 五笔整句（无模型） | 60.32% | 92.13% |
| 五笔整句 + 万象模型 | 70.85% | 94.98% |

## 复现命令

```powershell
python scripts/download_zhihu_hotlist.py --headed --browser-channel chrome --profile-dir .cache/zhihu-browser --require-bodies --answers 3
./scripts/run_test.ps1 -Corpus data/corpus/zhihu_hotlist_2026-11-18.txt -ArtifactsDir artifacts/2026-11-18-full-bodies-v2
```

重新抓取可能使热榜和回答内容变化；精确复现本次成绩应使用已保存语料及下列上游提交，不重新下载。浏览器会话目录包含 Cookie，不应分享或提交。

## Vendor 子模块版本

- `vendor/rime-frost`: `8c3a3862e68779f837461c3aa79caaa225eb144e`
- `vendor/rime-ice`: `927e1cf1d3eeb9bf4be85e3f684dba4dd485b6f6`
- `vendor/rime_wanxiang` (`wanxiang`): `aca3d3c807609d38f15db2d26495b0aa81a3e2df`
- `vendor/rime-wubi-sentence`: `edb9437d18d7d45239fd8f8303ddd836efa69749`

## 评测摘要

```text
========================================================================
Rime 多方案整句评测 — 摘要报告
========================================================================
生成时间 (UTC): 20261118T094153649792Z
rime.dll: D:\vscode\rime_projs\rime-schema-compare\lib\rime.dll
模式: 单语料 (zhihu_hotlist_2026-11-18)

语料文件:
  - zhihu_hotlist_2026-11-18: D:\vscode\rime_projs\rime-schema-compare\data\corpus\zhihu_hotlist_2026-11-18.txt

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
  gaboolic/rime-frost@master: 8c3a3862e68779f837461c3aa79caaa225eb144e

【上游版本: rime_frost_with_gram】
  gaboolic/rime-frost@master: 8c3a3862e68779f837461c3aa79caaa225eb144e

【上游版本: wanxiang】
  amzxyz/rime_wanxiang@wanxiang: aca3d3c807609d38f15db2d26495b0aa81a3e2df

【上游版本: rime_wanxiang_with_gram】
  amzxyz/rime_wanxiang@wanxiang: aca3d3c807609d38f15db2d26495b0aa81a3e2df

【上游版本: rime_wubi_sentens_wubi86】
  gaboolic/rime-wubi-sentence@master: edb9437d18d7d45239fd8f8303ddd836efa69749

【上游版本: rime_wubi_sentens_wubi86_with_gram】
  gaboolic/rime-wubi-sentence@master: edb9437d18d7d45239fd8f8303ddd836efa69749

【总体】
  [mingyuepinyin]
    句子正确率: 57.06%  (1576/2762 句完全匹配)
    文字正确率: 89.82%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 89.97%

  [mingyuepinyin_with_gram]
    句子正确率: 49.6%  (1370/2762 句完全匹配)
    文字正确率: 87.16%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 87.35%

  [luna_pinyin_with_octagram]
    句子正确率: 62.71%  (1732/2762 句完全匹配)
    文字正确率: 92.21%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.96%

  [rime_ice]
    句子正确率: 60.43%  (1669/2762 句完全匹配)
    文字正确率: 91.29%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 91.28%

  [rime_ice_with_gram]
    句子正确率: 67.96%  (1877/2762 句完全匹配)
    文字正确率: 93.06%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.95%

  [rime_frost]
    句子正确率: 68.9%  (1903/2762 句完全匹配)
    文字正确率: 93.78%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 93.7%

  [rime_frost_with_gram]
    句子正确率: 74.48%  (2057/2762 句完全匹配)
    文字正确率: 95.06%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.92%

  [wanxiang]
    句子正确率: 65.1%  (1798/2762 句完全匹配)
    文字正确率: 92.59%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.49%

  [rime_wanxiang_with_gram]
    句子正确率: 72.34%  (1998/2762 句完全匹配)
    文字正确率: 94.43%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.26%

  [rime_wubi_sentens_wubi86]
    句子正确率: 60.32%  (1666/2762 句完全匹配)
    文字正确率: 92.13%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 92.1%

  [rime_wubi_sentens_wubi86_with_gram]
    句子正确率: 70.85%  (1957/2762 句完全匹配)
    文字正确率: 94.98%  (全语料金文加权，基于 Levenshtein)
    文字正确率(逐句平均): 94.83%

========================================================================
【耗时】
  读取文件: 10.73 ms
  分句: 8.91 ms
  预过滤: 70.27 ms
  [luna_pinyin_with_octagram] 输入串: 498.18 ms, librime 加载: 340.62 ms, 开会话+选方案: 35.64 ms, 逐句解码: 14044.98 ms
  [mingyuepinyin] 输入串: 200.18 ms, librime 加载: 133.01 ms, 开会话+选方案: 17.87 ms, 逐句解码: 9115.5 ms
  [mingyuepinyin_with_gram] 输入串: 438.23 ms, librime 加载: 326.14 ms, 开会话+选方案: 52.77 ms, 逐句解码: 13359.24 ms
  [rime_frost] 输入串: 296.75 ms, librime 加载: 2040.62 ms, 开会话+选方案: 57.56 ms, 逐句解码: 54042.84 ms
  [rime_frost_with_gram] 输入串: 296.11 ms, librime 加载: 1852.34 ms, 开会话+选方案: 44.56 ms, 逐句解码: 53452.81 ms
  [rime_ice] 输入串: 341.93 ms, librime 加载: 2200.72 ms, 开会话+选方案: 77.89 ms, 逐句解码: 11158.7 ms
  [rime_ice_with_gram] 输入串: 294.12 ms, librime 加载: 2054.13 ms, 开会话+选方案: 51.18 ms, 逐句解码: 13699.68 ms
  [rime_wanxiang_with_gram] 输入串: 370.27 ms, librime 加载: 799.34 ms, 开会话+选方案: 1095.27 ms, 逐句解码: 63383.3 ms
  [rime_wubi_sentens_wubi86] 输入串: 1626.33 ms, librime 加载: 1770.19 ms, 开会话+选方案: 756.58 ms, 逐句解码: 14431.58 ms
  [rime_wubi_sentens_wubi86_with_gram] 输入串: 1509.89 ms, librime 加载: 2777.62 ms, 开会话+选方案: 718.22 ms, 逐句解码: 15916.78 ms
  [wanxiang] 输入串: 344.8 ms, librime 加载: 931.05 ms, 开会话+选方案: 1186.75 ms, 逐句解码: 60990.98 ms
  写出结果文件: 939.16 ms

========================================================================
句子正确判定: Top 1 候选中任一项与 gold 完全一致即判对。

同义词归一化（句级完全匹配与 CER 计算前）: 其它→其他；他/她/它→他；的/地/得→的

说明: 分句后仅「纯汉字」且不含 ASCII 数字/英文字母、汉字不少于 5 字的片段参与评测；其它片段已过滤。句子正确率 = 归一化后预测与金句完全一致的比例；文字正确率 = 全语料 (归一化后总字数−总编辑距离)/归一化后总字数。输入串按各 vendor 自身配置生成，可能是连续拼音，也可能是形码前缀串。
```
