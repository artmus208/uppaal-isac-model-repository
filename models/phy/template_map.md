# PHY Template Map

Layout mode: `readable`.

## `A_CH`

Channel classifier: turns finite alpha_PHY channel classes into ChannelClass and channel reports.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `ChannelNominal` | nominal channel class; baseline left-side state | `0,0` |
| `MeasurePending` | measurement/report deadline window | `300,180` |
| `InterferenceLimited` | communication degraded by interference | `660,-260` |
| `MobilityLimited` | communication degraded by mobility/Doppler | `660,-80` |
| `MultipathLimited` | communication degraded by delay spread | `660,100` |
| `Blockage` | blockage class detected | `960,-440` |
| `Outage` | channel outage event branch | `960,-640` |
| `ContractViolation_CH` | contract violation sink on the right side | `1280,0` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `ChannelNominal -> MeasurePending` | synchronised branch | `-` | `measure_tick?` | `c_meas`, `channel_report_pending` | measure_tick: listener here; senders ENV_CH |
| `ChannelNominal -> ChannelNominal` | receives MAC/SDN command | `-` | `power_cmd?` | - | power_cmd: listener here; senders ENV_MAC |
| `MeasurePending -> MeasurePending` | receives MAC/SDN command | `-` | `power_cmd?` | - | power_cmd: listener here; senders ENV_MAC |
| `InterferenceLimited -> MeasurePending` | synchronised branch | `-` | `measure_tick?` | `c_meas`, `channel_report_pending` | measure_tick: listener here; senders ENV_CH |
| `InterferenceLimited -> InterferenceLimited` | receives MAC/SDN command | `-` | `power_cmd?` | - | power_cmd: listener here; senders ENV_MAC |
| `MobilityLimited -> MeasurePending` | synchronised branch | `-` | `measure_tick?` | `c_meas`, `channel_report_pending` | measure_tick: listener here; senders ENV_CH |
| `MobilityLimited -> MobilityLimited` | receives MAC/SDN command | `-` | `power_cmd?` | - | power_cmd: listener here; senders ENV_MAC |
| `MultipathLimited -> MeasurePending` | synchronised branch | `-` | `measure_tick?` | `c_meas`, `channel_report_pending` | measure_tick: listener here; senders ENV_CH |
| `MultipathLimited -> MultipathLimited` | receives MAC/SDN command | `-` | `power_cmd?` | - | power_cmd: listener here; senders ENV_MAC |
| `Blockage -> MeasurePending` | synchronised branch | `-` | `measure_tick?` | `c_meas`, `channel_report_pending` | measure_tick: listener here; senders ENV_CH |
| `Blockage -> Blockage` | receives MAC/SDN command | `-` | `power_cmd?` | - | power_cmd: listener here; senders ENV_MAC |
| `Outage -> MeasurePending` | synchronised branch | `-` | `measure_tick?` | `c_meas`, `channel_report_pending` | measure_tick: listener here; senders ENV_CH |
| `Outage -> Outage` | receives MAC/SDN command | `-` | `power_cmd?` | - | power_cmd: listener here; senders ENV_MAC |
| `ContractViolation_CH -> MeasurePending` | synchronised branch | `-` | `measure_tick?` | `c_meas`, `channel_report_pending` | measure_tick: listener here; senders ENV_CH |
| `ContractViolation_CH -> ContractViolation_CH` | contract/deadline failure path | `-` | `power_cmd?` | - | power_cmd: listener here; senders ENV_MAC |
| `MeasurePending -> ChannelNominal` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_NORMAL && c_meas <= D_meas` | `channel_report!` | `ChannelClass`, `c_meas`, `ch_enabled_count`, `channel_degraded_flag`, `channel_report_pending` | channel_report: sender here; listeners A_PH, A_SQ |
| `MeasurePending -> InterferenceLimited` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_COMM_DEGRADED && c_meas <= D_meas` | `channel_report!` | `ChannelClass`, `c_meas`, `ch_enabled_count`, `channel_degraded_flag`, `channel_report_pending` | channel_report: sender here; listeners A_PH, A_SQ |
| `MeasurePending -> MobilityLimited` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_SENSING_DEGRADED && c_meas <= D_meas` | `channel_report!` | `ChannelClass`, `c_meas`, `ch_enabled_count`, `channel_degraded_flag`, `channel_report_pending` | channel_report: sender here; listeners A_PH, A_SQ |
| `MeasurePending -> Outage` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_JOINT_DEGRADED && c_meas <= D_meas` | `channel_report!` | `ChannelClass`, `c_meas`, `ch_enabled_count`, `channel_degraded_flag`, `channel_report_pending` | channel_report: sender here; listeners A_PH, A_SQ |
| `InterferenceLimited -> InterferenceLimited` | event self-loop | `-` | `channel_degraded!` | - | channel_degraded: sender here; listeners - |
| `MobilityLimited -> MobilityLimited` | event self-loop | `-` | `mobility_alert!` | - | mobility_alert: sender here; listeners - |
| `MultipathLimited -> MultipathLimited` | event self-loop | `-` | `multipath_alert!` | - | multipath_alert: sender here; listeners - |
| `Blockage -> Blockage` | event self-loop | `-` | `blockage_detected!` | - | blockage_detected: sender here; listeners - |
| `Outage -> Outage` | event self-loop | `-` | `phy_outage!` | - | phy_outage: sender here; listeners - |
| `ChannelNominal -> ContractViolation_CH` | contract/deadline failure path | `!ass_ch()` | `contract_violation_ch!` | - | contract_violation_ch: sender here; listeners - |
| `MeasurePending -> ContractViolation_CH` | contract/deadline failure path | `!ass_ch()` | `contract_violation_ch!` | - | contract_violation_ch: sender here; listeners - |
| `InterferenceLimited -> ContractViolation_CH` | contract/deadline failure path | `!ass_ch()` | `contract_violation_ch!` | - | contract_violation_ch: sender here; listeners - |
| `MobilityLimited -> ContractViolation_CH` | contract/deadline failure path | `!ass_ch()` | `contract_violation_ch!` | - | contract_violation_ch: sender here; listeners - |
| `MultipathLimited -> ContractViolation_CH` | contract/deadline failure path | `!ass_ch()` | `contract_violation_ch!` | - | contract_violation_ch: sender here; listeners - |
| `Blockage -> ContractViolation_CH` | contract/deadline failure path | `!ass_ch()` | `contract_violation_ch!` | - | contract_violation_ch: sender here; listeners - |
| `Outage -> ContractViolation_CH` | contract/deadline failure path | `!ass_ch()` | `contract_violation_ch!` | - | contract_violation_ch: sender here; listeners - |

