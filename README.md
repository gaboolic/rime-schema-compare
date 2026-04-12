# rime-schema-compare

在 **Windows** 上用 **Python + librime**（`rime.dll`，例如小狼毫自带）对比多套 Rime 词库方案的 **整句解码准确率**。

## 各套方案说明

默认参与对比的方案在 `src/rime_schema_compare/config.py` 的 `DEFAULT_VENDORS` 中定义：每个条目包含 **vendor 键**（命令行与报表列名）、**子目录**、以及 **主 schema_id**（librime 里选用的方案 ID）。

| Vendor 键 | 目录 | 主 schema | 说明 |
|-----------|------|-----------|------|
| `mingyuepinyin` | `vendor/mingyuepinyin` | `luna_pinyin_simp` | 明月拼音（简体全拼），与 Rime 自带 Luna 系方案同源的一类发行 |
| `rime_ice` | `vendor/rime-ice` | `rime_ice` | 薄荷方案（Rime 冰 / rime-ice） |
| `rime_frost` | `vendor/rime-frost` | `rime_frost` | 雾凇拼音（rime-frost） |
| `wanxiang` | `vendor/rime_wanxiang` | `wanxiang` | 万象拼音（子模块跟踪分支 `wanxiang`，见 [.gitmodules](.gitmodules)） |

各方案的实际 YAML、编译产物与用户状态都放在各自的 `vendor/...` 目录下；所有方案共用的只读资源放在 [`vendor/data`](vendor/data)（不存在会自动创建）。需要让所有方案看到同一套程序级配置或补丁时，把文件放在 `vendor/data`（例如从小狼毫安装目录复制或做符号链接）。

## 如何执行评测脚本

### 前置条件

- 已安装 **小狼毫**（或其它提供 `rime.dll` 及同目录依赖 DLL 的环境）。
- **Python 3.10+** 建议。
- **Git 子模块** 已拉取（首次体积较大）：

```bash
git submodule update --init --recursive --depth 1
```

### Rime 部署（每个要测的 `vendor/*` 至少做一次）

子模块里多为 **源码 YAML**。在跑 librime 前，需要像正常用户目录一样 **部署/编译** 出 `.bin` 等产物（例如把该目录拷到小狼毫用户目录后点「部署」，或对应该路径运行 `rime_deployer`）。未部署时，结果里会出现大量 `empty_prediction` / `no_context`。

### 安装依赖与 `rime.dll`

```bash
pip install -r requirements.txt
```

可选：在仓库根目录建 `.env`，指定 DLL 路径：

```env
RIME_DLL=C:\Program Files\Rime\weasel-0.16.3\rime.dll
```

若把 **`rime.dll`**（及所需同伴 DLL）放在 **仓库根目录**，脚本会优先使用，否则会扫描常见 `Program Files\Rime\weasel-*` 路径。

### 运行命令

在仓库根目录执行（PowerShell / cmd 示例）：

```bash
set RIME_DLL=C:\Program Files\Rime\weasel-0.16.3\rime.dll
python scripts\smoke_rime.py
python scripts\benchmark_sentences.py
```

不传 `--corpus` 时，会一次性评测 **`data/corpus/` 下所有 `*.txt`**。指定单个或多个语料文件：

```bash
python scripts\benchmark_sentences.py --corpus data\corpus\prose.txt
python scripts\benchmark_sentences.py --corpus data\corpus\prose.txt data\corpus\tech.txt
```

常用参数：

- `--vendors rime_frost rime_ice wanxiang mingyuepinyin` — 只跑其中若干套（键名见上表，默认四套全跑）。
- `--out-dir artifacts` — 输出目录。
- `--rime-dll <路径>` — 覆盖 `rime.dll`（等价于环境变量）。
- `--progress-every N` — 每 N 个原始分句打一条进度到 stderr（`0` 关闭）。
- `--eval-synonyms path/to.json` — 评测用同义词归一化规则（默认 `data/eval_synonyms.json`；不存在则用内置规则）。

### 输出文件（`artifacts/`）

未指定 `--corpus` 时，文件名前缀一般为 `benchmark_all_corpus_<时间戳>`；单语料时为 `benchmark_<语料标签>_<时间戳>`。

| 文件 | 内容 |
|------|------|
| `*_*.csv` | 宽表：每句一行，`gold` / `pinyin` 后接各方案的句子是否判对、单句字级准确率、预测与错误信息等 |
| `*_long.csv` | 窄表：每句 × 每方案一行；行序为先方案后句子 |
| `*_long_by_sentence.csv` | 同上结构；行序为先句子后方案 |
| `*_scheme_compare.txt` | 各方案**独有判对**及相对其它方案的**多判对**句子列表 |
| `*_summary.csv` | 按语料 × 方案汇总 |
| `*_report.txt` | 中文摘要：句子正确率、文字正确率等 |
| `*.json` | 完整 JSON（含窄表级 `per_sentence`） |

