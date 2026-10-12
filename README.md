# 油膜气泡碰撞结果数据：备份与溯源

## ChatGPT 可读取的定量分析数据

新增 [定量分析入口](analysis/collision-results-20261012-v1/README.md)、[四组目录](analysis/collision-results-20261012-v1/catalog.csv) 和 [数据字典](analysis/collision-results-20261012-v1/DATA_DICTIONARY.md)。四组核心历史及 64 张原始时序／径向环表已提供普通 UTF-8 CSV 分块，可通过 GitHub 工具按路径读取；完整数值、NaN、来源行号、重启段和失败尾段保留。

进行全量数值分析时，使用入口中的 fetch_analysis.py 获取四个约 5 MB 的核心 CSV，再作为普通文件附件上传 ChatGPT 并要求用数据分析工具读取所有行。只有网页预览或 CSV 的部分行时，不得声称已经完成全部数据分析。原始大体积 dump 继续从下方 Release 获取，不与 CSV 时序统计混为同一数据范围。

本次仅新增读取层，以下原始备份说明与验收状态保持不变。


本仓库保存四条既有碰撞结果的版本索引、来源清单和验收记录。大体积数据通过 GitHub Release 附件提供，常规 Git 仅保存可审计元数据。

## 本次数据版本

- 数据归档版本：`collision-results-20261011-v1`
- 本地归档完成：2026-10-11；本次 GitHub 备份请求日期：2026-10-12（Asia/Shanghai）。
- [Release 数据下载入口](https://github.com/sge965772-cmd/result/releases/tag/collision-results-20261011-v1)
- [完整归档清单](archives/collision-results-20261011T134038Z/ARCHIVE_MANIFEST.json)
- [四个数据包 SHA256](archives/collision-results-20261011T134038Z/SHA256SUMS.txt)
- 原始普通文件：1,889 个，6,370,564,875 字节。
- 四个压缩包：2,933,969,508 字节（约 2.934 GB；GB = 10^9 字节）。

Release 先以草稿上传，全部附件校验通过后才发布。请以已发布 Release 中的附件、文件大小及 SHA256 为完成依据；GitHub 自动生成的 Source code ZIP/TAR 仅含元数据，不包含下列四个碰撞数据包。

| 算例 | 下载 | 压缩字节数 | 原始文件数 | 原始结果状态 |
| --- | --- | ---: | ---: | --- |
| U010 | [U010-collision-results.tar.gz](https://github.com/sge965772-cmd/result/releases/download/collision-results-20261011-v1/U010-collision-results.tar.gz) | 671,280,074 | 590 | F-R-U010-L12 冻结反弹基准生产线结果 |
| U0183 | [U0183-collision-results.tar.gz](https://github.com/sge965772-cmd/result/releases/download/collision-results-20261011-v1/U0183-collision-results.tar.gz) | 749,519,449 | 523 | 三段合格历史拼接至 30 ms；原始故障尾段仍保留 |
| U0200 | [U0200-collision-results.tar.gz](https://github.com/sge965772-cmd/result/releases/download/collision-results-20261011-v1/U0200-collision-results.tar.gz) | 762,042,738 | 391 | 原始校准聚并候选跑到 30 ms，但未触发聚并，聚并验收未通过 |
| U0212 | [U0212-collision-results.tar.gz](https://github.com/sge965772-cmd/result/releases/download/collision-results-20261011-v1/U0212-collision-results.tar.gz) | 751,127,247 | 385 | 相容前驱库最高可恢复速度算例；约 29.19575 ms 失败，没有完整 30 ms 终态 |

## 来源关系及科学边界

U010（源码 `fca689f`）是原始 F-R/L12/v4/Reynolds 冻结反弹生产线。U0183 继承该生产线及源码基础，使用自身 U≈0.183 m/s 的前驱状态，不是从 U010 碰撞后的状态改速度续算。

U0183 的合格链为 0→16.1→20.2→30 ms，源码提交依次为 `c702bbe`、`432bdec`、`4798773`。完整 case hash、原始 attempt 路径、恢复点及原始验收门禁见 [三段报告](archives/collision-results-20261011T134038Z/U0183-three-segment-report.json)。

U0200 与 U0212 使用 `a84eaee` 原始校准聚并候选。U0200 的原始阈值为 14.133806292888758 µm，30 ms 内 0 次触发；[验收记录](archives/collision-results-20261011T134038Z/U0200-coalescence_acceptance.json) 保留未通过状态。U0212 的实际前驱速度为 0.21162571406691141 m/s；“最大速度”只指当时相容前驱库已保存、可恢复的最高速度，不是物理极限。

本次发布是数据备份，不是新的仿真或数值验收。冻结标签、上传成功、完整性校验通过均不等于网格无关性、实验预测或聚并物理验证通过。

## 数据范围与组织

仅包含四条正式碰撞结果；U0183 包含三个正式续算段。每个 attempt 的 dump、时序/界面数据、运行日志、结果记录及自带输入/源码快照原样保留。未另加完整前驱库、诊断重放、预检、后处理图件副本或其他 H15、Track A、L11/L13、平面算例。

包内路径相对于原服务器 `/home/user/liming-collision/`，保留部署和 attempt 名称。原始失败尾段不裁剪，合格拼接窗口以原始报告为准。各 `*-source-files.sha256` 清单覆盖全部 1,889 个原始普通文件；本地归档已逐文件比对通过。

时间字段以原始记录定义为准，物理时间通常为秒；各数据表列名、单位、参数和程序版本应结合原始表头、case JSON 及 attempt 内源码快照使用，不把 U010/U0183/U0200/U0212 标签当作精确测量值。

## 下载与校验

下载四个 `.tar.gz` 附件与 `SHA256SUMS.txt` 后，在 Linux/macOS/WSL 可执行：

```sh
sha256sum -c SHA256SUMS.txt
tar -xzf U0183-collision-results.tar.gz -C <已有的空目录>
```

Windows PowerShell 可用 `Get-FileHash -Algorithm SHA256` 与清单逐项比对，并用系统 `tar` 解包。建议解压到空目录，避免不同版本混合。

本版本以 Release 标签、Git 提交和 SHA256 共同溯源。后续变更应建立新版本，不覆盖本版本附件或重写本版本标签。本地 E 盘原始归档继续保留，GitHub 不作为唯一备份。

## 许可与引用

本次请求未指定研究数据许可、论文 DOI 或作者名单；未额外添加许可或虚构 DOI。当前可用版本标识为仓库 URL、Release 标签和 Git 提交 SHA。本仓库不是一次完整 FAIR/期刊投稿合规性认定。
