# 数据字典与读取规则

所有 CSV 使用 UTF-8、逗号分隔和英文原始列名。原始浮点文本逐 token 保留。`nan`、`-nan`、`inf`、`-inf` 等原值保留，不能当作 0；是否缺失／无效须结合原状态标记判断。请先按字符串读入，再对所需列进行数值转换，并报告非有限值数量。

## 核心历史表

| 列／前缀 | 含义 |
|---|---|
| `case_id` | U010 / U0183 / U0200 / U0212 标签，不是精确实测速度 |
| `segment_id` | 原独立 attempt；U0183 的 s1/s2/s3 顺序由原三段报告确定 |
| `time_s` | 同一原始键的物理时间，秒，未重置或平移 |
| `iteration` | 原始迭代号；不同恢复段不能只凭 i 去重 |
| `anchor_source_line`, `film_source_line` | 原始文本的 1-based 行号，包括表头位置 |
| `anchor__*` | 原 `anchor_stats.dat` 的全部 85 列，数值未改写 |
| `film__*` | 原 `film_state_stats.dat` 的全部 67 列，数值未改写 |
| `history_use` | 原记录在后续选择中的身份，见下表 |

| history_use | 选择规则 |
|---|---|
| `registered_prefix` | 仅 U0183：依据登记的 16.1/20.2 ms 恢复点及原段起始 i=64421/80837，原第一段拥有恢复点行，后段起始重复行不重复进入有效拼接 |
| `restart_duplicate` | U0183 后段的两条恢复起始行，保留用于连续性审查 |
| `post_checkpoint_failure_tail` | U0183 原前两段的 15 条恢复点之后故障尾记录，保留但不进入登记的有效拼接历史 |
| `retained_single_run` | 其他三个算例的原始单段记录。这个标签不等于科学验收通过，必须同时读 case status |

U0183 的实际键阈值来自原 s2/s3 首行迭代号。有效历史共 3000 行。时间显示的二进制浮点舍入差未用平滑、floor、重新定时或扩大的科学容差修复。

## 常用物理列

- 时间：`t`、`dt`、`handoff_time`、`restart_state_time` 使用秒。`time_s` 是原 `t` 的别名；ms 图轴需显式乘 1000。
- 原 `anchor_stats`：`lower_center` / `upper_center`、`moment_gap` / `plic_gap` 等位置和间隙使用米；`lower_u` / `upper_u` / `closing_speed` 使用 m/s。本组 `closing_speed>0` 表示接近，负值表示分离。
- `film__min_state_gap` 是持久化薄膜模型状态厚度；`film__min_raw_gap` 和 `anchor__plic_gap` 是不同定义的原生几何观测。不能互相替换。米转 µm 时显式乘 10^6。
- `anchor__film_mean_pressure` / `anchor__film_max_pressure` 是原统计列，使用 Pa；NaN 表示该记录没有可使用的有限统计，不能伪造压力剖面。
- 薄膜模型 `inventory_before/after`、`expected_inventory_after`、`handoff_inventory`、`inventory` 为体积量 m³。`cumulative_edge_outflow` 是原累计边界外流量，不能未经来源检查改称“累计排液量”。
- 请求／实际力列如 `actual_lower_force`、`actual_upper_force` 为 N；`step_work`、`cumulative_work` 为 J。力／功账本不等于整个气泡的完整外力／能量预算。
- 计数、status、valid、active、触发与失败标记保留原程序定义。未逐项确认单位的残差、容差和诊断量不要据列名猜测物理单位。

上述常用列按原保存表和 F–R/L12 源语义解释；进一步使用不在此列出的量，应查原 case JSON、表头与源码。所有列的**准确拼写与顺序**以 `catalog.json` 中各 table.columns 为准。

## 独立表

- `anchor_stats`：形态、质心、速度、原生间隙、相库存漂移、求解器和输运统计。
- `film_state_stats`：薄膜状态、几何可用性、库存、通量／压力残差、实际请求／施加力和功账本。
- `film_state_primitive`：逐径向环数据。`bin`、`active`、`radius`、`width`、`delta`、`thickness`、通量与库存一起读取；不能只看全局最小厚度来制造未保存的径向膜形。
- `contact_amr_stats`：已保存的接触区原生界面位置、间隙、细化尺度及强制细化统计。
- `coalescence_stats`：候选聚并模型的实际触发／事件账本；不能从算例命名推断聚并发生。
- `film_state_reject_rank*`：实际故障处各 rank 的逐环记录，不得混入正常时间历史。
- `initialization_audit`：初始化状态，不是缺失的 t=0 时序行。

每个 CSV 分块重复一次表头，行顺序与源表一致；拼接时只保留第一块表头。普通表多了 `case_id`、`segment_id`、`source_line` 三个溯源列。源路径、SHA256、行数和分块哈希均在 `catalog.json`。无表头的元数据、空文件与 JSON 原样放在 `metadata/`，未伪装成数值表。
