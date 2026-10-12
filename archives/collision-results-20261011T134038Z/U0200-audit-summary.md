# U=0.2 m/s、L12、MPI16：终态验收失败记录

检查：2026-10-02 05:49:45；独立复核：05:58:19，均为北京时间。

## 结论与可用范围

计算正常完成至 t=0.030000 s，i=120021，solver exit=0；聚并验收 status=2、accepted=false。冻结验收器对已有全程数据的两次只读重放完全复现原报告：31项门槛中23项通过、8项失败。本算例不能作为“最终单气核复合泡”的成功聚并结果，也没有被转而提升为已验收反弹黄金标准。

证据层级：single-grid-calibrated-closure，screening-boundary、non-predictive。该模型不是独立验证的分子破裂定律。

四份历史均为3001条，覆盖0–30 ms，采样间隔10 us。终态及最后3 ms的301条记录均为两个气核、两个包络，merged=0。

## 严格阈值核查

| 量 | 全程实测值 |
|---|---:|
| 有效、激活的膜状态样本数 | 2471 |
| 最小有效水膜厚 | 14.849892926570037 μm |
| 最小膜厚时刻 | 11.18 ms |
| 冻结聚并阈值 | 14.133806292888758 μm |
| 最小膜厚高于阈值的余量 | 0.716086633681279 μm |
| 低于阈值的有效样本数 | 0 |
| 实际聚并触发 / merged记录数 | 0 / 0 |

冻结代码要求有效激活状态满足严格 h < hcrit，并且只在注册采样时刻比较。观测记录不满足该触发条件。因此，未触发与现有模型和注册采样数据一致；没有证据支持“已跨阈值却漏触发”。不据此推断未记录的采样间极值。原始PLIC几何间距不是这个阈值的定义，不能替换有效膜状态。

## 全程门槛及失败原因

原始 coalescence_acceptance.json 保存全部31项逐项判定。以下保留失败项的准确含义，并分组列明通过项。

| 门槛 | 判定 | 窗口、指标及原因 |
|---|---|---|
| strict_single_trigger | 失败 | 0–30 ms：要求一次真实有效触发，实测0次。 |
| seed_conservation | 失败 | 没有执行播种事务，缺少必须的事务预算证据；不是已测得播种质量或动量不守恒。 |
| seed_energy_ledger | 失败 | 无触发事务，缺少播种前后动能、界面能及面积记录。 |
| transition_dumps | 失败 | final存在，但未发生转换，pre-/post-coalescence不存在。 |
| persistent_single_gas_and_envelope | 失败 | 27–30 ms的301条记录均为2气核、2包络，不满足持续单气核/单包络。 |
| persistent_resolved_oil_enclosure | 失败 | 27–30 ms全部301条不满足严格网格级油层隔离，窗口内首次失败时刻27 ms。气水混合积分/Vg最大0.007592874281528844；跨面气水支持量最大0.9994542430362813；两者各自门槛均为1e-6。 |
| retired_film_ledger | 失败 | 膜状态账本时刻及final dump绑定正确，但active=true、lifecycle=active，未按聚并退役。 |
| independent_final_dump | 失败 | 复合门槛包含单气核/单包络和油层隔离；这些终态要求失败。独立恢复本身成功，不能称为dump损坏或restore崩溃。 |
| declaration_binding、deployment_binding、input_hashes、source_hashes、precursor_full_history、calibration_binding | 通过 | 参数、冻结部署/源码、五组原始与复制输入、完整已验收前驱及U0183校准报告哈希一致。 |
| complete_history、normal_completion、finite_observables | 通过 | 四份3001条完整历史；正常退出；按注册有限性/允许NaN政策检查。 |
| phase_inventory、pressure_projection、viscous_convergence、transport_partition、post_release_anchor_zero、topology_identity | 通过 | 相体积、压力投影、粘性、v4材料输运、释放后约束及嵌套身份在注册界限内。 |
| film_handoff_quality、film_state_positive、film_flux_inventory、film_traction_applied、film_actual_pair_force、film_nonpositive_work、contact_band_at_finest_level、film_valid_area_fraction | 通过 | 全部聚并前继承的膜交接、正状态、通量、实际施力/力矩/一阶矩、功和接触网格门槛通过。 |