## `A_SIG`

Signal classifier: models waveform/pilot/PRS/payload sensing configuration and signal reports.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `SignalNominal` | baseline signal configuration | `0,0` |
| `PilotBasedSensing` | pilot-based sensing mode is viable | `620,0` |
| `PayloadAssistedSensing` | payload-assisted sensing mode is viable | `900,0` |
| `SignalReconfiguring` | configuration/report deadline window | `300,200` |
| `SignalLimited` | signal quality is limited | `1180,-220` |
| `ContractViolation_SIG` | contract violation sink on the right side | `1480,0` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `SignalNominal -> SignalReconfiguring` | receives MAC/SDN command | `-` | `waveform_config?` | `c_sig`, `signal_report_pending` | waveform_config: listener here; senders ENV_MAC |
| `SignalNominal -> SignalReconfiguring` | receives MAC/SDN command | `-` | `pilot_config?` | `c_sig`, `signal_report_pending` | pilot_config: listener here; senders ENV_MAC |
| `SignalNominal -> SignalReconfiguring` | receives MAC/SDN command | `-` | `prs_config?` | `c_sig`, `signal_report_pending` | prs_config: listener here; senders ENV_MAC |
| `SignalNominal -> SignalReconfiguring` | receives MAC/SDN command | `-` | `payload_sensing_config?` | `c_sig`, `signal_report_pending` | payload_sensing_config: listener here; senders ENV_MAC |
| `SignalNominal -> SignalReconfiguring` | receives MAC/SDN command | `-` | `sensing_mode_cmd?` | `c_sig`, `signal_report_pending` | sensing_mode_cmd: listener here; senders ENV_MAC |
| `PilotBasedSensing -> SignalReconfiguring` | receives MAC/SDN command | `-` | `waveform_config?` | `c_sig`, `signal_report_pending` | waveform_config: listener here; senders ENV_MAC |
| `PilotBasedSensing -> SignalReconfiguring` | receives MAC/SDN command | `-` | `pilot_config?` | `c_sig`, `signal_report_pending` | pilot_config: listener here; senders ENV_MAC |
| `PilotBasedSensing -> SignalReconfiguring` | receives MAC/SDN command | `-` | `prs_config?` | `c_sig`, `signal_report_pending` | prs_config: listener here; senders ENV_MAC |
| `PilotBasedSensing -> SignalReconfiguring` | receives MAC/SDN command | `-` | `payload_sensing_config?` | `c_sig`, `signal_report_pending` | payload_sensing_config: listener here; senders ENV_MAC |
| `PilotBasedSensing -> SignalReconfiguring` | receives MAC/SDN command | `-` | `sensing_mode_cmd?` | `c_sig`, `signal_report_pending` | sensing_mode_cmd: listener here; senders ENV_MAC |
| `PayloadAssistedSensing -> SignalReconfiguring` | receives MAC/SDN command | `-` | `waveform_config?` | `c_sig`, `signal_report_pending` | waveform_config: listener here; senders ENV_MAC |
| `PayloadAssistedSensing -> SignalReconfiguring` | receives MAC/SDN command | `-` | `pilot_config?` | `c_sig`, `signal_report_pending` | pilot_config: listener here; senders ENV_MAC |
| `PayloadAssistedSensing -> SignalReconfiguring` | receives MAC/SDN command | `-` | `prs_config?` | `c_sig`, `signal_report_pending` | prs_config: listener here; senders ENV_MAC |
| `PayloadAssistedSensing -> SignalReconfiguring` | receives MAC/SDN command | `-` | `payload_sensing_config?` | `c_sig`, `signal_report_pending` | payload_sensing_config: listener here; senders ENV_MAC |
| `PayloadAssistedSensing -> SignalReconfiguring` | receives MAC/SDN command | `-` | `sensing_mode_cmd?` | `c_sig`, `signal_report_pending` | sensing_mode_cmd: listener here; senders ENV_MAC |
| `SignalReconfiguring -> SignalReconfiguring` | receives MAC/SDN command | `-` | `waveform_config?` | `c_sig`, `signal_report_pending` | waveform_config: listener here; senders ENV_MAC |
| `SignalReconfiguring -> SignalReconfiguring` | receives MAC/SDN command | `-` | `pilot_config?` | `c_sig`, `signal_report_pending` | pilot_config: listener here; senders ENV_MAC |
| `SignalReconfiguring -> SignalReconfiguring` | receives MAC/SDN command | `-` | `prs_config?` | `c_sig`, `signal_report_pending` | prs_config: listener here; senders ENV_MAC |
| `SignalReconfiguring -> SignalReconfiguring` | receives MAC/SDN command | `-` | `payload_sensing_config?` | `c_sig`, `signal_report_pending` | payload_sensing_config: listener here; senders ENV_MAC |
| `SignalReconfiguring -> SignalReconfiguring` | receives MAC/SDN command | `-` | `sensing_mode_cmd?` | `c_sig`, `signal_report_pending` | sensing_mode_cmd: listener here; senders ENV_MAC |
| `SignalLimited -> SignalReconfiguring` | receives MAC/SDN command | `-` | `waveform_config?` | `c_sig`, `signal_report_pending` | waveform_config: listener here; senders ENV_MAC |
| `SignalLimited -> SignalReconfiguring` | receives MAC/SDN command | `-` | `pilot_config?` | `c_sig`, `signal_report_pending` | pilot_config: listener here; senders ENV_MAC |
| `SignalLimited -> SignalReconfiguring` | receives MAC/SDN command | `-` | `prs_config?` | `c_sig`, `signal_report_pending` | prs_config: listener here; senders ENV_MAC |
| `SignalLimited -> SignalReconfiguring` | receives MAC/SDN command | `-` | `payload_sensing_config?` | `c_sig`, `signal_report_pending` | payload_sensing_config: listener here; senders ENV_MAC |
| `SignalLimited -> SignalReconfiguring` | receives MAC/SDN command | `-` | `sensing_mode_cmd?` | `c_sig`, `signal_report_pending` | sensing_mode_cmd: listener here; senders ENV_MAC |
| `ContractViolation_SIG -> SignalReconfiguring` | receives MAC/SDN command | `-` | `waveform_config?` | `c_sig`, `signal_report_pending` | waveform_config: listener here; senders ENV_MAC |
| `ContractViolation_SIG -> SignalReconfiguring` | receives MAC/SDN command | `-` | `pilot_config?` | `c_sig`, `signal_report_pending` | pilot_config: listener here; senders ENV_MAC |
| `ContractViolation_SIG -> SignalReconfiguring` | receives MAC/SDN command | `-` | `prs_config?` | `c_sig`, `signal_report_pending` | prs_config: listener here; senders ENV_MAC |
| `ContractViolation_SIG -> SignalReconfiguring` | receives MAC/SDN command | `-` | `payload_sensing_config?` | `c_sig`, `signal_report_pending` | payload_sensing_config: listener here; senders ENV_MAC |
| `ContractViolation_SIG -> SignalReconfiguring` | receives MAC/SDN command | `-` | `sensing_mode_cmd?` | `c_sig`, `signal_report_pending` | sensing_mode_cmd: listener here; senders ENV_MAC |
| `SignalReconfiguring -> SignalNominal` | publishes report and commits classifier/aggregate state | `c_sig <= D_sig` | `signal_report!` | `SignalClass`, `c_sig`, `signal_report_pending` | signal_report: sender here; listeners A_PH, A_SQ |
| `SignalNominal -> PilotBasedSensing` | publishes report and commits classifier/aggregate state | `PilotDensityClass == PILOTDENSITYCLASS_OK && BLERClass == BLERCLASS_OK && DRTClass == DRTCLASS_OK` | `signal_report!` | `SignalClass`, `c_sig`, `signal_report_pending` | signal_report: sender here; listeners A_PH, A_SQ |
| `PilotBasedSensing -> PayloadAssistedSensing` | publishes report and commits classifier/aggregate state | `PilotDensityClass == PILOTDENSITYCLASS_LOW && PayloadSenseClass != PAYLOADSENSECLASS_FAILED` | `signal_report!` | `SignalClass`, `c_sig`, `signal_report_pending` | signal_report: sender here; listeners A_PH, A_SQ |
| `PayloadAssistedSensing -> SignalLimited` | publishes report and commits classifier/aggregate state | `BLERClass != BLERCLASS_OK \|\| DRTClass == DRTCLASS_BAD \|\| PayloadSenseClass == PAYLOADSENSECLASS_FAILED` | `signal_report!` | `SignalClass`, `c_sig`, `signal_degraded_flag`, `signal_report_pending` | signal_report: sender here; listeners A_PH, A_SQ |
| `SignalLimited -> SignalLimited` | event self-loop | `-` | `signal_degraded!` | - | signal_degraded: sender here; listeners - |
| `SignalLimited -> SignalReconfiguring` | receives MAC/SDN command | `-` | `waveform_config?` | `c_sig` | waveform_config: listener here; senders ENV_MAC |
| `SignalNominal -> ContractViolation_SIG` | contract/deadline failure path | `!ass_sig()` | `contract_violation_sig!` | - | contract_violation_sig: sender here; listeners - |
| `PilotBasedSensing -> ContractViolation_SIG` | contract/deadline failure path | `!ass_sig()` | `contract_violation_sig!` | - | contract_violation_sig: sender here; listeners - |
| `PayloadAssistedSensing -> ContractViolation_SIG` | contract/deadline failure path | `!ass_sig()` | `contract_violation_sig!` | - | contract_violation_sig: sender here; listeners - |
| `SignalReconfiguring -> ContractViolation_SIG` | contract/deadline failure path | `!ass_sig()` | `contract_violation_sig!` | - | contract_violation_sig: sender here; listeners - |
| `SignalLimited -> ContractViolation_SIG` | contract/deadline failure path | `!ass_sig()` | `contract_violation_sig!` | - | contract_violation_sig: sender here; listeners - |

