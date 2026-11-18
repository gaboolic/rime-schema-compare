# 原版朙月拼音 + 原版八股文模型测试

对应 [Issue #1](https://github.com/gaboolic/rime-schema-compare/issues/1)。本次仅测试新增方案，不将旧语料/旧版本的其他方案成绩混入排名。

- 测试时间：2026-11-18 16:48（Asia/Shanghai）
- Vendor：`luna_pinyin_with_octagram`
- 方案：`luna_pinyin_simp`（原版繁体底库、简体输出）
- 模型：`zh-hant-t-essay-bgw.gram`，原版 `grammar:/hant` 参数
- 运行环境：Windows，librime 1.16.1，仓库自带 `lib/rime.dll`
- 语料：[知乎热榜 2026-08-30](../data/corpus/zhihu_hotlist_2026-08-30.txt)
- 用户词库：禁用；输入：连续全拼；取 Top 1；同义词归一化沿用现有评测规则

## 结果

| 指标 | 结果 |
|------|------|
| 参与评测 | 3466 句 |
| 完全匹配 | 1813 句 |
| 整句正确率 | **52.31%** |
| 文字正确率（全语料金文加权，Levenshtein） | **89.46%** |
| 文字正确率（逐句平均） | 89.26% |
| 解码失败 | 0 句 |
| 金文字数 / 编辑距离 | 38027 / 4007 |

## 模型加载验证

已检查编译后的配置：`grammar.language=zh-hant-t-essay-bgw`、`contextual_suggestions=true`、`max_homophones=7`、`max_homographs=7`、`enable_user_dict=false`，未注入 `max_sentences`。日志确认实际加载了模型，而非仅存在文件：

```text
octagram.cc:29] use grammar: zh-hant-t-essay-bgw
gram_db.cc:14] loading gram db: ...\vendor\luna_pinyin_with_octagram\zh-hant-t-essay-bgw.gram
gram_db.cc:44] found double array image of size 10353920.
```

## 上游版本

| 仓库 / 分支 | 提交 |
|-------------|------|
| rime/rime-luna-pinyin / master | `56b934b099dfbeab842320f13aa8b461a6ab3e42` |
| rime/rime-prelude / master | `082425ea0684bca36474415d4a0e8db9b016487e` |
| rime/rime-essay / master | `d95eeae056df429ecf993038c325a216f0b28c5b` |
| rime/rime-stroke / master | `1e8fff9b9494ddec23b0cbc526bcfd8171a6fd48` |
| lotem/rime-octagram-data / master | `8ceef1b42eb77e86501382a52e85c309c0f2f04c` |
| lotem/rime-octagram-data / hant | `97bf55046aad163c3d1881abae5312040b1bbed9` |

## 复现

```bash
python scripts/setup_luna_octagram.py
python scripts/benchmark_sentences.py --vendors luna_pinyin_with_octagram --progress-every 0
```

安装脚本首次下载当前上游，后续复用本地缓存；使用 `--update` 会更新到最新提交，结果可能变化。每次报告都会记录实际使用的上游提交。OpenCC 使用仓库共享数据。

原始结果前缀（位于本地忽略的 `artifacts/`）：`benchmark_zhihu_hotlist_2026-08-30_20261118T084824796342Z`。
