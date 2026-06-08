# SDN/RIC Policy Map

| Policy | Guard | Mode | Outcome |
|---|---|---|---|
| `POL_REJECT` | `riskClass == RISK_CRIT || sliceClass == SLICE_VIOLATED || recoveryClass == REC_FAILED` | `RejectByPolicy` | service_reject/drop_report with reason |
| `POL_CONSTRAINED` | `telemetryClass == TEL_STALE || telemetryClass == TEL_MISSING || riskClass == RISK_HIGH || sliceClass == SLICE_WARN` | `ConstrainedMode` | conservative command or degraded service |
| `POL_REROUTE` | `(ruleClass == RULE_MISS || link_failure_pending || node_failure_pending) && finite alternative && fresh telemetry` | `NormalMode/Reroute` | flow_mod or standby command |
| `POL_SENS_BOOST` | `sensing_degradation_pending && fresh telemetry && riskClass != RISK_CRIT` | `SensingBoostMode` | sdn_policy_cmd and service_degraded |
| `POL_COMM_PRIO` | `service_request_pending && sliceClass != SLICE_VIOLATED && fresh telemetry` | `CommPriorityMode` | service_accept and policy command |
| `POL_NORMAL` | `fallback when no higher-priority guard holds` | `NormalMode` | maintain current rules/slices |