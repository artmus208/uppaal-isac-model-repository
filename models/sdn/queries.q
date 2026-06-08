A[] not deadlock
A[] (A_RULE.RuleInstallPending imply c_rule <= D_rule_install)
A[] (telemetryClass == TEL_STALE imply !optimistic_reconfig)
A[] (telemetryClass == TEL_MISSING imply !optimistic_reconfig)
A[] (recoveryClass == REC_FAILED imply failure_report_sent)
A[] not ObsRuleMiss.Violation
A[] not ObsRecovery.Violation
A[] not ObsAdmission.Violation
A[] not ObsStaleTelemetry.Violation
E<> A_POLICY.Evaluate
E<> A_RULE.RuleTimeout
E<> A_REC.RecoveryFailed
A[] policy_enabled_count >= 1
