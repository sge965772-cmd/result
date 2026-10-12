# 四组碰撞结果：ChatGPT 定量分析入口

本目录将已公开归档中的**完整时序表和逐径向环状态**转换为 UTF-8 CSV。原始数值字符串、NaN/Inf、来源行号、重启段和故障尾段保留；没有抽样、平滑、补零、插值或重跑仿真。

## 从哪里开始

1. 先读 [四组结果目录 catalog.csv](catalog.csv) 和 [数据字典](DATA_DICTIONARY.md)。
2. 读取合并了同一原始 `(case, segment, t, i)` 键的核心历史：
   - [U010](core_history/U010/README.md)：3000 行，F–R/L12 冻结反弹基准。
   - [U0183](core_history/U0183/README.md)：3017 行，包括三段记录、故障尾段与重启重复行；`history_use=registered_prefix` 为原报告登记的 3000 行有效拼接历史。
   - [U0200](core_history/U0200/README.md)：3001 行；跑到 30 ms，但没有触发聚并，原聚并验收未通过。
   - [U0212](core_history/U0212/README.md)：2920 行；保存的统计表结束约 29.190 ms，运行实际失败约 29.19575 ms。不能补造 30 ms 终态。
3. 若分析径向膜形／膜库存／边界通量，读取 `tables/<case>/<segment>/film_state_primitive/`；如分析 AMR、原始统计、聚并触发和故障，按 [完整表清单 catalog.json](catalog.json) 中的 `table` 与 `parts` 路径读取。

共有 **64 张原始表、81005 行**。每块 CSV 小于 512000 字节并有独立表头，方便按路径读取；分块不会抽样或截去尾行。完整列列表、源文件 SHA256、每块大小和 SHA256 均保存在 `catalog.json`。

## ChatGPT 的两种读取方式

### A. 通过 GitHub 连接读取

在 ChatGPT 使用已连接并获准访问本仓库的 GitHub 工具，提供本目录 URL。先要求读取本说明和目录，再指定具体 CSV 路径。浏览器只打开 Release 下载页、看到 README，或者读到 CSV 的前几行，都不等于已读取整个数据集。

GitHub 连接是否可用取决于当前账号与聊天环境；本次发布实际用 GitHub 工具读取了仓库元数据与文件，并在发布后回读了 CSV。

### B. 完整数值分析：上传四个核心 CSV

四个核心 CSV 约 5.1–5.3 MB/个，可作为普通 CSV 附件上传至具备数据分析工具的 ChatGPT。请明确要求用 Python/pandas 读取**所有行**，检查行数及时间范围；不要只根据网页预览或文本摘要计算。

`fetch_analysis.py` 可在允许联网的 Python 环境中，把四组核心 CSV 分块下载、校验并恢复为四个完整 CSV。若当前 ChatGPT 的代码环境不允许联网，请在本机运行，再将生成的 CSV 上传到聊天或项目。网络不可用时不能宣称下载或全量读取成功。

```text
python fetch_analysis.py --output-dir chatgpt_upload
```

本次也提供了 [四组核心 CSV 下载包（5.83 MB）](ChatGPT_four_collision_core_csv.zip)；打开后选择 Download raw file 下载。这个包用于方便传输；**最稳妥的附件是解压后的四个 CSV 和 DATA_DICTIONARY.md**，不需要上传四个约 0.7 GB 的原始 tar.gz。

## 可复制到 ChatGPT 的请求

> 请读取 sge965772-cmd/result 的 analysis/collision-results-20261012-v1/README.md、DATA_DICTIONARY.md 和 catalog.csv。用数据分析工具读取所需的完整 CSV／全部分块，先报告各组实际文件数、行数、时间范围与校验结果，再开始定量计算。若只有索引、网页预览或部分行，请明确说明未完成全量读取。U0183 的有效拼接历史只选 history_use=registered_prefix，其他行保留用于故障审查。区分原生 PLIC 间隙与薄膜模型状态厚度；保留 NaN 和不同恢复段；U0200 不得被标成已验收聚并，U0212 不得补出 30 ms 终态。所有指标、单位、选择范围和计算代码要可复核。

## 来源与边界

来源是 [collision-results-20261011-v1](https://github.com/sge965772-cmd/result/releases/tag/collision-results-20261011-v1) 归档。82 个小文件在原服务器只读取得，并逐个匹配已发布归档的来源 SHA256 清单；仅传输了约 7.8 MB 压缩数据，没有再次下载／解压 2.934 GB 归档。

核心历史是 `anchor_stats` 与 `film_state_stats` 的精确键连接：缺行、重复键或不相等的原始时钟会拒绝转换，不会自动插值或默认补值。全部原始表另行保留。U0183 两个段起始的重启重复行与 15 个故障尾行均保留并显式分类；这遵循原 [三段报告](provenance/U0183-three-segment-report.json)，不是新的数值验收。

**此层不包含原生二进制 dump 的所有网格、速度场、压力场或全部 PLIC 空间界面。**这些大数据仍在原始 Release。若后续分析需要空间场／局部形状，需要从相应 dump 做可复现的按需字段导出；不能从已有图片反推数值，也不能把当前时序统计当作完整空间场。

本次仅改善读取形式，不改变任何原始科学验收、物理模型、冻结标签或失败结果；未新增数据许可或 DOI。
