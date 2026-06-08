# MAC Template Map

## A_SCH

Scheduler: collects KPI, selects finite MAC policy, sends PHY command, waits for ack.

| Location | Meaning | Invariant |
|---|---|---|
| `Idle` | MAC state | `` |
| `CollectKPI` | MAC state | `c_sched <= D_collect` |
| `SelectMode` | MAC state | `c_sched <= D_sched` |
| `ApplySchedule` | MAC state | `` |
| `WaitPHYAck` | MAC state | `c_phy_ack <= D_phy_ack` |
| `ScheduleFailure` | MAC state | `` |

## A_Q

Queue monitor: reacts to critical queue class before D_queue_crit.

| Location | Meaning | Invariant |
|---|---|---|
| `QueueNormal` | MAC state | `` |
| `QueueWarning` | MAC state | `` |
| `QueueCritical` | MAC state | `c_queue <= D_queue_crit` |
| `QueueDraining` | MAC state | `` |

## A_BUF

Buffer monitor: reports overflow before D_buf_report.

| Location | Meaning | Invariant |
|---|---|---|
| `BufferSafe` | MAC state | `` |
| `BufferWarning` | MAC state | `` |
| `BufferOverflow` | MAC state | `c_buf <= D_buf_report` |

## A_RSRC

Resource conflict monitor: prevents silent accept under exhausted resource.

| Location | Meaning | Invariant |
|---|---|---|
| `ResourceAvailable` | MAC state | `` |
| `ResourceTight` | MAC state | `` |
| `ResourceConflict` | MAC state | `` |
| `ResourceExhausted` | MAC state | `` |

## A_MAC_AGG

MAC report aggregator: builds and broadcasts MAC report payload.

| Location | Meaning | Invariant |
|---|---|---|
| `ReportIdle` | MAC state | `` |
| `ReportBuild` | MAC state | `c_report <= D_mac_report` |
| `ReportSent` | MAC state | `` |
| `ReportStale` | MAC state | `` |
