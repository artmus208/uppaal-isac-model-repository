// C01-deadlock | structural | no verdict
A[] not deadlock
// C01-queue | structural | no verdict
A[] !mac_queue_overflow_seen
// C01-attempts | structural | no verdict
A[] !sdn_attempt_bad
// attempt-protocol | recorder-validity | no verdict
A[] !sdn_attempt_protocol_error
// C02-ack-elapsed | bounded-response-safety | no verdict
A[] (!mac_obs_ack_late && (mac_obs_ack_active imply mac_c_obs_ack <= mac_D_phy_ack))
// queue-nonempty | nonvacuity | no verdict
E<> mac_queue_q > 0
// queue-full | nonvacuity | no verdict
E<> mac_queue_q == mac_queue_K && !mac_queue_overflow_seen
// queue-overflow | negative-result-diagnostic | no verdict
E<> mac_queue_overflow_seen
// attempt-start | nonvacuity | no verdict
E<> sdn_attempt_active
// attempt-primary | nonvacuity | no verdict
E<> sdn_attempt_primary == 1
// attempt-rollback | nonvacuity | no verdict
E<> sdn_attempt_rollback == 1
// attempt-two | nonvacuity | no verdict
E<> sdn_attempt_total == 2
// ack-start | nonvacuity | no verdict
E<> mac_obs_ack_active
// ack-timeout | nonvacuity | no verdict
E<> mac_phy_ack_timeout
// ack-unconditional-completion | completion-diagnostic-not-time-divergence-restricted | no verdict
mac_obs_ack_active --> !mac_obs_ack_active