## `A_BM`

Beam management: search, lock, prediction, recovery, handover assist and failed beam outcomes.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `BeamSearch` | beam search baseline | `0,0` |
| `BeamSearchSeen` | target has been detected during search | `280,0` |
| `BeamTrack` | beam tracking path | `560,0` |
| `BeamLock` | locked/restored beam | `840,0` |
| `BeamPredict` | predictive branch before recovery | `840,-220` |
| `BeamMisalign` | misalignment alert branch | `560,-260` |
| `BeamRecoveryStart` | recovery trigger handoff | `1120,220` |
| `BeamRecover` | bounded recovery deadline window | `1400,220` |
| `BeamHOAssist` | handover assist outcome | `1680,200` |
| `BeamFailed` | beam recovery failed | `1680,-260` |
| `ContractViolation_BM` | contract violation sink on the right side | `1980,0` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `BeamSearch -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `BeamSearch -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `BeamSearch -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `BeamSearch -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `BeamSearchSeen -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `BeamSearchSeen -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `BeamSearchSeen -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `BeamSearchSeen -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `BeamTrack -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `BeamTrack -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `BeamTrack -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `BeamTrack -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `BeamLock -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `BeamLock -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `BeamLock -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `BeamLock -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `BeamPredict -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `BeamPredict -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `BeamPredict -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `BeamPredict -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `BeamMisalign -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `BeamMisalign -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `BeamMisalign -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `BeamMisalign -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `BeamRecoveryStart -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `BeamRecoveryStart -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `BeamRecoveryStart -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `BeamRecoveryStart -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `BeamRecover -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `BeamRecover -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `BeamRecover -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `BeamRecover -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `BeamHOAssist -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `BeamHOAssist -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `BeamHOAssist -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `BeamHOAssist -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `BeamFailed -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `BeamFailed -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `BeamFailed -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `BeamFailed -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `ContractViolation_BM -> BeamSearch` | receives MAC/SDN command | `-` | `beam_cmd?` | `BeamClass`, `c_ssb` | beam_cmd: listener here; senders ENV_MAC |
| `ContractViolation_BM -> BeamSearch` | receives MAC/SDN command | `-` | `ssb_burst_config?` | `BeamClass`, `c_ssb` | ssb_burst_config: listener here; senders ENV_MAC |
| `ContractViolation_BM -> BeamRecover` | receives MAC/SDN command | `-` | `recovery_cmd?` | `BeamClass`, `c_rec` | recovery_cmd: listener here; senders ENV_MAC |
| `ContractViolation_BM -> BeamHOAssist` | receives MAC/SDN command | `-` | `handover_assist_cmd?` | `BeamClass` | handover_assist_cmd: listener here; senders ENV_MAC |
| `BeamSearch -> BeamSearchSeen` | synchronised branch | `-` | `target_detected?` | `target_seen` | target_detected: listener here; senders ENV_TARGET |
| `BeamSearchSeen -> BeamTrack` | publishes report and commits classifier/aggregate state | `PRSClass != PRSCLASS_FAILED` | `beam_report!` | `BeamClass` | beam_report: sender here; listeners A_PH, A_SQ |
| `BeamTrack -> BeamLock` | publishes report and commits classifier/aggregate state | `BeamErrorClass == BEAMERRORCLASS_LOCKABLE` | `beam_report!` | `BeamClass` | beam_report: sender here; listeners A_PH, A_SQ |
| `BeamTrack -> BeamMisalign` | publishes report and commits classifier/aggregate state | `AccClass == ACCCLASS_FAILED \|\| BeamErrorClass == BEAMERRORCLASS_CRITICAL` | `beam_report!` | `BeamClass`, `beam_degraded_flag` | beam_report: sender here; listeners A_PH, A_SQ |
| `BeamLock -> BeamLock` | publishes report and commits classifier/aggregate state | `MisClass == MISCLASS_OK` | `beam_report!` | `BeamClass` | beam_report: sender here; listeners A_PH, A_SQ |
| `BeamLock -> BeamPredict` | publishes report and commits classifier/aggregate state | `MisClass == MISCLASS_WARN \|\| BlockageClass == BLOCKAGECLASS_SUSPECTED` | `beam_report!` | `BeamClass` | beam_report: sender here; listeners A_PH, A_SQ |
| `BeamPredict -> BeamRecoveryStart` | receives MAC/SDN command | `-` | `extra_ssb_cmd?` | `c_rec` | extra_ssb_cmd: listener here; senders ENV_MAC |
| `BeamRecoveryStart -> BeamRecover` | synchronised branch | `-` | `recovery_start!` | `BeamClass` | recovery_start: sender here; listeners ObsBeamRecovery |
| `BeamMisalign -> BeamRecoveryStart` | synchronised branch | `-` | `beam_misaligned!` | `c_rec` | beam_misaligned: sender here; listeners - |
| `BeamRecover -> BeamLock` | beam recovery outcome | `BeamErrorClass == BEAMERRORCLASS_LOCKABLE && c_rec <= D_BM` | `beam_restored!` | `BeamClass` | beam_restored: sender here; listeners ObsBeamRecovery |
| `BeamRecover -> BeamHOAssist` | beam recovery outcome | `BlockageClass == BLOCKAGECLASS_CONFIRMED && c_rec <= D_BM` | `handover_hint!` | `BeamClass` | handover_hint: sender here; listeners ObsBeamRecovery |
| `BeamRecover -> BeamFailed` | beam recovery outcome | `c_rec == D_BM && BeamErrorClass != BEAMERRORCLASS_LOCKABLE && BlockageClass != BLOCKAGECLASS_CONFIRMED` | `beam_failure!` | `BeamClass` | beam_failure: sender here; listeners ObsBeamRecovery |
| `BeamHOAssist -> BeamTrack` | synchronised branch | `-` | `new_beam_confirmed?` | `BeamClass` | new_beam_confirmed: listener here; senders ENV_MAC |
| `BeamSearch -> ContractViolation_BM` | contract/deadline failure path | `!ass_bm()` | `contract_violation_bm!` | - | contract_violation_bm: sender here; listeners - |
| `BeamSearchSeen -> ContractViolation_BM` | contract/deadline failure path | `!ass_bm()` | `contract_violation_bm!` | - | contract_violation_bm: sender here; listeners - |
| `BeamTrack -> ContractViolation_BM` | contract/deadline failure path | `!ass_bm()` | `contract_violation_bm!` | - | contract_violation_bm: sender here; listeners - |
| `BeamLock -> ContractViolation_BM` | contract/deadline failure path | `!ass_bm()` | `contract_violation_bm!` | - | contract_violation_bm: sender here; listeners - |
| `BeamPredict -> ContractViolation_BM` | contract/deadline failure path | `!ass_bm()` | `contract_violation_bm!` | - | contract_violation_bm: sender here; listeners - |
| `BeamMisalign -> ContractViolation_BM` | contract/deadline failure path | `!ass_bm()` | `contract_violation_bm!` | - | contract_violation_bm: sender here; listeners - |
| `BeamRecoveryStart -> ContractViolation_BM` | contract/deadline failure path | `!ass_bm()` | `contract_violation_bm!` | - | contract_violation_bm: sender here; listeners - |
| `BeamRecover -> ContractViolation_BM` | contract/deadline failure path | `!ass_bm()` | `contract_violation_bm!` | - | contract_violation_bm: sender here; listeners - |
| `BeamHOAssist -> ContractViolation_BM` | contract/deadline failure path | `!ass_bm()` | `contract_violation_bm!` | - | contract_violation_bm: sender here; listeners - |
| `BeamFailed -> ContractViolation_BM` | contract/deadline failure path | `!ass_bm()` | `contract_violation_bm!` | - | contract_violation_bm: sender here; listeners - |

