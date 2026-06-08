# MAC Policy Map

| Policy | Guard | Mode | Outcome |
|---|---|---|---|
| `P0` | `resourceClass == RES_EXHAUSTED || mappedResourceClass == RES_EXHAUSTED` | `SCH_CONSTRAINED` | resource_reject! or mac_report! by D_sched |
| `P1` | `bufferClass == B_OVERFLOW || delayClass == D_VIOLATED` | `SCH_COMM` | protect communication and report SDN/RIC |
| `P2` | `queueClass == Q_CRIT && commDemand == COMM_CRITICAL` | `SCH_COMM` | mac_schedule_cmd! or mac_report! |
| `P3` | `sensingDemand == SENS_CRITICAL && SDN allows sensing priority` | `SCH_SENS or SCH_JOINT` | sensing_boost_cmd! or constrained_mode_cmd! |
| `P4` | `resourceClass == RES_TIGHT and both demands active` | `SCH_JOINT or SCH_CONSTRAINED` | joint scheduling or deficit report |
| `P5` | `KPIFreshnessClass stale or missing` | `SCH_CONSTRAINED` | avoid aggressive reconfiguration |
| `P6` | `ResourceClass free or balanced` | `SCH_JOINT` | ordinary ISAC schedule |
| `P7` | `fallback` | `SCH_CONSTRAINED` | safe fallback |