全程最大单泡气/油体积相对漂移2.8483932908867624e-5（门槛1e-3）；最大压力缩放残差9.998749341021587e-12（2e-8）；投影体积改变量2.5188274363442027e-7（1e-6）；粘性残差9.992120280062333e-6（1e-5）。

油层隔离失败是独立的网格级阻断项，不能解释成已发生物理分子级油膜破裂；也不能因体积守恒通过而忽略。它与没有水膜阈值触发是不同的问题。

## 原生终态 dump 独立恢复

重用已编译的串行 coalescence_dump_probe_axi，仅恢复final并在init退出；未执行正时间步、聚并事务或续算。输出与runner保存的原始probe逐值一致。

- 原生时刻0.029999999999998948 s、i=120021，必需原始场齐全。
- invalid_cells=0，maximum_identity_defect=0；速度、压力及相场有限性检查通过。
- Vg=1.5690315724383815e-8 m³，Vo=3.9201684412605957e-9 m³，与末行历史在注册容差内一致。
- 气核/包络=2/2；气水混合积分1.1572357366783782e-10 m³，跨面气水支持量0.9753196045759569。
- 终态哈希及膜账本的来源哈希、时刻绑定均通过；但拓扑和隔离不满足成功聚并要求。

## 冻结来源及原始证据

唯一attempt：

`/home/user/liming-collision/oilcoat_coalescence_a84eaee_u0200_20261001/results/F-R-C-U0200-L12-81b22adeba024ea1fdf5321dea2e23ccc47d99b2e6aec1641e278cf91d96478d/attempt-20261001T082139Z-film-on`

源码提交：`a84eaeea5db8575264e48c980fe0297d2addd46a`。

386文件部署源码清单SHA256：`d04d2f828d43af82db017a95e86cba8f9e4bb15897e605c9c81a61e49cd9111d`；44份复制求解器源文件全部通过哈希复核。

| 来源 | SHA256 |
|---|---|
| 归一化已验收前驱；原native t=30.6 ms，实际U=0.19992443478660926 m/s | 28f02c54c83fde89f2c3af06283c2e0589fdaa6779c95a3926cb2a54008ef4b7 |
| 完整历史前驱验收元数据 | a56ef64f3142e007808d20568dc9f5eeae144548224ba07c2ca42658509af46d |
| 上泡包络输入 | 4523d766a3b54ae5933661a4636a4897efa3aef8f6c8a528aa942c058c397490 |
| 上泡QA侧文件 | 59b802c613e0fac9c5411f18c62067106a9c43bdcf2305621da8e9f6c2cd17cf |
| U0183三段全程校准验收报告 | e816a60f058dda113885abe6a0d307dc4dae241cc23184d5cd1c320b304b97c4 |
| final dump | b8498cf23c7e7292afd0f535f1eb8e7360be0432c7055ca6f760c0dfcdecfe78 |
| 原始聚并验收报告 | fd4e34c093940f66d9417697fea0a332f68476044a48df02ce53e60723a13e14 |
| 原始serial final probe报告 | 5b305b4ccdfc01f86476c5768819b06ee2123d2c2e8bb2b709511129dd914ec6 |

原始两份JSON报告已按字节复制到本目录，验收报告下载哈希核对一致。服务器完整历史、primitive膜状态、全部dump、源码、输入、日志及所有失败现场保持原位。未修改黄金U0183基线或前驱，未重跑前驱，未调阈值/颈尺度/初始间距或验收门槛，未重启生产，也未改动其他算例。

## 后续边界

当前可交付的是有完整来源的未达聚并目标的负结果。水膜阈值、播种尺度及门槛不能事后调整以强制成功。若用户另行授权，可在独立诊断环境研究油层网格隔离失败及更广泛的初态/模型敏感性；本次没有实施修复、新算例或正时间续算。U0212是独立attempt，本次没有对它操作，也没有在未复核时宣称其最新状态或结果。
