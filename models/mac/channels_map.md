# MAC Channels Map

| Channel | Kind | Role |
|---|---|---|
| `phy_kpi_report` | `broadcast` | PHY-to-MAC finite KPI report |
| `mac_report` | `broadcast` | MAC-to-SDN/RIC report |
| `mac_tick` | `handshake` | scheduling window tick |
| `sdn_policy_cmd` | `handshake` | finite SDN/RIC policy command |
| `service_priority` | `handshake` | service priority update |
| `phy_ack` | `handshake` | PHY command acknowledgement |
| `mac_schedule_cmd` | `handshake` | PHY scheduling command |
| `beam_update_cmd` | `handshake` | PHY beam update command |
| `sensing_boost_cmd` | `handshake` | PHY sensing boost command |
| `constrained_mode_cmd` | `handshake` | PHY constrained mode command |
| `resource_reject` | `handshake` | explicit resource rejection |
