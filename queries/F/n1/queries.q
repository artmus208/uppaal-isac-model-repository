// C01-deadlock | structural | no verdict
A[] not deadlock
// u0-C01-queue | structural | no verdict
A[] !u0_mac_queue_overflow_seen
// u0-C01-attempts | structural | no verdict
A[] !u0_sdn_attempt_bad
// u0-attempt-protocol | recorder-validity | no verdict
A[] !u0_sdn_attempt_protocol_error
// u0-C02-ack-elapsed | bounded-response-safety | no verdict
A[] (!u0_mac_obs_ack_late && (u0_mac_obs_ack_active imply u0_mac_c_obs_ack <= u0_mac_D_phy_ack))
// u0-queue-nonempty | nonvacuity | no verdict
E<> u0_mac_queue_q > 0
// u0-queue-full | nonvacuity | no verdict
E<> u0_mac_queue_q == u0_mac_queue_K && !u0_mac_queue_overflow_seen
// u0-queue-overflow | negative-result-diagnostic | no verdict
E<> u0_mac_queue_overflow_seen
// u0-attempt-start | nonvacuity | no verdict
E<> u0_sdn_attempt_active
// u0-attempt-primary | nonvacuity | no verdict
E<> u0_sdn_attempt_primary == 1
// u0-attempt-rollback | nonvacuity | no verdict
E<> u0_sdn_attempt_rollback == 1
// u0-attempt-two | nonvacuity | no verdict
E<> u0_sdn_attempt_total == 2
// u0-ack-start | nonvacuity | no verdict
E<> u0_mac_obs_ack_active
// u0-ack-timeout | nonvacuity | no verdict
E<> u0_mac_phy_ack_timeout
// u0-ack-unconditional-completion | completion-diagnostic-not-time-divergence-restricted | no verdict
u0_mac_obs_ack_active --> !u0_mac_obs_ack_active
// shared-capacity | candidate-structural | no verdict
A[] ((family_grant_0 ? 1 : 0) <= 1)
// u0-service-choice | candidate-nonvacuity | no verdict
E<> family_grant_0
