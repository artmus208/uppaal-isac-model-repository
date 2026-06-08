# PHY Channels Map

| Channel | Semantics | Declaration | Emits | Listens | Contract role |
|---|---|---|---|---|---|
| `aos_ctrl_expired` | broadcast event/alert | `broadcast` | `ENV_NET` | `ObsFreshness` | diagnostic/degradation/recovery event |
| `beam_failure` | broadcast event/alert | `broadcast` | `A_BM` | `ObsBeamRecovery` | diagnostic/degradation/recovery event |
| `beam_locked` | broadcast event | `broadcast` | - | - | diagnostic/degradation/recovery event |
| `beam_misaligned` | broadcast event | `broadcast` | `A_BM` | - | diagnostic/degradation/recovery event |
| `beam_report` | broadcast report | `broadcast` | `A_BM` | `A_PH`, `A_SQ` | report notification |
| `beam_restored` | broadcast event | `broadcast` | `A_BM` | `ObsBeamRecovery` | diagnostic/degradation/recovery event |
| `blockage_detected` | broadcast event | `broadcast` | `A_CH` | - | diagnostic/degradation/recovery event |
| `channel_degraded` | broadcast event/alert | `broadcast` | `A_CH` | - | diagnostic/degradation/recovery event |
| `channel_report` | broadcast report | `broadcast` | `A_CH` | `A_PH`, `A_SQ` | report notification |
| `contract_violation_bm` | broadcast event/alert | `broadcast` | `A_BM` | - | diagnostic/degradation/recovery event |
| `contract_violation_ch` | broadcast event/alert | `broadcast` | `A_CH` | - | diagnostic/degradation/recovery event |
| `contract_violation_ph` | broadcast event/alert | `broadcast` | `A_PH` | - | diagnostic/degradation/recovery event |
| `contract_violation_sig` | broadcast event/alert | `broadcast` | `A_SIG` | - | diagnostic/degradation/recovery event |
| `contract_violation_sq` | broadcast event/alert | `broadcast` | `A_SQ` | - | diagnostic/degradation/recovery event |
| `degradation_event` | broadcast event | `broadcast` | `A_PH` | - | diagnostic/degradation/recovery event |
| `handover_hint` | broadcast event | `broadcast` | `A_BM` | `ObsBeamRecovery` | diagnostic/degradation/recovery event |
| `mobility_alert` | broadcast event/alert | `broadcast` | `A_CH` | - | diagnostic/degradation/recovery event |
| `multipath_alert` | broadcast event/alert | `broadcast` | `A_CH` | - | diagnostic/degradation/recovery event |
| `phy_failure` | broadcast event/alert | `broadcast` | `A_PH` | - | diagnostic/degradation/recovery event |
| `phy_kpi_report` | broadcast report | `broadcast` | `A_PH` | `ObsSenseReport` | report notification |
| `phy_outage` | broadcast event/alert | `broadcast` | `A_CH` | - | diagnostic/degradation/recovery event |
| `recovery_event` | broadcast event | `broadcast` | - | - | diagnostic/degradation/recovery event |
| `recovery_start` | broadcast event | `broadcast` | `A_BM` | `ObsBeamRecovery` | diagnostic/degradation/recovery event |
| `sensing_degraded` | broadcast event/alert | `broadcast` | `A_SQ` | `ObsSenseReport` | diagnostic/degradation/recovery event |
| `sensing_failure` | broadcast event/alert | `broadcast` | `A_SQ` | - | diagnostic/degradation/recovery event |
| `sensing_report` | broadcast report | `broadcast` | `A_SQ` | `A_PH`, `ObsFreshness` | report notification |
| `sensing_success` | broadcast event | `broadcast` | - | - | diagnostic/degradation/recovery event |
| `signal_degraded` | broadcast event/alert | `broadcast` | `A_SIG` | - | diagnostic/degradation/recovery event |
| `signal_report` | broadcast report | `broadcast` | `A_SIG` | `A_PH`, `A_SQ` | report notification |
| `target_detected` | broadcast event | `broadcast` | `ENV_TARGET` | `A_BM` | diagnostic/degradation/recovery event |
| `beam_cmd` | handshake command | `handshake` | `ENV_MAC` | `A_BM` | environment/MAC/SDN command |
| `controller_report_delivered` | handshake command | `handshake` | `ENV_NET` | `A_PH` | environment/MAC/SDN command |
| `extra_ssb_cmd` | handshake command | `handshake` | `ENV_MAC` | `A_BM` | environment/MAC/SDN command |
| `handover_assist_cmd` | handshake command | `handshake` | `ENV_MAC` | `A_BM` | environment/MAC/SDN command |
| `mac_report_delivered` | handshake command | `handshake` | `ENV_NET` | `A_PH` | environment/MAC/SDN command |
| `measure_tick` | handshake command | `handshake` | `ENV_CH` | `A_CH` | environment/MAC/SDN command |
| `new_beam_confirmed` | handshake command | `handshake` | `ENV_MAC` | `A_BM` | environment/MAC/SDN command |
| `payload_sensing_config` | handshake command | `handshake` | `ENV_MAC` | `A_SIG` | environment/MAC/SDN command |
| `pilot_config` | handshake command | `handshake` | `ENV_MAC` | `A_SIG` | environment/MAC/SDN command |
| `power_cmd` | handshake command | `handshake` | `ENV_MAC` | `A_CH` | environment/MAC/SDN command |
| `prs_config` | handshake command | `handshake` | `ENV_MAC` | `A_SIG` | environment/MAC/SDN command |
| `recovery_cmd` | handshake command | `handshake` | `ENV_MAC` | `A_BM`, `A_PH` | environment/MAC/SDN command |
| `sensing_mode_cmd` | handshake command | `handshake` | `ENV_MAC` | `A_SIG` | environment/MAC/SDN command |
| `ssb_burst_config` | handshake command | `handshake` | `ENV_MAC` | `A_BM` | environment/MAC/SDN command |
| `waveform_config` | handshake command | `handshake` | `ENV_MAC` | `A_SIG` | environment/MAC/SDN command |
