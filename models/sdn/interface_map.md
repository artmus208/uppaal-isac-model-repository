# SDN/RIC Interface Map

| Procedure | Trigger | Deadline | Outcomes |
|---|---|---|---|
| `rule_miss` | `rule_miss?` | `D_rule_install` | flow_mod!, forward_cmd!, drop_report!, timeout_report! |
| `recovery` | `link_failure? | node_failure?` | `D_recovery + D_rollback` | sdn_policy_cmd!, flow_mod!, rollback_cmd!, failure_report! |
| `sensing_degradation` | `mac_report? | phy_kpi_report?` | `D_decision` | sdn_policy_cmd!, service_degraded!, service_reject! |
| `service_admission` | `service_request?` | `D_admission` | service_accept!, service_degraded!, service_reject! |