## `A_SQ`

Sensing QoS classifier: aggregates child reports into finite sensing quality states.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `Idle` | baseline idle state | `0,0` |
| `SensingEvaluating` | child report aggregation deadline window | `300,180` |
| `SensingQoSOk` | sensing QoS nominal | `620,0` |
| `ProbabilityLimited` | detection probability limited | `620,-240` |
| `FalseAlarmLimited` | false alarm rate limited | `900,-240` |
| `AccuracyLimited` | accuracy/resolution limited | `1180,-240` |
| `FreshnessLimited` | freshness/AoS limited | `900,-480` |
| `CoverageLimited` | coverage limited | `1180,-480` |
| `CapacityLimited` | capacity/resource limited | `1460,-240` |
| `SensingFailure` | sensing failure branch | `1460,-480` |
| `ContractViolation_SQ` | contract violation sink on the right side | `1780,0` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `Idle -> SensingEvaluating` | consumes child report | `-` | `channel_report?` | `c_sense`, `input_changed`, `sensing_report_pending` | channel_report: listener here; senders A_CH |
| `Idle -> SensingEvaluating` | consumes child report | `-` | `signal_report?` | `c_sense`, `input_changed`, `sensing_report_pending` | signal_report: listener here; senders A_SIG |
| `Idle -> SensingEvaluating` | consumes child report | `-` | `beam_report?` | `c_sense`, `input_changed`, `sensing_report_pending` | beam_report: listener here; senders A_BM |
| `SensingEvaluating -> SensingQoSOk` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_NORMAL && c_sense <= D_sense` | `sensing_report!` | `SensingState`, `c_sense`, `sensing_degraded_flag`, `sensing_qos_ok`, `sensing_report_pending`, `sq_enabled_count` | sensing_report: sender here; listeners A_PH, ObsFreshness |
| `SensingEvaluating -> SensingQoSOk` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_COMM_DEGRADED && c_sense <= D_sense` | `sensing_report!` | `SensingState`, `c_sense`, `sensing_degraded_flag`, `sensing_qos_ok`, `sensing_report_pending`, `sq_enabled_count` | sensing_report: sender here; listeners A_PH, ObsFreshness |
| `SensingEvaluating -> FreshnessLimited` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_SENSING_DEGRADED && c_sense <= D_sense` | `sensing_report!` | `SensingState`, `c_sense`, `sensing_degraded_flag`, `sensing_qos_ok`, `sensing_report_pending`, `sq_enabled_count` | sensing_report: sender here; listeners A_PH, ObsFreshness |
| `SensingEvaluating -> SensingFailure` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_JOINT_DEGRADED && c_sense <= D_sense` | `sensing_report!` | `SensingState`, `c_sense`, `sensing_failure_flag`, `sensing_qos_ok`, `sensing_report_pending`, `sq_enabled_count` | sensing_report: sender here; listeners A_PH, ObsFreshness |
| `ProbabilityLimited -> ProbabilityLimited` | event self-loop | `-` | `sensing_degraded!` | - | sensing_degraded: sender here; listeners ObsSenseReport |
| `FalseAlarmLimited -> FalseAlarmLimited` | event self-loop | `-` | `sensing_degraded!` | - | sensing_degraded: sender here; listeners ObsSenseReport |
| `AccuracyLimited -> AccuracyLimited` | event self-loop | `-` | `sensing_degraded!` | - | sensing_degraded: sender here; listeners ObsSenseReport |
| `FreshnessLimited -> FreshnessLimited` | event self-loop | `-` | `sensing_degraded!` | - | sensing_degraded: sender here; listeners ObsSenseReport |
| `CoverageLimited -> CoverageLimited` | event self-loop | `-` | `sensing_degraded!` | - | sensing_degraded: sender here; listeners ObsSenseReport |
| `CapacityLimited -> CapacityLimited` | event self-loop | `-` | `sensing_degraded!` | - | sensing_degraded: sender here; listeners ObsSenseReport |
| `SensingFailure -> SensingFailure` | event self-loop | `-` | `sensing_failure!` | - | sensing_failure: sender here; listeners - |
| `Idle -> ContractViolation_SQ` | contract/deadline failure path | `!ass_sq()` | `contract_violation_sq!` | - | contract_violation_sq: sender here; listeners - |
| `SensingEvaluating -> ContractViolation_SQ` | contract/deadline failure path | `!ass_sq()` | `contract_violation_sq!` | - | contract_violation_sq: sender here; listeners - |
| `SensingQoSOk -> ContractViolation_SQ` | contract/deadline failure path | `!ass_sq()` | `contract_violation_sq!` | - | contract_violation_sq: sender here; listeners - |
| `ProbabilityLimited -> ContractViolation_SQ` | contract/deadline failure path | `!ass_sq()` | `contract_violation_sq!` | - | contract_violation_sq: sender here; listeners - |
| `FalseAlarmLimited -> ContractViolation_SQ` | contract/deadline failure path | `!ass_sq()` | `contract_violation_sq!` | - | contract_violation_sq: sender here; listeners - |
| `AccuracyLimited -> ContractViolation_SQ` | contract/deadline failure path | `!ass_sq()` | `contract_violation_sq!` | - | contract_violation_sq: sender here; listeners - |
| `FreshnessLimited -> ContractViolation_SQ` | contract/deadline failure path | `!ass_sq()` | `contract_violation_sq!` | - | contract_violation_sq: sender here; listeners - |
| `CoverageLimited -> ContractViolation_SQ` | contract/deadline failure path | `!ass_sq()` | `contract_violation_sq!` | - | contract_violation_sq: sender here; listeners - |
| `CapacityLimited -> ContractViolation_SQ` | contract/deadline failure path | `!ass_sq()` | `contract_violation_sq!` | - | contract_violation_sq: sender here; listeners - |
| `SensingFailure -> ContractViolation_SQ` | contract/deadline failure path | `!ass_sq()` | `contract_violation_sq!` | - | contract_violation_sq: sender here; listeners - |

