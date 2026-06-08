A[] not deadlock
E<> A_PH.PHYNormal
E<> A_PH.PHYSensingDegraded
E<> A_PH.PHYCommunicationDegraded
E<> A_PH.PHYJointDegraded
A[] (A_PH.PHYNormal imply (comm_ok && sensing_qos_ok))
A[] (ch_enabled_count <= 1)
A[] (sq_enabled_count <= 1)
A[] (A_BM.BeamRecover imply c_rec <= D_BM)
A[] not ObsSenseReport.Violation
A[] not ObsFreshness.Violation
A[] not ObsBeamRecovery.Violation
A[] (ass_ch() imply not A_CH.ContractViolation_CH)
A[] (ass_sig() imply not A_SIG.ContractViolation_SIG)
A[] (ass_bm() imply not A_BM.ContractViolation_BM)
A[] (ass_sq() imply not A_SQ.ContractViolation_SQ)
A[] (ass_ph() imply not A_PH.ContractViolation_PH)
