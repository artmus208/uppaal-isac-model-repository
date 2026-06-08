# SDN/RIC Template Map

## A_MON

Telemetry monitor: classifies fresh/stale/missing MAC/PHY reports.

| Location | Invariant |
|---|---|
| `MonitorIdle` | `` |
| `CollectReports` | `c_mon <= D_mon` |
| `TelemetryFresh` | `` |
| `TelemetryStale` | `` |
| `TelemetryMissing` | `` |

## A_RISK

Risk classifier over finite telemetry, rule, recovery and slice classes.

| Location | Invariant |
|---|---|
| `RiskLow` | `` |
| `RiskMedium` | `` |
| `RiskHigh` | `` |
| `RiskCritical` | `` |

## A_POLICY

Finite SDN/RIC policy selector with stale telemetry protection.

| Location | Invariant |
|---|---|
| `PolicyIdle` | `` |
| `Evaluate` | `c_dec <= D_decision` |
| `NormalMode` | `` |
| `SensingBoostMode` | `` |
| `CommPriorityMode` | `` |
| `ConstrainedMode` | `` |
| `RejectByPolicy` | `` |

## A_RULE

Rule-miss handling: install, ack, explicit drop or timeout.

| Location | Invariant |
|---|---|
| `RuleStable` | `` |
| `RuleMiss` | `` |
| `RuleInstallPending` | `c_rule <= D_rule_install` |
| `RuleInstalled` | `` |
| `RuleAcked` | `` |
| `RuleTimeout` | `` |
| `RuleDropReason` | `` |

## A_REC

Bounded link/node failure recovery with rollback/failure outcomes.

| Location | Invariant |
|---|---|
| `StableConfig` | `` |
| `FailureDetected` | `` |
| `StandbySwitch` | `c_rec <= D_recovery` |
| `ReactiveReembedding` | `c_rec <= D_recovery` |
| `Rollback` | `c_rollback <= D_rollback` |
| `RecoveryFailed` | `` |

## A_SDN_AGG

Command aggregation and lower-plane acknowledgement timeout.

| Location | Invariant |
|---|---|
| `CommandBuild` | `` |
| `CommandSent` | `` |
| `AwaitAck` | `c_ctrl_ack <= D_ctrl_ack` |
| `Acked` | `` |
| `CommandTimeout` | `` |