## `A_PH`

Aggregate PHY state: collects child reports and emits PHY KPI/failure/degradation state.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `PHYNormal` | aggregate PHY is normal | `0,0` |
| `PHYCommunicationDegraded` | aggregate communication degradation | `660,-240` |
| `PHYSensingDegraded` | aggregate sensing degradation | `660,-40` |
| `PHYJointDegraded` | joint communication+sensing degradation | `940,-420` |
| `PHYKpiReporting` | aggregate report deadline window | `320,200` |
| `PHYRecovery` | aggregate recovery service path | `660,260` |
| `PHYFailure` | aggregate PHY failure branch | `1220,-300` |
| `ContractViolation_PH` | contract violation sink on the right side | `1520,0` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `PHYNormal -> PHYKpiReporting` | consumes child report | `-` | `channel_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | channel_report: listener here; senders A_CH |
| `PHYNormal -> PHYKpiReporting` | consumes child report | `-` | `signal_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | signal_report: listener here; senders A_SIG |
| `PHYNormal -> PHYKpiReporting` | consumes child report | `-` | `beam_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | beam_report: listener here; senders A_BM |
| `PHYNormal -> PHYKpiReporting` | consumes child report | `-` | `sensing_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | sensing_report: listener here; senders A_SQ |
| `PHYNormal -> PHYNormal` | event self-loop | `-` | `mac_report_delivered?` | - | mac_report_delivered: listener here; senders ENV_NET |
| `PHYNormal -> PHYNormal` | event self-loop | `-` | `controller_report_delivered?` | - | controller_report_delivered: listener here; senders ENV_NET |
| `PHYNormal -> PHYRecovery` | receives MAC/SDN command | `-` | `recovery_cmd?` | `PHYState` | recovery_cmd: listener here; senders ENV_MAC |
| `PHYCommunicationDegraded -> PHYKpiReporting` | consumes child report | `-` | `channel_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | channel_report: listener here; senders A_CH |
| `PHYCommunicationDegraded -> PHYKpiReporting` | consumes child report | `-` | `signal_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | signal_report: listener here; senders A_SIG |
| `PHYCommunicationDegraded -> PHYKpiReporting` | consumes child report | `-` | `beam_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | beam_report: listener here; senders A_BM |
| `PHYCommunicationDegraded -> PHYKpiReporting` | consumes child report | `-` | `sensing_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | sensing_report: listener here; senders A_SQ |
| `PHYCommunicationDegraded -> PHYCommunicationDegraded` | event self-loop | `-` | `mac_report_delivered?` | - | mac_report_delivered: listener here; senders ENV_NET |
| `PHYCommunicationDegraded -> PHYCommunicationDegraded` | event self-loop | `-` | `controller_report_delivered?` | - | controller_report_delivered: listener here; senders ENV_NET |
| `PHYCommunicationDegraded -> PHYRecovery` | receives MAC/SDN command | `-` | `recovery_cmd?` | `PHYState` | recovery_cmd: listener here; senders ENV_MAC |
| `PHYSensingDegraded -> PHYKpiReporting` | consumes child report | `-` | `channel_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | channel_report: listener here; senders A_CH |
| `PHYSensingDegraded -> PHYKpiReporting` | consumes child report | `-` | `signal_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | signal_report: listener here; senders A_SIG |
| `PHYSensingDegraded -> PHYKpiReporting` | consumes child report | `-` | `beam_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | beam_report: listener here; senders A_BM |
| `PHYSensingDegraded -> PHYKpiReporting` | consumes child report | `-` | `sensing_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | sensing_report: listener here; senders A_SQ |
| `PHYSensingDegraded -> PHYSensingDegraded` | event self-loop | `-` | `mac_report_delivered?` | - | mac_report_delivered: listener here; senders ENV_NET |
| `PHYSensingDegraded -> PHYSensingDegraded` | event self-loop | `-` | `controller_report_delivered?` | - | controller_report_delivered: listener here; senders ENV_NET |
| `PHYSensingDegraded -> PHYRecovery` | receives MAC/SDN command | `-` | `recovery_cmd?` | `PHYState` | recovery_cmd: listener here; senders ENV_MAC |
| `PHYJointDegraded -> PHYKpiReporting` | consumes child report | `-` | `channel_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | channel_report: listener here; senders A_CH |
| `PHYJointDegraded -> PHYKpiReporting` | consumes child report | `-` | `signal_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | signal_report: listener here; senders A_SIG |
| `PHYJointDegraded -> PHYKpiReporting` | consumes child report | `-` | `beam_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | beam_report: listener here; senders A_BM |
| `PHYJointDegraded -> PHYKpiReporting` | consumes child report | `-` | `sensing_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | sensing_report: listener here; senders A_SQ |
| `PHYJointDegraded -> PHYJointDegraded` | event self-loop | `-` | `mac_report_delivered?` | - | mac_report_delivered: listener here; senders ENV_NET |
| `PHYJointDegraded -> PHYJointDegraded` | event self-loop | `-` | `controller_report_delivered?` | - | controller_report_delivered: listener here; senders ENV_NET |
| `PHYJointDegraded -> PHYRecovery` | receives MAC/SDN command | `-` | `recovery_cmd?` | `PHYState` | recovery_cmd: listener here; senders ENV_MAC |
| `PHYKpiReporting -> PHYKpiReporting` | consumes child report | `-` | `channel_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | channel_report: listener here; senders A_CH |
| `PHYKpiReporting -> PHYKpiReporting` | consumes child report | `-` | `signal_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | signal_report: listener here; senders A_SIG |
| `PHYKpiReporting -> PHYKpiReporting` | consumes child report | `-` | `beam_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | beam_report: listener here; senders A_BM |
| `PHYKpiReporting -> PHYKpiReporting` | consumes child report | `-` | `sensing_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | sensing_report: listener here; senders A_SQ |
| `PHYKpiReporting -> PHYKpiReporting` | event self-loop | `-` | `mac_report_delivered?` | - | mac_report_delivered: listener here; senders ENV_NET |
| `PHYKpiReporting -> PHYKpiReporting` | event self-loop | `-` | `controller_report_delivered?` | - | controller_report_delivered: listener here; senders ENV_NET |
| `PHYKpiReporting -> PHYRecovery` | receives MAC/SDN command | `-` | `recovery_cmd?` | `PHYState` | recovery_cmd: listener here; senders ENV_MAC |
| `PHYRecovery -> PHYKpiReporting` | consumes child report | `-` | `channel_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | channel_report: listener here; senders A_CH |
| `PHYRecovery -> PHYKpiReporting` | consumes child report | `-` | `signal_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | signal_report: listener here; senders A_SIG |
| `PHYRecovery -> PHYKpiReporting` | consumes child report | `-` | `beam_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | beam_report: listener here; senders A_BM |
| `PHYRecovery -> PHYKpiReporting` | consumes child report | `-` | `sensing_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | sensing_report: listener here; senders A_SQ |
| `PHYRecovery -> PHYRecovery` | event self-loop | `-` | `mac_report_delivered?` | - | mac_report_delivered: listener here; senders ENV_NET |
| `PHYRecovery -> PHYRecovery` | event self-loop | `-` | `controller_report_delivered?` | - | controller_report_delivered: listener here; senders ENV_NET |
| `PHYRecovery -> PHYRecovery` | receives MAC/SDN command | `-` | `recovery_cmd?` | `PHYState` | recovery_cmd: listener here; senders ENV_MAC |
| `PHYFailure -> PHYKpiReporting` | consumes child report | `-` | `channel_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | channel_report: listener here; senders A_CH |
| `PHYFailure -> PHYKpiReporting` | consumes child report | `-` | `signal_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | signal_report: listener here; senders A_SIG |
| `PHYFailure -> PHYKpiReporting` | consumes child report | `-` | `beam_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | beam_report: listener here; senders A_BM |
| `PHYFailure -> PHYKpiReporting` | consumes child report | `-` | `sensing_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | sensing_report: listener here; senders A_SQ |
| `PHYFailure -> PHYFailure` | event self-loop | `-` | `mac_report_delivered?` | - | mac_report_delivered: listener here; senders ENV_NET |
| `PHYFailure -> PHYFailure` | event self-loop | `-` | `controller_report_delivered?` | - | controller_report_delivered: listener here; senders ENV_NET |
| `PHYFailure -> PHYRecovery` | receives MAC/SDN command | `-` | `recovery_cmd?` | `PHYState` | recovery_cmd: listener here; senders ENV_MAC |
| `ContractViolation_PH -> PHYKpiReporting` | consumes child report | `-` | `channel_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | channel_report: listener here; senders A_CH |
| `ContractViolation_PH -> PHYKpiReporting` | consumes child report | `-` | `signal_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | signal_report: listener here; senders A_SIG |
| `ContractViolation_PH -> PHYKpiReporting` | consumes child report | `-` | `beam_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | beam_report: listener here; senders A_BM |
| `ContractViolation_PH -> PHYKpiReporting` | consumes child report | `-` | `sensing_report?` | `c_report`, `child_update`, `phy_kpi_report_pending` | sensing_report: listener here; senders A_SQ |
| `ContractViolation_PH -> ContractViolation_PH` | contract/deadline failure path | `-` | `mac_report_delivered?` | - | mac_report_delivered: listener here; senders ENV_NET |
| `ContractViolation_PH -> ContractViolation_PH` | contract/deadline failure path | `-` | `controller_report_delivered?` | - | controller_report_delivered: listener here; senders ENV_NET |
| `ContractViolation_PH -> PHYRecovery` | receives MAC/SDN command | `-` | `recovery_cmd?` | `PHYState` | recovery_cmd: listener here; senders ENV_MAC |
| `PHYKpiReporting -> PHYNormal` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_NORMAL && c_report <= D_report` | `phy_kpi_report!` | `PHYState`, `c_report`, `comm_ok`, `degradation_flag`, `phy_kpi_report_pending`, `sensing_qos_ok` | phy_kpi_report: sender here; listeners ObsSenseReport |
| `PHYKpiReporting -> PHYCommunicationDegraded` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_COMM_DEGRADED && c_report <= D_report` | `phy_kpi_report!` | `PHYState`, `c_report`, `comm_ok`, `degradation_flag`, `phy_kpi_report_pending`, `sensing_qos_ok` | phy_kpi_report: sender here; listeners ObsSenseReport |
| `PHYKpiReporting -> PHYSensingDegraded` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_SENSING_DEGRADED && c_report <= D_report` | `phy_kpi_report!` | `PHYState`, `c_report`, `comm_ok`, `degradation_flag`, `phy_kpi_report_pending`, `sensing_qos_ok` | phy_kpi_report: sender here; listeners ObsSenseReport |
| `PHYKpiReporting -> PHYJointDegraded` | publishes report and commits classifier/aggregate state | `env_scenario == SCENARIO_JOINT_DEGRADED && c_report <= D_report` | `phy_kpi_report!` | `PHYState`, `c_report`, `comm_ok`, `degradation_flag`, `phy_kpi_report_pending`, `sensing_qos_ok` | phy_kpi_report: sender here; listeners ObsSenseReport |
| `PHYKpiReporting -> PHYFailure` | guarded classification branch | `ChannelClass == CHANNELCLASS_OUTAGE \|\| BeamClass == BEAMCLASS_FAILED \|\| SensingState == SENSINGSTATE_SENSINGFAILURE` | `phy_failure!` | `PHYState` | phy_failure: sender here; listeners - |
| `PHYCommunicationDegraded -> PHYCommunicationDegraded` | event self-loop | `-` | `degradation_event!` | - | degradation_event: sender here; listeners - |
| `PHYSensingDegraded -> PHYSensingDegraded` | event self-loop | `-` | `degradation_event!` | - | degradation_event: sender here; listeners - |
| `PHYJointDegraded -> PHYJointDegraded` | event self-loop | `-` | `degradation_event!` | - | degradation_event: sender here; listeners - |
| `PHYNormal -> ContractViolation_PH` | contract/deadline failure path | `!ass_ph()` | `contract_violation_ph!` | - | contract_violation_ph: sender here; listeners - |
| `PHYCommunicationDegraded -> ContractViolation_PH` | contract/deadline failure path | `!ass_ph()` | `contract_violation_ph!` | - | contract_violation_ph: sender here; listeners - |
| `PHYSensingDegraded -> ContractViolation_PH` | contract/deadline failure path | `!ass_ph()` | `contract_violation_ph!` | - | contract_violation_ph: sender here; listeners - |
| `PHYJointDegraded -> ContractViolation_PH` | contract/deadline failure path | `!ass_ph()` | `contract_violation_ph!` | - | contract_violation_ph: sender here; listeners - |
| `PHYKpiReporting -> ContractViolation_PH` | contract/deadline failure path | `!ass_ph()` | `contract_violation_ph!` | - | contract_violation_ph: sender here; listeners - |
| `PHYRecovery -> ContractViolation_PH` | contract/deadline failure path | `!ass_ph()` | `contract_violation_ph!` | - | contract_violation_ph: sender here; listeners - |
| `PHYFailure -> ContractViolation_PH` | contract/deadline failure path | `!ass_ph()` | `contract_violation_ph!` | - | contract_violation_ph: sender here; listeners - |

