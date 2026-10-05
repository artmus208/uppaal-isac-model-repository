E<> true
// C01-deadlock | structural | no verdict
A[] not deadlock
// u0-C01-queue | structural | no verdict
A[] !u0_mac_queue_overflow_seen
// u1-C01-queue | structural | no verdict
A[] !u1_mac_queue_overflow_seen
// u2-C01-queue | structural | no verdict
A[] !u2_mac_queue_overflow_seen
// u3-C01-queue | structural | no verdict
A[] !u3_mac_queue_overflow_seen
// u0-C01-attempts | structural | no verdict
A[] !u0_sdn_attempt_bad
// u1-C01-attempts | structural | no verdict
A[] !u1_sdn_attempt_bad
// u2-C01-attempts | structural | no verdict
A[] !u2_sdn_attempt_bad
// u3-C01-attempts | structural | no verdict
A[] !u3_sdn_attempt_bad
// u0-attempt-protocol | recorder-validity | no verdict
A[] !u0_sdn_attempt_protocol_error
// u1-attempt-protocol | recorder-validity | no verdict
A[] !u1_sdn_attempt_protocol_error
// u2-attempt-protocol | recorder-validity | no verdict
A[] !u2_sdn_attempt_protocol_error
// u3-attempt-protocol | recorder-validity | no verdict
A[] !u3_sdn_attempt_protocol_error
// u0-C02-ack-elapsed | bounded-response-safety | no verdict
A[] (!u0_mac_obs_ack_late && (u0_mac_obs_ack_active imply u0_mac_c_obs_ack <= u0_mac_D_phy_ack))
// u1-C02-ack-elapsed | bounded-response-safety | no verdict
A[] (!u1_mac_obs_ack_late && (u1_mac_obs_ack_active imply u1_mac_c_obs_ack <= u1_mac_D_phy_ack))
// u2-C02-ack-elapsed | bounded-response-safety | no verdict
A[] (!u2_mac_obs_ack_late && (u2_mac_obs_ack_active imply u2_mac_c_obs_ack <= u2_mac_D_phy_ack))
// u3-C02-ack-elapsed | bounded-response-safety | no verdict
A[] (!u3_mac_obs_ack_late && (u3_mac_obs_ack_active imply u3_mac_c_obs_ack <= u3_mac_D_phy_ack))
// u0-queue-nonempty | nonvacuity | no verdict
E<> u0_mac_queue_q > 0
// u1-queue-nonempty | nonvacuity | no verdict
E<> u1_mac_queue_q > 0
// u2-queue-nonempty | nonvacuity | no verdict
E<> u2_mac_queue_q > 0
// u3-queue-nonempty | nonvacuity | no verdict
E<> u3_mac_queue_q > 0
// u0-queue-full | nonvacuity | no verdict
E<> u0_mac_queue_q == u0_mac_queue_K && !u0_mac_queue_overflow_seen
// u1-queue-full | nonvacuity | no verdict
E<> u1_mac_queue_q == u1_mac_queue_K && !u1_mac_queue_overflow_seen
// u2-queue-full | nonvacuity | no verdict
E<> u2_mac_queue_q == u2_mac_queue_K && !u2_mac_queue_overflow_seen
// u3-queue-full | nonvacuity | no verdict
E<> u3_mac_queue_q == u3_mac_queue_K && !u3_mac_queue_overflow_seen
// u0-queue-overflow | negative-result-diagnostic | no verdict
E<> u0_mac_queue_overflow_seen
// u1-queue-overflow | negative-result-diagnostic | no verdict
E<> u1_mac_queue_overflow_seen
// u2-queue-overflow | negative-result-diagnostic | no verdict
E<> u2_mac_queue_overflow_seen
// u3-queue-overflow | negative-result-diagnostic | no verdict
E<> u3_mac_queue_overflow_seen
// u0-attempt-start | nonvacuity | no verdict
E<> u0_sdn_attempt_active
// u1-attempt-start | nonvacuity | no verdict
E<> u1_sdn_attempt_active
// u2-attempt-start | nonvacuity | no verdict
E<> u2_sdn_attempt_active
// u3-attempt-start | nonvacuity | no verdict
E<> u3_sdn_attempt_active
// u0-attempt-primary | nonvacuity | no verdict
E<> u0_sdn_attempt_primary == 1
// u1-attempt-primary | nonvacuity | no verdict
E<> u1_sdn_attempt_primary == 1
// u2-attempt-primary | nonvacuity | no verdict
E<> u2_sdn_attempt_primary == 1
// u3-attempt-primary | nonvacuity | no verdict
E<> u3_sdn_attempt_primary == 1
// u0-attempt-rollback | nonvacuity | no verdict
E<> u0_sdn_attempt_rollback == 1
// u1-attempt-rollback | nonvacuity | no verdict
E<> u1_sdn_attempt_rollback == 1
// u2-attempt-rollback | nonvacuity | no verdict
E<> u2_sdn_attempt_rollback == 1
// u3-attempt-rollback | nonvacuity | no verdict
E<> u3_sdn_attempt_rollback == 1
// u0-attempt-two | nonvacuity | no verdict
E<> u0_sdn_attempt_total == 2
// u1-attempt-two | nonvacuity | no verdict
E<> u1_sdn_attempt_total == 2
// u2-attempt-two | nonvacuity | no verdict
E<> u2_sdn_attempt_total == 2
// u3-attempt-two | nonvacuity | no verdict
E<> u3_sdn_attempt_total == 2
// u0-ack-start | nonvacuity | no verdict
E<> u0_mac_obs_ack_active
// u1-ack-start | nonvacuity | no verdict
E<> u1_mac_obs_ack_active
// u2-ack-start | nonvacuity | no verdict
E<> u2_mac_obs_ack_active
// u3-ack-start | nonvacuity | no verdict
E<> u3_mac_obs_ack_active
// u0-ack-timeout | nonvacuity | no verdict
E<> u0_mac_phy_ack_timeout
// u1-ack-timeout | nonvacuity | no verdict
E<> u1_mac_phy_ack_timeout
// u2-ack-timeout | nonvacuity | no verdict
E<> u2_mac_phy_ack_timeout
// u3-ack-timeout | nonvacuity | no verdict
E<> u3_mac_phy_ack_timeout
// u0-ack-unconditional-completion | completion-diagnostic-not-time-divergence-restricted | no verdict
u0_mac_obs_ack_active --> !u0_mac_obs_ack_active
// u1-ack-unconditional-completion | completion-diagnostic-not-time-divergence-restricted | no verdict
u1_mac_obs_ack_active --> !u1_mac_obs_ack_active
// u2-ack-unconditional-completion | completion-diagnostic-not-time-divergence-restricted | no verdict
u2_mac_obs_ack_active --> !u2_mac_obs_ack_active
// u3-ack-unconditional-completion | completion-diagnostic-not-time-divergence-restricted | no verdict
u3_mac_obs_ack_active --> !u3_mac_obs_ack_active
// shared-capacity | candidate-structural | no verdict
A[] ((family_grant_0 ? 1 : 0) + (family_grant_1 ? 1 : 0) + (family_grant_2 ? 1 : 0) + (family_grant_3 ? 1 : 0) <= 1)
// u0-service-choice | candidate-nonvacuity | no verdict
E<> family_grant_0
// u1-service-choice | candidate-nonvacuity | no verdict
E<> family_grant_1
// u2-service-choice | candidate-nonvacuity | no verdict
E<> family_grant_2
// u3-service-choice | candidate-nonvacuity | no verdict
E<> family_grant_3
// joint-backlog | candidate-nonvacuity | no verdict
E<> u0_mac_queue_q > 0 && u1_mac_queue_q > 0 && u2_mac_queue_q > 0 && u3_mac_queue_q > 0
A[] ((family_grant_0 ? 1 : 0) + (family_grant_1 ? 1 : 0) + (family_grant_2 ? 1 : 0) + (family_grant_3 ? 1 : 0) <= 1)
E<> family_grant_0
E<> family_grant_1
E<> family_grant_2
E<> family_grant_3
E<> u0_mac_queue_q > 0 && u1_mac_queue_q > 0 && u2_mac_queue_q > 0 && u3_mac_queue_q > 0
A[] !u0_mac_queue_overflow_seen
A[] !(u0_mac_queue_overflow_seen || u1_mac_queue_overflow_seen || u2_mac_queue_overflow_seen || u3_mac_queue_overflow_seen)
E<> u0_mac_queue_q == u0_mac_queue_K && !u0_mac_queue_overflow_seen
