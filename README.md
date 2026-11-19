# rime-schema-compare

用 **Python + librime** 对比多套 Rime 词库方案的 **整句解码准确率**。[librime](https://github.com/rime/librime)
当前 `librime` 进程内评测支持 **Windows / macOS / Linux**，会按平台自动查找动态库：Windows 使用 `rime.dll`，macOS 使用 `librime*.dylib`，Linux 使用 `librime.so*`。

## 最新评测结果 

[2026-11-18：原版朙月拼音 + 原版八股文专项测试](report/2026-11-18-luna-octagram.md)（Issue #1，3466 句，整句正确率 52.31%，文字正确率 89.46%）。

会定期替换语料来测试。语料分几种，1当天随便找的新闻/当天的知乎热榜 2随便找的小说网站点开排行榜找一个 3随便搜一个文艺一点的散文 4侧重新科技的文章

[查看rime多方案最新评测结果（调用librime）](report/latest.md)

[查看其他windows输入法最新评测结果（黑盒模拟按键的方式测试）](report/other_latest.md)

最新评测结果表明，[白霜拼音](https://github.com/gaboolic/rime-frost)以及[万象拼音](https://github.com/amzxyz/rime_wanxiang)使用ngrams模型均超越了微软拼音。

[2026.4.25日评测结果](report/2026-04-25.md)，[白霜拼音](https://github.com/gaboolic/rime-frost)在不使用模型时领先其他方案；使用模型时，已超越商业输入法的准确率（[白霜拼音用模型]句子正确率: 71.54% (176/246 句完全匹配)，手心输入法句子正确率: 71.14%  (175/246 句完全匹配)）。


[查看rime多方案top3正确率最新评测结果（调用我修改的librime）](report/top3_latest.md) 我修改的librime：https://github.com/gaboolic/librime 修改了组句算法，支持输出多个整句候选

## 各套方案说明

默认参与对比的方案在 `src/rime_schema_compare/config.py` 的 `DEFAULT_VENDORS` 中定义：每个条目包含 **vendor 键**（命令行与报表列名）、**子目录**、以及 **主 schema_id**（librime 里选用的方案 ID）。

默认对比的基础方案均按“**无语言模型、无用户词库**”口径评测：不额外挂载 `.gram` 模型文件，且评测前会清理 `userdb` 并通过 `custom.yaml` 禁用 `translator/enable_user_dict`。现有 `*_with_gram` 变体统一复用同一个 [`wanxiang-lts-zh-hans.gram`](https://github.com/amzxyz/RIME-LMDG/releases)，仅在各自方案目录下额外挂载该语言模型，其余仍保持禁用用户词库。

| Vendor 键 | 目录 | 主 schema | 说明 |
|-----------|------|-----------|------|
| `mingyuepinyin` | `vendor/mingyuepinyin` | `luna_pinyin_simp` | 明月拼音（简体全拼），与 Rime 自带 Luna 系方案同源的一类发行 |
| `mingyuepinyin_with_gram` | `vendor/mingyuepinyin_with_gram` | `luna_pinyin_simp` | 带 `wanxiang-lts-zh-hans` ngram 模型的明月拼音；其余配置与 `vendor/mingyuepinyin` 保持一致 |
| `luna_pinyin_with_octagram` | `vendor/luna_pinyin_with_octagram` | `luna_pinyin_simp` | 原版 `rime/rime-luna-pinyin` + 原版八股文 `zh-hant-t-essay-bgw`，简体输出，保留上游模型参数 |
| `rime_ice` | `vendor/rime-ice` | `rime_ice` | 雾凇拼音 |
| `rime_ice_with_gram` | `vendor/rime-ice_with_gram` | `rime_ice` | 带 `wanxiang-lts-zh-hans` ngram 模型的雾凇拼音；其余配置与 `vendor/rime-ice` 保持一致 |
| `rime_frost` | `vendor/rime-frost` | `rime_frost` | 白霜拼音（rime-frost） |
| `rime_frost_with_gram` | `vendor/rime-frost_with_gram` | `rime_frost` | 带 `wanxiang-lts-zh-hans` ngram 模型的白霜拼音；其余配置与 `vendor/rime-frost` 保持一致 |
| `wanxiang` | `vendor/rime_wanxiang` | `wanxiang` | 万象拼音（子模块跟踪分支 `wanxiang`，见 [.gitmodules](.gitmodules)） |
| `rime_wanxiang_with_gram` | `vendor/rime_wanxiang_with_gram` | `wanxiang` | 带 `ngrams` 模型文件的万象拼音；其余配置与 `vendor/rime_wanxiang` 保持一致 |
| `rime_wubi_sentens_wubi86` | `vendor/rime-wubi-sentence` | `wubi86` | `gaboolic/rime-wubi-sentence` 的五笔整句 `wubi86` 方案；输入串按单字形码表取前 2 码连续拼接 |
| `rime_wubi_sentens_wubi86_with_gram` | `vendor/rime-wubi-sentence_with_gram` | `wubi86` | 带 `wanxiang-lts-zh-hans` ngram 模型的五笔整句 `wubi86` 方案；其余配置与 `vendor/rime-wubi-sentence` 保持一致 |

各方案的实际 YAML、编译产物与用户状态都放在各自的 `vendor/...` 目录下；所有方案共用的只读资源放在 [`vendor/data`](vendor/data)（不存在会自动创建）。需要让所有方案看到同一套程序级配置或补丁时，把文件放在 `vendor/data`（例如从小狼毫安装目录复制或做符号链接）。

## 如何执行评测脚本

### 前置条件

- 已安装可用的 **librime** 运行环境，且动态库及其依赖可被加载：
  - Windows：`rime.dll`（例如小狼毫自带）
  - macOS：`librime*.dylib`
  - Linux：`librime.so*`
- **Python 3.10+** 建议。
- **Git 子模块** 已拉取（首次体积较大）：

```bash
git submodule update --init --recursive --depth 1
```

### 原版朙月拼音 + 原版八股文（Issue #1）

首次运行默认评测前，安装这一独立测试项：

```bash
python scripts/setup_luna_octagram.py
```

脚本从官方 `rime/rime-luna-pinyin` 及其 `prelude`、`essay`、`stroke` 依赖取得原版资源，从 `lotem/rime-octagram-data` 的主分支取得 `grammar.yaml`，从 `hant` 分支取得 `zh-hant-t-essay-bgw.gram`。资源安装到独立目录，不改写现有明月拼音或万象模型测试项。需要 Git 和网络；重复执行复用缓存，更新上游用 `--update`。

测试采用 `luna_pinyin_simp`：只将输出转换为简体，底层仍是原版繁体词典，因此使用 `grammar:/hant`，不是 `hans` 模型。保留上游的 contextual suggestions、max_homophones=7、max_homographs=7 等参数，不注入其他方案的候选参数；仅按评测口径禁用用户词库。需要 librime 支持 `librime-octagram`，并提供 OpenCC 的 `t2s.json` 等数据（本仓库放在 `vendor/data/opencc`）。

单独测试：

```bash
python scripts/benchmark_sentences.py --vendors luna_pinyin_with_octagram
```

安装后默认全方案评测也会包含该项；缺少资源时会明确报错，避免悄悄跑成无模型结果。上游提交记录保存在该测试目录的 `upstream_versions.json`，并写入摘要报告。现有每周评测流程会在评测前安装/更新此项，无需另外创建定时任务。

### 安装依赖

```bash
pip install -r requirements.txt
```


### 运行命令

通过 `librime` 测试各个 Rime 输入方案，推荐直接运行 Python CLI；仓库会按当前系统自动解析动态库，也可手动用 `RIME_LIBRARY`（兼容旧变量 `RIME_DLL`）指定绝对路径：

```bash
python scripts/benchmark_sentences.py
python scripts/benchmark_sentences.py --corpus data/corpus/news.txt
RIME_LIBRARY=/absolute/path/to/librime python scripts/benchmark_sentences.py
```

Windows 下也可以继续使用 PowerShell 入口：

```
./scripts/run_test.ps1
# 指定本次语料，避免与 data/corpus 中的历史语料混跑：
./scripts/run_test.ps1 -Corpus data/corpus/zhihu_hotlist_2026-11-18.txt
```

### 无需登录的公开正文（当前自动评测来源）

自动评测默认使用 **GitHub 托管的《科技爱好者周刊》最新一期完整原始 Markdown**，不再依赖知乎域名、网页登录或正文摘要接口：

```bash
python scripts/download_public_articles.py --source github-weekly --out data/corpus/public_articles_2026-11-19.txt
```

来源为 [ruanyf/weekly](https://github.com/ruanyf/weekly)：先固定目录索引的提交，再选最新期号、固定对应正文提交，保存该文件的完整原始 Markdown，不改写、不把外链文章摘要冒充外链全文。默认只选最新 1 期，而不是当天 5 篇新闻；原刊本身含有资讯摘编，报告会注明。下载器只访问 GitHub API 和 GitHub 原始文件域名，不请求文章内的外链，也不下载图片。无需浏览器、知乎 Cookie 或 Access Secret；Actions 使用自动提供的 `GITHUB_TOKEN` 读 GitHub API（仅发送到 API 主机），无需配置个人凭据。可用 `--date YYYY-MM-DD` 指定本次选择日期，默认北京时间当天；源码更新时间允许早于选择日期，但不得超过 14 天，也不得来自未来。

保留 `--source zhihu-daily` 作为可选手动来源。日报 API `news-at.zhihu.com` 在部分境外 DNS 下会指向失效别名；虽然本地通过 AliDNS 回退可用，官方 runner 实测仍可能解析失败，因此它不再是 CI 默认来源。可选回退始终保留原始主机名的证书/SNI 校验，不固定 IP、不改系统 DNS、不接受私网目标，也不会关闭 HTTPS 验证。

语料旁的元数据分别记录选择/采集日期、源码最近更新时间（不冒充首次发表日期）、固定提交、原始链接、正文/语料 SHA-256 和署名。原始 Markdown 保持未改写；缺失正文、超龄、哈希或来源不符时不覆盖已有语料。作者博客声明的非商用、保持署名等许可要求仍需遵守；抓取用于研究评测不等于可以自由改编或商业转载，原文也不会因进入语料目录而变成项目代码的许可证。

Tophub 可以作为榜单目录，但它的知乎热榜只提供标题和原链接，不能解决知乎回答登录限制；当前正文来源不依赖 Tophub 或知乎开放平台鉴权。报告默认明确标注“科技爱好者周刊完整原始正文”，不称为“知乎热榜回答”或“当日新闻”。

### 获取知乎热榜回答正文（保留的手动工具，非 CI 默认）

安装 Playwright 后，可使用本机 Chrome 和独立持久化会话抓取公开回答：

```bash
pip install playwright
python scripts/download_zhihu_hotlist.py --headed --browser-channel chrome --profile-dir .cache/zhihu-browser --require-bodies --answers 3
```

需要本机已安装 Chrome；也支持 `--browser-channel msedge`，默认 `chromium` 则需先执行 `playwright install chromium`。浏览器使用原生 UA 和 client hints，不再固定冒充 Chrome 126；先访问首页建立正常会话，再等待回答 DOM。初始 HTTP 403 可能只是 JS challenge，不能仅凭状态码判断最终失败；若仍出现登录或验证要求，需要人工处理，不会绕过。

输出语料旁会生成 `.meta.json`，记录实际回答数、来源链接和语料哈希。`--require-bodies` 在一条回答也未取得时会报错并保留原语料，避免把摘要测试误当正文测试。部分问题失败时仍可能回退到摘要，须检查元数据的 `fallback_questions`。持久化目录可能包含会话 Cookie，不要提交或分享，也不要指定日常 Chrome 用户目录。

### 每周自动采集、评测与发布（GitHub Actions）

[Weekly Benchmark Report](.github/workflows/weekly-report.yml) 在**北京时间每周一 08:00**执行（cron `0 0 * * 1` 使用 UTC；GitHub 可能延迟启动），也可在仓库 Actions 页面手动选择 **Run workflow**。配置需先进入默认分支 `main` 才会按时运行。

另有 [Public Article Source Check](.github/workflows/public-source-smoke.yml)：相关采集代码推送到 `main` 时，会自动在官方 Windows runner 上执行离线测试和与生产一致的最新一期完整周刊下载；只读权限，不下载模型、不发布报告，诊断附件保留 7 天。失败会把具体 DNS、TLS 或超时原因写到任务 Annotations，避免把网络故障统一隐藏成一个错误。正文采集检查通过不等于完整 11 方案评测已在云端完成。

流程首先验证并下载 **GitHub 上最新一期周刊完整原始正文**；采集成功后更新所有方案子模块，用 [`setup_benchmark_vendors.py`](scripts/setup_benchmark_vendors.py) 从同一源码版本重建带模型副本、安装官方朙月/八股文并下载校验当前万象 LTS 模型，再对当天语料跑全部 11 个默认测试项。模型缓存每次都根据上游当前附件的大小与 SHA-256 校验，不会静默沿用旧模型。

报告先生成在运行专属的 `artifacts/weekly-...` 暂存目录；[`validate_weekly_benchmark.py`](scripts/validate_weekly_benchmark.py) 会验证选择/采集日期属于当天（北京时间）、源码更新时间不超过 14 天、固定提交及原始正文完整一致、文章来源 URL 和正文哈希、无摘要回退、语料/模型哈希、11 项齐全、每项至少 20 句、没有缺码或解码失败，以及实际编译模型和禁用用户词库配置。全部通过后才更新 `report/latest.md`、当天报告，并自动提交当天正文/来源元数据和方案版本到 `main`。失败保留远端旧报告，成功/失败均上传运行日志和原始结果（保留 30 天），不上传浏览器 Cookie 或 profile。

周刊每周更新，而不是每天发布；采集日和源码更新时间均会明确展示。语料种类及评测句数变化会影响成绩，不能直接与旧的知乎热榜回答或日报语料成绩比较。采集失败时仍保留下载日志和逐篇诊断，不会发布摘要替代正文。

**使用 GitHub 官方托管的 `windows-latest`，不需要自托管 runner，也不需要个人电脑保持开机。**

公开仓库使用 GitHub 官方**标准 runner 的计算用量免费**（[官方说明](https://docs.github.com/en/actions/reference/runners/github-hosted-runners#standard-github-hosted-runners-for-public-repositories)）；本流程没有选择收费的 larger runner。[官方 Windows 镜像](https://github.com/actions/runner-images/blob/main/images/windows/Windows2025-Readme.md) 已预装 Git 和 PowerShell，Python 依赖由流程安装，librime 使用仓库内的 Windows 运行库。每次运行都会验证 librime 的 octagram 模块；自动采集不安装 Playwright、不启动 Chrome，也不需要桌面或登录会话。仓库与子模块使用浅克隆，减少官方 runner 的磁盘占用。

1. 确认仓库 **Actions** 已启用，并在 **Settings → Actions → General → Workflow permissions** 允许写入仓库；如 `main` 有分支保护，应允许自动提交，或改为提交 PR 的发布方式。无需个人访问令牌，但组织策略可能限制 `GITHUB_TOKEN` 写入。
2. 首次建议手动运行一次，验证官方 runner 上的完整链路。外部公开接口仍可能暂时不可用；遇到网络错误、源码超过 14 天未更新或正文不完整时，流程会失败并保留旧报告，不会用摘要冒充正文发布。
3. 每次任务使用独立的临时 Windows 环境；无需注册 runner、配置本地自动登录或运行 `run.cmd`。

自动流程不创建浏览器 profile，也不接收知乎登录凭据。保留的手动浏览器下载工具独立于 CI，其 profile 不应提交或分享。该定时任务不运行需要前台焦点的系统输入法黑盒测试。

### 运行 Windows 拼音输入法黑盒评测

Windows 下可单独跑系统/第三方拼音输入法的 GUI 黑盒评测。推荐使用通用入口：

```bash
python scripts/benchmark_windows_pinyin.py --ime microsoft_pinyin
python scripts/benchmark_windows_pinyin.py --ime microsoft_pinyin --corpus data/corpus/news.txt
python scripts/benchmark_windows_pinyin.py --ime sogou_pinyin
python scripts/benchmark_windows_pinyin.py --ime microsoft_pinyin sogou_pinyin
```

也可以用 PowerShell 入口一次同时评测微软拼音和搜狗拼音，并生成 `report/other_latest.md`：

```bash
./scripts/run_blackbox_test.ps1
```

默认口径固定为：

- 宿主程序是 `Notepad`
- 输入法由 `--ime` 指定，目前支持 `microsoft_pinyin`、`sogou_pinyin`
- 先预处理全部语料，再按输入法整批运行；例如先完整跑微软拼音，再完整跑搜狗拼音
- 对每句发送**连续全拼**
- 按 `Space` 提交第 1 候选
- 读取最终上屏文本，统计整句准确率与字级准确率

注意：

- 这是 **Windows 系统输入法黑盒评测**，不是像 `librime` 那样的进程内调用。
- 结果会受到 **Windows 版本、输入法版本、是否联网、个性化词频、当前系统输入法状态** 的影响。
- 跑黑盒评测时需要保持前台焦点稳定，不要手动切窗口或输入。
- 当前脚本会先解析系统里的 `InputMethodTips`，再切换到目标输入法；默认通过 Windows API 设置目标输入法并校验已切到正确 profile。若机器上的输入法顺序或系统行为有变化，黑盒结果仍可能出现波动。

### 输出文件（`artifacts/`）

未指定 `--corpus` 时，文件名前缀一般为 `benchmark_all_corpus_<时间戳>`；单语料时为 `benchmark_<语料标签>_<时间戳>`。

| 文件 | 内容 |
|------|------|
| `*_*.csv` | 宽表：每句一行，`gold` 后接各方案各自的 `*_input` / 句子是否判对 / 单句字级准确率 / 预测 / 错误信息 |
| `*_long.csv` | 窄表：每句 × 每方案一行；含该方案实际输入串 `input`，行序为先方案后句子 |
| `*_long_by_sentence.csv` | 同上结构；行序为先句子后方案 |
| `*_scheme_compare.txt` | 各方案**独有判对**及相对其它方案的**多判对**句子列表，并附对应方案的预测结果对比 |
| `*_summary.csv` | 按语料 × 方案汇总 |
| `*_report.txt` | 中文摘要：句子正确率、文字正确率等 |
| `*.json` | 完整 JSON（含窄表级 `per_sentence`） |

进度与阶段日志在 **stderr**（简体中文 Windows 控制台多为 GBK，避免乱码勿强行把 stderr 设为 UTF-8）。阶段前缀包括：`[启动]`、`[语料列表]`、`[分句]`、`[预过滤]`、`[输入串 x]`、`[librime:加载方案 x]`、`[librime:解码 x]`、`[汇总]`、`[写出结果]` 等。若使用 UTF-8 终端（如 `chcp 65001`），stderr 中的中文通常也能正常显示。

## 评测细节

### 指标与同义词

对每条参与评测的句子，用 **整句是否完全一致** 统计句子级准确率；字级用 **Levenshtein 编辑距离** 汇总得到 macro CER（总编辑量 / 金文总字数）。比较前可做 **同义词归一化**（默认规则 + `data/eval_synonyms.json`，例如 其它→其他、他/她/它→他、的/地/得→的），可用 `--eval-synonyms` 覆盖。

Windows 拼音输入法黑盒脚本复用同一套分句、过滤、同义词归一化和 Levenshtein 统计逻辑，因此输出的 `sentence_accuracy_percent` 与 `character_accuracy_percent` 可以和当前 Rime 结果并排看；但两者**不能视为完全同口径的引擎裸对比**，因为黑盒路径包含宿主窗口、系统 IME 状态与机器环境因素。

### 语料切分

实现见 [`src/rime_schema_compare/text_pipeline.py`](src/rime_schema_compare/text_pipeline.py)（`split_sentences` 与相关辅助函数）。要点如下：

- 先按 **换行** 分成行，空行丢弃；再对每行按标点切分。
- **全角 `，`、`。`** 以及 **半角 `,`** 均为切分点；**半角 `.`** 仅在 **非小数**（两侧为数字的 `.` 不切，如 `68.4`）时切分。
- 使用 **弯引号 「”** 配对深度：`：“` / `:"` 后进入引号内；闭引号 `”` 前切分并出层；避免把小数点当句号。
- 去掉段首尾的孤立引号与空白；**含顿号 `、`或书名号 `《》《`** 的片段 **整段丢弃**（不参与评测）。
- 切分后的片段还须满足下面「参与评测」的过滤条件。

### 哪些片段会进入「金句 + 输入串」流水线

与 `benchmark_sentences.py` 中准备阶段一致：

- 片段内 **不得** 含 ASCII 数字或拉丁字母。
- 去掉空白后须为 **纯 CJK 统一表意文字**（`U+4E00`–`U+9FFF`），不含符号或其它文字。
- 纯汉字片段长度须 **不少于 `MIN_EVAL_HANZI_CHARS`（默认 5）**。
- 拼音类方案由 `pypinyin` 的 `lazy_pinyin(..., Style.NORMAL)` 生成 **连续小写全拼** 作为输入。
- `rime_wubi_sentens_wubi86` 读取 `vendor/rime-wubi-sentence/program/wubi86.dict.yaml` 的单字码表，对每个汉字取对应形码的**前 2 个字母**并串接成输入；若句中任一字缺码，则该句对该方案跳过。
- `rime_wubi_sentens_wubi86_with_gram` 读取 `vendor/rime-wubi-sentence_with_gram/program/wubi86.dict.yaml` 的单字码表，对每个汉字取对应形码的**前 2 个字母**并串接成输入；若句中任一字缺码，则该句对该方案跳过。
- `rime_wubi_sentens_tiger` 读取 `vendor/rime-wubi-sentence/program/tiger.dict.yaml` 的单字码表，对每个汉字取对应形码的**前 2 个字母**并串接成输入；若句中任一字缺码，则该句对该方案跳过。
- `rime_wubi_sentens_ziyuan` 读取 `vendor/rime-wubi-sentence/cn_dicts_ziyuan/8105.dict.yaml` 的单字码表，对每个汉字取对应形码的**前 2 个字母**并串接成输入；若句中任一字缺码，则该句对该方案跳过。

### 加载方案（librime 目录）

[`RimeDistroRunner`](src/rime_schema_compare/rime_runner.py) 对每个 vendor：

- **`shared_data_dir`**：固定为仓库下 **`vendor/data`**。
- **`user_data_dir`**：该方案对应的 **`vendor/<子目录>`**（即各子模块根目录），用于读取该发行自己的 `build`、词典与用户侧配置。

切换方案时调用 `switch_distro`：若目录或 schema 变化，会 **关闭旧会话、重新 `initialize`**，再为后续解码做准备。

### 选择方案（schema）

每个 vendor 对应唯一的 **`schema_id`**（见上表）。评测在加载该 vendor 后调用 **`select_schema(session_id, schema_id)`** 打开批量解码会话（`begin_decode_batch`），整段语料在同一 session 内逐句 `feed_input`。

命令行 **`--vendors`** 只决定 **跑哪些 vendor**，不改变各 vendor 自带的 `schema_id`；若要换主方案，需改 `config.py` 中对应 `VendorConfig.schema_id`。

### 关闭用户词库

为保证对比的是 **词库方案本身** 而非个人累计词频，跑基准前会对每个将评测的 `user_data_dir` 调用 [`prepare_vendor_for_benchmark`](src/rime_schema_compare/benchmark_env.py)：

1. **删除** 目录下所有 **`*.userdb`**（LevelDB 式文件夹或文件），去掉已有用户词典。
2. **合并写入** `{schema_id}.custom.yaml`，在 `patch` 中设置 **`translator/enable_user_dict: false`**，禁用译者组件的用户词典。

因此评测前会 **修改** 各 `vendor/*` 下的 custom 与用户库文件；若需保留本地状态，请先备份或使用单独工作副本。

### 语言模型配置说明
几个带_with_gram的方案是在原方案的基础上，改成万象模型

rime_ice_with_gram：
添加rime_ice.custom.yaml
```
patch:
  grammar:
    language: wanxiang-lts-zh-hans
    collocation_max_length: 5
    collocation_min_length: 2
  translator/contextual_suggestions: true
  translator/max_homophones: 4
  translator/max_homographs: 2
  translator/enable_user_dict: false
```
rime_frost_with_gram：
添加rime_frost.custom.yaml
```
patch:
  grammar:
    language: wanxiang-lts-zh-hans
    collocation_max_length: 5
    collocation_min_length: 2
    non_collocation_penalty: -4
    collocation_penalty: -14
  translator/contextual_suggestions: true
  translator/max_homophones: 4
  translator/max_homographs: 2
  translator/enable_user_dict: false
```

wanxiang的配置里本来就有模型配置，把模型文件加上就行

rime-wubi-sentence_with_gram
```
patch:
  grammar:
    language: wanxiang-lts-zh-hans
    collocation_max_length: 5
    collocation_min_length: 2
    non_collocation_penalty: -4
    collocation_penalty: -14
  translator/contextual_suggestions: true
  translator/max_homophones: 4
  translator/max_homographs: 2
  translator/enable_user_dict: false
```

## 仓库布局速查

| 路径 | 作用 |
|------|------|
| [`src/rime_schema_compare/call_librime.py`](src/rime_schema_compare/call_librime.py) | Rime 动态库（`rime.dll` / `librime*.dylib` / `librime.so*`）的 ctypes 封装 |
| [`scripts/benchmark_sentences.py`](scripts/benchmark_sentences.py) | 主评测 CLI |
| [`data/corpus/`](data/corpus/) | 示例语料（UTF-8，可换成自己的文本） |


## License

本仓库自带的脚本与打包以原样提供；第三方组件见 [NOTICE](NOTICE)。各 `vendor/*` 仍遵循其上游许可证。