## `ENV_CH`

Environment stimulus loop for measurement ticks and finite channel/sensing classes.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `TickWait` | environment measurement tick loop | `0,0` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `TickWait -> TickWait` | event self-loop | `-` | `measure_tick!` | `AoSClass`, `IClass`, `PdClass`, `PowerClass`, `RfaClass`, `SINRClass`, `TimingOk`, `c_env`, `env_scenario` | measure_tick: sender here; listeners A_CH |
| `TickWait -> TickWait` | event self-loop | `-` | `measure_tick!` | `AoSClass`, `IClass`, `PdClass`, `PowerClass`, `RfaClass`, `SINRClass`, `TimingOk`, `c_env`, `env_scenario` | measure_tick: sender here; listeners A_CH |
| `TickWait -> TickWait` | event self-loop | `-` | `measure_tick!` | `AoSClass`, `IClass`, `PdClass`, `PowerClass`, `RfaClass`, `SINRClass`, `TimingOk`, `c_env`, `env_scenario` | measure_tick: sender here; listeners A_CH |
| `TickWait -> TickWait` | event self-loop | `-` | `measure_tick!` | `AoSClass`, `IClass`, `PdClass`, `PowerClass`, `RfaClass`, `SINRClass`, `TimingOk`, `c_env`, `env_scenario` | measure_tick: sender here; listeners A_CH |
| `TickWait -> TickWait` | internal/environment branch | `-` | `-` | - | - |