进度与阶段日志在 **stderr**（简体中文 Windows 控制台多为 GBK，避免乱码勿强行把 stderr 设为 UTF-8）。阶段前缀包括：`[启动]`、`[语料列表]`、`[分句]`、`[pypinyin]`、`[librime:加载方案 x]`、`[librime:解码 x]`、`[汇总]`、`[写出结果]` 等。若使用 UTF-8 终端（如 `chcp 65001`），stderr 中的中文通常也能正常显示。

## 评测细节

### 指标与同义词

对每条参与评测的句子，用 **整句是否完全一致** 统计句子级准确率；字级用 **Levenshtein 编辑距离** 汇总得到 macro CER（总编辑量 / 金文总字数）。比较前可做 **同义词归一化**（默认规则 + `data/eval_synonyms.json`，例如 其它→其他、他/她/它→他、的/地/得→的），可用 `--eval-synonyms` 覆盖。

### 语料切分

实现见 [`src/rime_schema_compare/text_pipeline.py`](src/rime_schema_compare/text_pipeline.py)（`split_sentences` 与相关辅助函数）。要点如下：

- 先按 **换行** 分成行，空行丢弃；再对每行按标点切分。
- **全角 `，`、`。`** 以及 **半角 `,`** 均为切分点；**半角 `.`** 仅在 **非小数**（两侧为数字的 `.` 不切，如 `68.4`）时切分。
- 使用 **弯引号 「”** 配对深度：`：“` / `:"` 后进入引号内；闭引号 `”` 前切分并出层；避免把小数点当句号。
- 去掉段首尾的孤立引号与空白；**含顿号 `、`或书名号 `《》《`** 的片段 **整段丢弃**（不参与评测）。
- 切分后的片段还须满足下面「参与评测」的过滤条件。

### 哪些片段会进入「金句 + 拼音」流水线

与 `benchmark_sentences.py` 中准备阶段一致：

- 片段内 **不得** 含 ASCII 数字或拉丁字母。
- 去掉空白后须为 **纯 CJK 统一表意文字**（`U+4E00`–`U+9FFF`），不含符号或其它文字。
- 纯汉字片段长度须 **不少于 `MIN_EVAL_HANZI_CHARS`（默认 5）**。
- 由 `pypinyin` 的 `lazy_pinyin(..., Style.NORMAL)` 生成 **连续小写全拼** 作为输入；仅保留汉字部分参与转写。

### 加载方案（librime 目录）

[`RimeDistroRunner`](src/rime_schema_compare/rime_runner.py) 对每个 vendor：

- **`shared_data_dir`**：固定为仓库下 **`vendor/data`**。
- **`user_data_dir`**：该方案对应的 **`vendor/<子目录>`**（即各子模块根目录），用于读取该发行自己的 `build`、词典与用户侧配置。

切换方案时调用 `switch_distro`：若目录或 schema 变化，会 **关闭旧会话、重新 `initialize`**，再为后续解码做准备。

### 选择方案（schema）

每个 vendor 对应唯一的 **`schema_id`**（见上表）。评测在加载该 vendor 后调用 **`select_schema(session_id, schema_id)`** 打开批量解码会话（`begin_decode_batch`），整段语料在同一 session 内逐句 `feed_pinyin`。

命令行 **`--vendors`** 只决定 **跑哪些 vendor**，不改变各 vendor 自带的 `schema_id`；若要换主方案，需改 `config.py` 中对应 `VendorConfig.schema_id`。

### 关闭用户词库

为保证对比的是 **词库方案本身** 而非个人累计词频，跑基准前会对每个将评测的 `user_data_dir` 调用 [`prepare_vendor_for_benchmark`](src/rime_schema_compare/benchmark_env.py)：

1. **删除** 目录下所有 **`*.userdb`**（LevelDB 式文件夹或文件），去掉已有用户词典。
2. **合并写入** `{schema_id}.custom.yaml`，在 `patch` 中设置 **`translator/enable_user_dict: false`**，禁用译者组件的用户词典。

因此评测前会 **修改** 各 `vendor/*` 下的 custom 与用户库文件；若需保留本地状态，请先备份或使用单独工作副本。

## 仓库布局速查

| 路径 | 作用 |
|------|------|
| [`src/rime_schema_compare/call_librime.py`](src/rime_schema_compare/call_librime.py) | `rime.dll` 的 ctypes 封装 |
| [`scripts/benchmark_sentences.py`](scripts/benchmark_sentences.py) | 主评测 CLI |
| [`data/corpus/`](data/corpus/) | 示例语料（UTF-8，可换成自己的文本） |

## 故障排除

- **`FileNotFoundError`（`rime.dll`）** — 设置 `RIME_DLL` 或 `--rime-dll` 指向小狼毫目录中的 `rime.dll`。
- **`Vendor data directory missing`** — 执行 `git submodule update --init --recursive`（并确认 `vendor/mingyuepinyin` 等目录存在）。
- **大量 `empty_prediction`** — 对该 `vendor/*` 执行 Rime 部署，生成编译产物。
- **子模块克隆 SSL 错误** — 检查 Git HTTPS / 代理后重试。

## License

本仓库自带的脚本与打包以原样提供；第三方组件见 [NOTICE](NOTICE)。各 `vendor/*` 仍遵循其上游许可证。
