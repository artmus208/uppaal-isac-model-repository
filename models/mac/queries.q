A[] not deadlock
A[] (resourceClass == RES_EXHAUSTED imply !silent_accept)
A[] (A_SCH.WaitPHYAck imply c_phy_ack <= D_phy_ack)
A[] not ObsPhyAck.Violation
A[] not ObsQueueCritical.Violation
A[] not ObsSensingCritical.Violation
E<> A_SCH.SelectMode
E<> A_MAC_AGG.ReportSent
A[] policy_enabled_count >= 1