## `ENV_TARGET`

Environment stimulus loop for target detection and blockage classes.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `TargetWait` | environment target/blockage stimulus loop | `0,0` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `TargetWait -> TargetWait` | event self-loop | `-` | `target_detected!` | `BeamErrorClass`, `BlockageClass`, `PRSClass` | target_detected: sender here; listeners A_BM |
| `TargetWait -> TargetWait` | internal/environment branch | `-` | `-` | `BlockageClass` | - |

## `ENV_MAC`

Environment stimulus loop for MAC/SDN configuration commands.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `ConfigWait` | environment MAC/SDN command loop | `0,0` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `pilot_config!` | `BeamCmdAdmissible`, `ConfigAdmissible` | pilot_config: sender here; listeners A_SIG |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `prs_config!` | `BeamCmdAdmissible`, `ConfigAdmissible` | prs_config: sender here; listeners A_SIG |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `ssb_burst_config!` | `BeamCmdAdmissible`, `ConfigAdmissible` | ssb_burst_config: sender here; listeners A_BM |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `waveform_config!` | `BeamCmdAdmissible`, `ConfigAdmissible` | waveform_config: sender here; listeners A_SIG |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `payload_sensing_config!` | `BeamCmdAdmissible`, `ConfigAdmissible` | payload_sensing_config: sender here; listeners A_SIG |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `beam_cmd!` | `BeamCmdAdmissible`, `ConfigAdmissible` | beam_cmd: sender here; listeners A_BM |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `extra_ssb_cmd!` | `BeamCmdAdmissible`, `ConfigAdmissible` | extra_ssb_cmd: sender here; listeners A_BM |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `handover_assist_cmd!` | `BeamCmdAdmissible`, `ConfigAdmissible` | handover_assist_cmd: sender here; listeners A_BM |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `power_cmd!` | `BeamCmdAdmissible`, `ConfigAdmissible` | power_cmd: sender here; listeners A_CH |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `sensing_mode_cmd!` | `BeamCmdAdmissible`, `ConfigAdmissible` | sensing_mode_cmd: sender here; listeners A_SIG |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `new_beam_confirmed!` | `BeamCmdAdmissible`, `ConfigAdmissible` | new_beam_confirmed: sender here; listeners A_BM |
| `ConfigWait -> ConfigWait` | event self-loop | `-` | `recovery_cmd!` | `BeamCmdAdmissible`, `ConfigAdmissible` | recovery_cmd: sender here; listeners A_BM, A_PH |
| `ConfigWait -> ConfigWait` | internal/environment branch | `-` | `-` | - | - |

