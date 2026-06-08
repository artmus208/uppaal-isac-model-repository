# SDN/RIC Channels Map

| Channel | Kind | Role |
|---|---|---|
| `mac_report` | `broadcast` | MAC-to-SDN finite report |
| `phy_kpi_report` | `broadcast` | PHY-to-SDN finite KPI report |
| `service_request` | `broadcast` | Service-to-SDN finite request |
| `service_accept` | `broadcast` | SDN accepts service |
| `service_degraded` | `broadcast` | SDN admits degraded service |
| `service_reject` | `broadcast` | SDN rejects service with reason |
| `rule_miss` | `handshake` | Data plane rule miss |
| `link_failure` | `handshake` | Link failure event |
| `node_failure` | `handshake` | Node failure event |
| `ack` | `handshake` | Lower-plane acknowledgement |
| `sdn_policy_cmd` | `handshake` | Policy command to MAC/lower plane |
| `flow_mod` | `handshake` | Install flow rule |
| `forward_cmd` | `handshake` | Forward command |
| `drop_report` | `handshake` | Explicit drop report |
| `failure_report` | `handshake` | Explicit recovery failure report |
| `timeout_report` | `handshake` | Explicit timeout report |
| `rollback_cmd` | `handshake` | Rollback command |