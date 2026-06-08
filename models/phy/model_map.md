# PHY Model Map

- layout mode: `readable`
- coordinate convention: X left-to-right follows scenario progress.
- coordinate convention: negative Y is degradation/alerts; positive Y is recovery/reporting/service paths.
- coordinate convention: nominal/base states are left; violation/failure states are right.

## Templates

| Template | Purpose | Listens | Publishes | Writes | Reads |
|---|---|---|---|---|---|
| `A_CH` | Channel classifier: turns finite alpha_PHY channel classes into ChannelClass and channel reports. | `measure_tick`, `power_cmd` | `blockage_detected`, `channel_degraded`, `channel_report`, `contract_violation_ch`, `mobility_alert`, `multipath_alert`, `phy_outage` | `ChannelClass`, `c_meas`, `ch_enabled_count`, `channel_degraded_flag`, `channel_report_pending` | `env_scenario` |
| `A_SIG` | Signal classifier: models waveform/pilot/PRS/payload sensing configuration and signal reports. | `payload_sensing_config`, `pilot_config`, `prs_config`, `sensing_mode_cmd`, `waveform_config` | `contract_violation_sig`, `signal_degraded`, `signal_report` | `SignalClass`, `c_sig`, `signal_degraded_flag`, `signal_report_pending` | `BLERClass`, `DRTClass`, `PayloadSenseClass`, `PilotDensityClass` |
| `A_BM` | Beam management: search, lock, prediction, recovery, handover assist and failed beam outcomes. | `beam_cmd`, `extra_ssb_cmd`, `handover_assist_cmd`, `new_beam_confirmed`, `recovery_cmd`, `ssb_burst_config`, `target_detected` | `beam_failure`, `beam_misaligned`, `beam_report`, `beam_restored`, `contract_violation_bm`, `handover_hint`, `recovery_start` | `BeamClass`, `beam_degraded_flag`, `c_rec`, `c_ssb`, `target_seen` | `AccClass`, `BeamErrorClass`, `BlockageClass`, `MisClass`, `PRSClass` |
| `A_SQ` | Sensing QoS classifier: aggregates child reports into finite sensing quality states. | `beam_report`, `channel_report`, `signal_report` | `contract_violation_sq`, `sensing_degraded`, `sensing_failure`, `sensing_report` | `SensingState`, `c_sense`, `input_changed`, `sensing_degraded_flag`, `sensing_failure_flag`, `sensing_qos_ok`, `sensing_report_pending`, `sq_enabled_count` | `env_scenario` |
| `A_PH` | Aggregate PHY state: collects child reports and emits PHY KPI/failure/degradation state. | `beam_report`, `channel_report`, `controller_report_delivered`, `mac_report_delivered`, `recovery_cmd`, `sensing_report`, `signal_report` | `contract_violation_ph`, `degradation_event`, `phy_failure`, `phy_kpi_report` | `PHYState`, `c_report`, `child_update`, `comm_ok`, `degradation_flag`, `phy_kpi_report_pending`, `sensing_qos_ok` | `BeamClass`, `ChannelClass`, `SensingState`, `env_scenario` |
| `ENV_CH` | Environment stimulus loop for measurement ticks and finite channel/sensing classes. | - | `measure_tick` | `AoSClass`, `IClass`, `PdClass`, `PowerClass`, `RfaClass`, `SINRClass`, `TimingOk`, `c_env`, `env_scenario` | - |
| `ENV_TARGET` | Environment stimulus loop for target detection and blockage classes. | - | `target_detected` | `BeamErrorClass`, `BlockageClass`, `PRSClass` | - |
| `ENV_MAC` | Environment stimulus loop for MAC/SDN configuration commands. | - | `beam_cmd`, `extra_ssb_cmd`, `handover_assist_cmd`, `new_beam_confirmed`, `payload_sensing_config`, `pilot_config`, `power_cmd`, `prs_config`, `recovery_cmd`, `sensing_mode_cmd`, `ssb_burst_config`, `waveform_config` | `BeamCmdAdmissible`, `ConfigAdmissible` | - |
| `ENV_NET` | Environment stimulus loop for network/controller delivery and freshness expiry. | - | `aos_ctrl_expired`, `controller_report_delivered`, `mac_report_delivered` | `NetDeliveryOk`, `aos_ctrl`, `c_net` | - |
| `ObsSenseReport` | Bounded-response observer: trigger, wait, response-satisfied edge, violation edge. | `phy_kpi_report`, `sensing_degraded` | - | `c_obs_sense` | - |
| `ObsFreshness` | Bounded-response observer: trigger, wait, response-satisfied edge, violation edge. | `aos_ctrl_expired`, `sensing_report` | - | `c_obs_fresh` | `SensingState` |
| `ObsBeamRecovery` | Bounded-response observer: trigger, wait, response-satisfied edge, violation edge. | `beam_failure`, `beam_restored`, `handover_hint`, `recovery_start` | - | `c_obs_beam` | - |

## Semantic Zones

### `A_CH`

| Zone | Locations / paths |
|---|---|
| nominal | `ChannelNominal` |
| measurement | `MeasurePending` |
| channel degraded classes | `InterferenceLimited`, `MobilityLimited`, `MultipathLimited`, `Blockage` |
| outage | `Outage` |
| contract violation | `ContractViolation_CH` |

### `A_SIG`

| Zone | Locations / paths |
|---|---|
| signal nominal | `SignalNominal`, `PilotBasedSensing`, `PayloadAssistedSensing` |
| reconfiguring | `SignalReconfiguring` |
| signal limited | `SignalLimited` |
| report path | `signal_report! transitions` |
| violation | `ContractViolation_SIG` |

### `A_BM`

| Zone | Locations / paths |
|---|---|
| beam lock | `BeamSearch`, `BeamSearchSeen`, `BeamTrack`, `BeamLock`, `BeamPredict` |
| recovery | `BeamMisalign`, `BeamRecoveryStart`, `BeamRecover` |
| restored | `BeamLock` |
| handover assist | `BeamHOAssist` |
| failed | `BeamFailed`, `ContractViolation_BM` |

### `A_SQ`

| Zone | Locations / paths |
|---|---|
| sensing nominal | `Idle`, `SensingEvaluating`, `SensingQoSOk` |
| probability/freshness/resolution limited | `ProbabilityLimited`, `FalseAlarmLimited`, `AccuracyLimited`, `FreshnessLimited`, `CoverageLimited`, `CapacityLimited` |
| failure | `SensingFailure`, `ContractViolation_SQ` |

### `A_PH`

| Zone | Locations / paths |
|---|---|
| aggregate normal | `PHYNormal` |
| communication degraded | `PHYCommunicationDegraded` |
| sensing degraded | `PHYSensingDegraded` |
| joint degraded | `PHYJointDegraded` |
| failure | `PHYFailure`, `ContractViolation_PH` |
| reporting/recovery | `PHYKpiReporting`, `PHYRecovery` |

### `ENV_*`

| Zone | Locations / paths |
|---|---|
| environment stimulus loops | `TickWait`, `TargetWait`, `ConfigWait`, `DeliveryWait` |

### `Obs*`

| Zone | Locations / paths |
|---|---|
| trigger | `Idle -> Wait` |
| waiting | `Wait` |
| satisfied | `Wait -> Idle response transitions` |
| violation | `Violation` |