## `ENV_NET`

Environment stimulus loop for network/controller delivery and freshness expiry.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `DeliveryWait` | environment delivery/freshness loop | `0,0` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `DeliveryWait -> DeliveryWait` | event self-loop | `-` | `mac_report_delivered!` | `NetDeliveryOk`, `c_net` | mac_report_delivered: sender here; listeners A_PH |
| `DeliveryWait -> DeliveryWait` | event self-loop | `-` | `controller_report_delivered!` | `NetDeliveryOk`, `aos_ctrl`, `c_net` | controller_report_delivered: sender here; listeners A_PH |
| `DeliveryWait -> DeliveryWait` | event self-loop | `-` | `aos_ctrl_expired!` | - | aos_ctrl_expired: sender here; listeners ObsFreshness |
| `DeliveryWait -> DeliveryWait` | internal/environment branch | `-` | `-` | - | - |

## `ObsSenseReport`

Bounded-response observer: trigger, wait, response-satisfied edge, violation edge.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `Idle` | baseline idle state | `0,0` |
| `Wait` | observer waiting for bounded response | `300,0` |
| `Violation` | observer deadline violation | `620,-220` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `Idle -> Wait` | synchronised branch | `-` | `sensing_degraded?` | `c_obs_sense` | sensing_degraded: listener here; senders A_SQ |
| `Wait -> Idle` | consumes child report | `c_obs_sense <= D_report` | `phy_kpi_report?` | - | phy_kpi_report: listener here; senders A_PH |
| `Wait -> Violation` | contract/deadline failure path | `c_obs_sense > D_report` | `-` | - | - |

## `ObsFreshness`

Bounded-response observer: trigger, wait, response-satisfied edge, violation edge.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `Idle` | baseline idle state | `0,0` |
| `Wait` | observer waiting for bounded response | `300,0` |
| `Violation` | observer deadline violation | `620,-220` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `Idle -> Wait` | synchronised branch | `-` | `aos_ctrl_expired?` | `c_obs_fresh` | aos_ctrl_expired: listener here; senders ENV_NET |
| `Wait -> Idle` | consumes child report | `c_obs_fresh <= D_sense && SensingState == SENSINGSTATE_FRESHNESSLIMITED` | `sensing_report?` | - | sensing_report: listener here; senders A_SQ |
| `Wait -> Violation` | contract/deadline failure path | `c_obs_fresh > D_sense` | `-` | - | - |

## `ObsBeamRecovery`

Bounded-response observer: trigger, wait, response-satisfied edge, violation edge.

### Locations

| Location | Meaning | Coordinates |
|---|---|---|
| `Idle` | baseline idle state | `0,0` |
| `Wait` | observer waiting for bounded response | `300,0` |
| `Violation` | observer deadline violation | `620,-220` |

### Transitions

| Transition | Reason | Guard | Sync | Assignment writes | Sender / listeners |
|---|---|---|---|---|---|
| `Idle -> Wait` | synchronised branch | `-` | `recovery_start?` | `c_obs_beam` | recovery_start: listener here; senders A_BM |
| `Wait -> Idle` | guarded classification branch | `c_obs_beam <= D_BM` | `beam_restored?` | - | beam_restored: listener here; senders A_BM |
| `Wait -> Idle` | guarded classification branch | `c_obs_beam <= D_BM` | `handover_hint?` | - | handover_hint: listener here; senders A_BM |
| `Wait -> Idle` | guarded classification branch | `c_obs_beam <= D_BM` | `beam_failure?` | - | beam_failure: listener here; senders A_BM |
| `Wait -> Violation` | contract/deadline failure path | `c_obs_beam > D_BM` | `-` | - | - |
