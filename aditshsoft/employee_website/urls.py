from employee_website.views import *
from django.conf.urls import include
from django.conf.urls import url

# Knowledge and Training
urlpatterns = [
    url(r'^hrms/employeeservices/recruitement/updateconsultants/list/$', EmployeeServicesRecruitementUpdateConsultantsList.as_view(), name='crm_website_employeeservices_recruitement_updateconsultants_list'),
    url(r'^hrms/employeeservices/recruitement/updateconsultants/add/$', AddEditCrmEmployeeServicesRecruitementUpdateConsultants.as_view(), name='crm_website_employeeservices_recruitement_updateconsultants_add'),
    url(r'^hrms/employeeservices/recruitement/updateconsultants/edit/(?P<id>[0-9,a-z,A-Z]+)/$', EditCrmEmployeeServicesRecruitementUpdateConsultants, name="crm_website_employeeservices_recruitement_updateconsultants_edit"),
    url(r'^hrms/employeeservices/recruitement/updateconsultants/delete/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeServicesRecruitementUpdateConsultantsDelete.as_view(), name='crm_website_employeeservices_recruitement_updateconsultants_delete'),
    url(r'^hrms/employeeservices/recruitement/createrequirement/list/$', EmployeeServicesRecruitementCreateRequirementList.as_view(), name='crm_website_employeeservices_recruitement_createrequirement_list'),
   
    url(r'^hrms/employeeservices/recruitement/createrequirement/add/$', AddEditCrmEmployeeServicesRecruitementCreateRequirement.as_view(), name='crm_website_employeeservices_recruitement_createrequirement_add'),
    url(r'^hrms/employeeservices/recruitement/createrequirement/edit/(?P<id>[0-9,a-z,A-Z]+)/$', AddEditCrmEmployeeServicesRecruitementCreateRequirement.as_view(), name="crm_website_employeeservices_recruitement_createrequirement_edit"),
    url(r'^hrms/employeeservices/recruitement/createrequirement/delete/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeServicesRecruitementCreateRequirementDelete.as_view(), name='crm_website_employeeservices_recruitement_createrequirement_delete'),
    url(r'^hrms/employeeservices/approval/vacancy/(?P<id>[0-9,a-z,A-Z]+)/$', ApprovalVacancies.as_view(), name='approval_vacancy_update_status'),
    url(r'^hrms/employeeservices/recruitement/approvevacancies/list/$', EmployeeServicesRecruitementApproveVacanciesList.as_view(), name='crm_website_employeeservices_recruitement_approvevacancies_list'),
    url(r'^hrms/employeeservices/recruitement/approvevacancies/update/(?P<id>[0-9,a-z,A-Z]+)/$', AddEditCrmEmployeeServicesRecruitementApproveVacancies.as_view(), name='crm_website_employeeservices_recruitement_approvevacancies_update'),
    url(r'^hrms/employeeservices/recruitement/publishvacancies/list/$', EmployeeServicesRecruitementPublishVacanciesList.as_view(), name='crm_website_employeeservices_recruitement_publishvacancies_list'),
    url(r'^hrms/employeeservices/recruitement/publishvacancies/update/(?P<id>[0-9,a-z,A-Z]+)/$', AddEditCrmEmployeeServicesRecruitementPublishVacancies.as_view(), name='crm_website_employeeservices_recruitement_publishvacancies_update'),
    url(r'^hrms/employeeservices/recruitement/inviteresume/list/$', EmployeeServicesRecruitementInviteResumeList.as_view(), name='crm_website_employeeservices_recruitement_inviteresume_list'),
    url(r'^hrms/employeeservices/recruitement/inviteresume/add/$', AddEditCrmEmployeeServicesRecruitementInviteResume.as_view(), name='crm_website_employeeservices_recruitement_inviteresume_add'),
   
    url(r'^hrms/employeeservices/recruitement/resume/$', AddEmployeeServicesRecruitementResume, name='crm_website_employeeservices_recruitement_list1'),
    url(r'^hrms/employeeservices/recruitement/resume/add/$', AddUpdateEmployeeServicesRecruitementResumeView, name='crm_website_employeeservices_recruitement_list'),
    
    
    url(r'^hrms/employeeservices/recruitement/resumes/add/$', AddEditCrmEmployeeServicesRecruitementResume.as_view(), name='crm_website_employeeservices_recruitement_inviteresume_add1'),
    url(r'^hrms/employeeservices/recruitement/inviteresume/edit/(?P<id>[0-9,a-z,A-Z]+)/$', AddEditCrmEmployeeServicesRecruitementInviteResume.as_view(), name="crm_website_employeeservices_recruitement_inviteresume_edit"),
    url(r'^hrms/employeeservices/recruitement/inviteresume/delete/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeServicesRecruitementInviteResumeDelete.as_view(), name='crm_website_employeeservices_recruitement_inviteresume_delete'),

#################  PsychometricTest
    url(r'^hrms/employeeservices/recruitement/psychometric/test/list/$', EmployeeServicesRecruitementPsychometricTestList.as_view(), name='crm_website_employeeservices_recruitement_psychometrictest_list'),
    url(r'^hrms/employeeservices/recruitement/psychometric/test/add/$', AddEditCrmEmployeeServicesRecruitementPsychometricTest.as_view(), name='crm_website_employeeservices_recruitement_psychometrictest_add'),
    url(r'^hrms/employeeservices/recruitement/psychometric/test/edit/(?P<id>[0-9,a-z,A-Z]+)/$', AddEditCrmEmployeeServicesRecruitementPsychometricTest.as_view(), name="crm_website_employeeservices_recruitement_psychometrictest_edit"),
    url(r'^hrms/employeeservices/recruitement/psychometric/test/delete/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeServicesRecruitementPsychometricTestDelete.as_view(), name='crm_website_employeeservices_recruitement_psychometrictest_delete'),

    ####


    url(r'^hrms/employeeservices/recruitement/shortlistedresume/list/$', EmployeeServicesRecruitementResumeShortlistedList.as_view(), name='crm_website_employeeservices_recruitement_shortlistedresume_list'),
    url(r'^hrms/employeeservices/recruitement/interviewstatus/list/$', EmployeeServicesRecruitementCandidatesInterViewStatusList.as_view(), name='crm_website_employeeservices_recruitement_interviewstatus_list'),
    url(r'^hrms/employeeservices/recruitement/candidatesshortlisted/list/$', EmployeeServicesRecruitementCandidateShortlistedList.as_view(), name='crm_website_employeeservices_recruitement_candidateshortlisted_list'),
    url(r'^hrms/employeeservices/recruitement/interviewstatus/update/(?P<id>[0-9,a-z,A-Z]+)/$', AddEditCrmEmployeeServicesInterViewStatus.as_view(), name="crm_website_employeeservices_recruitement_interview_status_update"),
    url(r'^hrms/employeeservices/recruitement/candidatesshortlisted/update/(?P<id>[0-9,a-z,A-Z]+)/$', AddEditCrmEmployeeServicesRecruitementCandidatesShortlisted.as_view(), name="crm_website_employeeservices_recruitement_candidatesshortlisted_update"),
    url(r'^hrms/employeeservices/recruitement/offerstatus/list/$', EmployeeServicesRecruitementOfferStatusList.as_view(), name='crm_website_employeeservices_recruitement_offer_status_list'),
    
    url(r'^hrms/employeeservices/recruitement/document/list/$', EmployeeServicesRecruitementDocumentList.as_view(), name='crm_website_employeeservices_recruitement_document_list'),
    url(r'^hrms/employeeservices/recruitement/document/update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeServicesRecruitementDocumentadd.as_view(), name='crm_website_employeeservices_recruitement_document_add'),
    # url(r'^hrms/employeeservices/recruitement/document/update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeServicesRecruitementDocumentEdit.as_view(), name='crm_website_employeeservices_recruitement_document_edit'),
    # url(r'^hrms/employeeservices/recruitement/document/delete/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeServicesRecruitementDocumentDelete.as_view(), name='crm_website_employeeservices_recruitement_document_delete'),

    url(r'^hrms/employeeservices/recruitement/candidateofferstatus/update/(?P<id>[0-9,a-z,A-Z]+)/$', AddEditCrmEmployeeServicesRecruitementCandidatesOfferStatus.as_view(), name="crm_website_employeeservices_recruitement_candidateofferstatus_update"),
    url(r'^hrms/employeeservices/recruitement/candidateofferstatus/change/(?P<id>[0-9,a-z,A-Z]+)/$', AddEditCrmEmployeeServicesRecruitementCandidatesOfferUpdateStatus.as_view(), name="crm_website_employeeservices_recruitement_candidateofferstatus_change"),
    url(r'^hrms/employeeservices/recruitement/vacancystatus/list/$', EmployeeServicesRecruitementVacancyStatusList.as_view(), name='crm_website_employeeservices_recruitement_vacancystatus_list'),
    url(r'^hrms/employeeservices/employeeregistration/updateregistrations/list/$', EmployeeServicesEmployeeRegistrationUpdateRegistrationsList.as_view(), name='crm_website_employeeservices_employeeregistration_updateregistrations_list'),
    ##
    url(r'^hrms/employeeservices/employeeregistration/updateregistrations/add/$', AddEmployeeServicesEmployeeRegistrationUpdateRegistrations.as_view(), name='crm_website_employeeservices_employeeregistration_updateregistrations_add'),
    url(r'^hrms/employeeservices/recruitement/offerlaytter/list/$', EmployeeServicesEmployeeOfferLatter.as_view(), name='crm_website_employeeservices_offer_latter_list'),
    url(r'^hrms/employeeservices/employeeregistration/updateregistrations/edit/(?P<id>[0-9,a-z,A-Z]+)/$', EditEmployeeServicesEmployeeRegistrationUpdateRegistrations.as_view(), name="crm_website_employeeservices_employeeregistration_updateregistrations_edit"),
    url(r'^hrms/employeeservices/employeeregistration/updateregistrations/delete/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeServicesEmployeeRegistrationUpdateRegistrationsDelete.as_view(), name="crm_website_employeeservices_employeeregistration_updateregistrations_delete"),
    url(r'^hrms/employeeservices/employeeregistration/updatedepartment/update/$', AddEditCrmEmployeeEmployeeRegistrationUpdateDepartment.as_view(), name='crm_website_employeeservices_employeeregistration_updatedeaprtment_update'),
    url(r'^hrms/employeeservices/employeeregistration/updatedepartment/json/$', AddEditCrmEmployeeEmployeeRegistrationUpdateDepartmentJsonEmployee.as_view(), name='crm_website_employeeservices_employeeregistration_updatedeaprtment_json'),
    url(r'^hrms/employeeservices/employeeregistration/employee/list/$', EmployeeServicesEmployeeRegistrationEmployeeListList.as_view(), name='crm_website_employeeservices_employeeregistration_employee_list'),
   
    url(r'^hrms/employeeservices/employeeregistration/employee/update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeServicesEmployeeRegistrationEmployeeUpdate.as_view(), name='crm_website_employeeservices_employeeregistration_employee_update'),

    url(r'^hrms/employeeservices/employeeregistration/add/verificationreport/(?P<id>[0-9,a-z,A-Z]+)/$', AddEmployeeServicesEmployeeRegistrationVerficationReport.as_view(), name='crm_website_employeeservices_employeeregistration_verficationreport_add'),
    url(r'^hrms/employeeservices/employeeregistration/add/documents/(?P<id>[0-9,a-z,A-Z]+)/$', AddEmployeeServicesEmployeeRegistrationDocument.as_view(), name='crm_website_employeeservices_employeeregistration_document_add'),
    # Leaves
    url(r'^hrms/employeeservices/employee/leavequota/list/$', LeavesUpdateLeaveQuotaOfEmployesListView.as_view(), name='crm_website_employeeservices_employees_leavequota_list'),
    url(r'^hrms/employeeservices/employee/leavequota/add/$', LeavesUpdateLeaveQuotaOfEmployesAddView.as_view(), name='crm_website_employeeservices_employees_leavequota_add'),
    url(r'^hrms/employeeservices/employee/leavequota/update/(?P<id>[0-9,a-z,A-Z]+)/$', LeavesUpdateLeaveQuotaOfEmployesUpdateView.as_view(), name="crm_website_employeeservices_employees_leavequota_update"),
    url(r'^hrms/employeeservices/employee/leavequota/delete/(?P<id>[0-9,a-z,A-Z]+)/$', LeavesUpdateLeaveQuotaOfEmployesUpdateViewDelete.as_view(), name="crm_website_employeeservices_employees_leavequota_delete"),
    url(r'^hrms/employeeservices/leaves/apply/$', EmployeeLeavesLeaveRequestPostLeave.as_view(), name='crm_website_employeeservices_leaves_apply'),
    url(r'^hrms/employeeservices/leaves/cancel/(?P<id>[0-9,a-z,A-Z]+)/$', LeavesUpdateLeaveQuotaOfEmployesUpdateViewCancel.as_view(), name='crm_website_employeeservices_leaves_cancele'),
    url(r'^hrms/employeeservices/leaves/quota/$', EmployeeLeavesLeaveRequestPostLeaveJsonData.as_view(), name='crm_website_employeeservices_leaves_quota'),
    url(r'^hrms/employeeservices/leaves/pendingforapproval/list/$', EmployeeLeavesLeaveRequestPendingforApprovalList.as_view(), name='crm_website_employeeservices_leave_pendingforapproval_list'),
    url(r'^hrms/employeeservices/leaves/pendingforapproval/status/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeLeavesLeaveRequestPostLeaveUpdate.as_view(), name="crm_website_employeeservices_leave_pendingforapproval_status"),
    url(r'^hrms/employeeservices/leaves/approved/list/$', EmployeeLeavesLeaveRequestApprovedLeaveList.as_view(), name="crm_website_employeeservices_leave_approved_list"),
    url(r'^hrms/employeeservices/leaves/rejected/list/$', EmployeeLeavesLeaveRequestRejectedLeaveList.as_view(), name="crm_website_employeeservices_leave_rejected"),
    url(r'^hrms/employeeservices/leaves/mybalance/list/$', EmployeeLeavesLeaveRequestMyBalanceLeaveList.as_view(), name="crm_website_employeeservices_leave_mybalance"),
    # Attendance
    url(r'^hrms/employeeservices/attendance/upload/$', EmployeeAttendanceUploadAttendanceUpdate.as_view(), name='crm_employee_services_attendance_upload_attendance'),
    url(r'^hrms/employeeservices/attendance/correction/list/$', EmployeeAttendanceUpdateAttendanceList.as_view(), name='crm_employee_services_attendance_update_list'),
    url(r'^hrms/employeeservices/attendance/update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeAttendanceUpdateAttendanceUpdate.as_view(), name='crm_employee_services_attendance_update'),
    url(r'^hrms/employeeservices/attendance/status/$', EmployeeAttendanceAttendanceStatusList.as_view(), name='crm_employee_services_attendance_status'),
    url(r'^hrms/employeeservices/attendance/status/update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeAttendanceAttendanceStatusUpdate.as_view(), name='crm_employee_services_attendance_update'),
    
    
    # HR Policies
    url(r'^hrms/employeeservices/hrpolicies/updatepolicies/$', EmployeeHRPoliciesUpdatePolicy.as_view(), name='crm_employee_services_hrpolicies_upload_update_policies'),
    url(r'^hrms/employeeservices/hrpolicies/updatepolicies/edit/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeHRPoliciesUpdatePolicy.as_view(), name='crm_employee_services_hrpolicies_upload_policies_edit'),
    url(r'^hrms/employeeservices/hrpolicies/updateforms/$', EmployeeHRPoliciesUpdateForms.as_view(), name='crm_employee_services_hrpolicies_upload_update_forms'),
    url(r'^hrms/employeeservices/hrpolicies/updateforms/edit/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeHRPoliciesUpdateForms.as_view(), name='crm_employee_services_hrpolicies_upload_forms_edit'),
    url(r'^hrms/employeeservices/hrpolicies/updatecirculars/$', EmployeeHRUpdateCircularsForms.as_view(), name='crm_employee_services_hrpolicies_upload_update_circulars'),
    url(r'^hrms/employeeservices/hrpolicies/updatecirculars/edit/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeHRUpdateCircularsForms.as_view(), name='crm_employee_services_hrpolicies_upload_circulars_edit'),
    url(r'^hrms/employeeservices/hrpolicies/updatepolicies/list/$', EmployeeHRPoliciesUpdatePolicyList.as_view(), name='crm_employee_services_hrpolicies_upload_update_policies_list'),
    url(r'^hrms/employeeservices/hrpolicies/updatecirculars/list/$', EmployeeHRPoliciesUpdateCircularsmodelList.as_view(), name='crm_employee_services_hrpolicies_upload_update_circulars_list'),
    url(r'^hrms/employeeservices/hrpolicies/updateforms/list/$', EmployeeHRPoliciesUpdateFormmodelList.as_view(), name='crm_employee_services_hrpolicies_upload_update_forms_list'),
    # Claim And Reimbursement
    url(r'^hrms/employeeservices/claimandreimbursement/submitclaims/$', EmployeeClaimandReimbursementSubmitClaimsFormView.as_view(), name='crm_employee_services_claimandreimbursement_submitclaims'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitclaims/approved/list/$', EmployeeClaimandReimbursementSubmitClaimsApprovedListView.as_view(), name='crm_employee_services_claimandreimbursement_submitclaims_approved_list'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitclaims/pending/list/$', EmployeeClaimandReimbursementSubmitClaimsListView.as_view(), name='crm_employee_services_claimandreimbursement_submitclaims_list'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitclaims/pending/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeClaimandReimbursementSubmitClaimsApprovedView.as_view(), name='crm_employee_services_claimandreimbursement_submitclaims_approved'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitclaims/processing/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeClaimandReimbursementApprovedDateOfProcessingView.as_view(), name='crm_employee_services_claimandreimbursement_submitclaims_processing'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitclaims/claimprocessed/list/$', EmployeeClaimandReimbursementClaimClaimProcessedListView.as_view(), name='crm_employee_services_claimandreimbursement_claim_claimprocessed_list'),
    
    url(r'^hrms/employeeservices/claimandreimbursement/submitclaims/claimprocessed/updates/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeClaimandReimbursementClaimClaimProcessedUpdatesView.as_view(), name='crm_employee_services_claimandreimbursement_claim_claimprocessed_update'),
    
    url(r'^hrms/employeeservices/claimandreimbursement/submitclaims/claimprocess/list/$', EmployeeClaimandReimbursementSubmitReimbursementApprovedClaimToProcessView.as_view(), name='crm_employee_services_claimandreimbursement_claimprocessing_list'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitclaims/status/list/$', EmployeeClaimandReimbursementClaimStatusListView.as_view(), name='crm_employee_services_claimandreimbursement_claim_status_list'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitreimbursement/$', EmployeeClaimandReimbursementSubmitReimbursementFormView.as_view(), name='crm_employee_services_claimandreimbursement_submitreimbursement'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitreimbursement/update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeClaimandReimbursementSubmitReimbursementListView.as_view(), name='crm_employee_services_claimandreimbursement_submitreimbursement_update'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitreimbursement/update/status/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeClaimandReimbursementSubmitReimbursementApprovedDateOfProcessingView.as_view(), name='crm_employee_services_claimandreimbursement_submitreimbursement_update_staus'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitreimbursement/pending/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeClaimandReimbursementSubmitReimbursementApprovedView.as_view(), name='crm_employee_services_claimandreimbursement_submitreimbursement_approved'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitreimbursement/approved/list/$', EmployeeClaimandReimbursementSubmitReimbursementApprovedListView.as_view(), name='crm_employee_services_claimandreimbursement_submitreimbursement_approved_list'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitreimbursement/reimbursementprocessing/list/$', EmployeeClaimandReimbursementSubmitReimbursementApprovedClaimToProcessListView.as_view(), name='crm_employee_services_claimandreimbursement_submitreimbursement_reimbursementprocessing_list'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitreimbursement/reimbursementprocessed/list/$', EmployeeClaimandReimbursementReimbursementRejectedListView.as_view(), name='crm_employee_services_claimandreimbursement_submitreimbursement_reimbursement_reimbursementprocessed_list'), 
    url(r'^hrms/employeeservices/claimandreimbursement/submitreimbursement/reimbursementprocessed/Update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeClaimandReimbursementReimbursementRejectedUpdateView.as_view(), name='crm_employee_services_claimandreimbursement_submitreimbursement_reimbursement_reimbursementprocessed_Update'),
    url(r'^hrms/employeeservices/claimandreimbursement/submitreimbursement/status/list/$', EmployeeClaimandReimbursementRembursementStatusListView.as_view(), name='crm_employee_services_claimandreimbursement_submitreimbursement_reimbursement_status_list'),
    # Payroll
    url(r'^hrms/employeeservices/payroll/accept/attendance/list/$', EmployeePayrollProcessingAcceptAttendanceListView.as_view(), name='crm_employee_services_payroll_accept_attendance_list'),
    ####
    url(r'^hrms/employeeservices/payroll/accept/attendance/update/(?P<id>[0-9,a-z,A-Z]+)/$',UserAcceptAttendanceUpdateFormView.as_view(), name='crm_employee_services_payroll_accept_attendance_update'),
    url(r'^hrms/employeeservices/payroll/accept/overtime/list/$', EmployeePayrollProcessingAcceptOverTimeListView.as_view(), name='crm_employee_services_payroll_accept_overtime_list'),
    url(r'^hrms/employeeservices/payroll/update/leaves/list/$', EmployeePayrollUpdateLeavesListView.as_view(), name='crm_employee_services_payroll_update_leave_list'),
    url(r'^hrms/employeeservices/payroll/claim/update/list/$', EmployeePayrollAcceptClaimsView.as_view(), name='crm_employee_services_payroll_claim_update_list'),
    url(r'^hrms/employeeservices/payroll/reimbursement/update/list/$', EmployeePayrollUpdateReimbursementView.as_view(), name='crm_employee_services_payroll_reimbursement_update_list'),
    url(r'^hrms/employeeservices/payroll/update/advances/list/$', EmployeePayrollUpdateAdvancesView.as_view(), name='crm_employee_services_payroll_update_advances_list'),
    url(r'^hrms/employeeservices/payroll/update/incentive/list/$', EmployeePayrollIncentivesView.as_view(), name='crm_employee_services_payroll_update_incentive_list'),
    
    url(r'^hrms/employeeservices/payroll/tax/declaration/list/$', EmployeeUpdateTaxDeclarationView.as_view(), name='crm_employee_services_payroll_tax_declaration_list'),
    url(r'^hrms/employeeservices/payroll/tax/declaration/update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeUpdateTaxDeclarationUpdateView, name='crm_employee_services_payroll_tax_declaration_update'),
    
    url(r'^hrms/employeeservices/payroll/tax/recovery/list/$', EmployeeUpdateTaxRecoveryView.as_view(), name='crm_employee_services_payroll_tax_recovery_list'),
    url(r'^hrms/employeeservices/payroll/tax/recovery/update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeUpdateTaxRecoveryUpdateView, name='crm_employee_services_payroll_tax_recovery_update'),
    
    url(r'^hrms/employeeservices/payroll/tax/calculation/list/$', EmployeePayrollProcessingTaxCalculationView.as_view(), name='crm_employee_services_payroll_tax_calculation_list'),
    url(r'^hrms/employeeservices/payroll/tax/calculation/update(?P<id>[0-9,a-z,A-Z]+)/$', EmployeePayrollProcessingTaxCalculationUpdateView, name='crm_employee_services_payroll_tax_calculation_update'),    
    url(r'^hrms/employeeservices/payroll/update/recovery/list/$', EmployeePayrollProcessingUpdateRecoveriesView.as_view(), name='crm_employee_services_payroll_update_recovery_list'),
    url(r'^hrms/employeeservices/payroll/update/recovery/add/$', EmployeePayrollProcessingUpdateRecoveriesAdd, name='crm_employee_services_payroll_update_recovery_add'),
    url(r'^hrms/employeeservices/payroll/update/recovery/update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeePayrollProcessingUpdateRecoveriesUpdate, name='crm_employee_services_payroll_update_recovery_update'),
    
    url(r'^hrms-employee/emplyeesservices/managepayroll/statutorydeduction/list/$', EmployeeSalaryDeductionsListAddView.as_view(), name='crm_crmemployee_manageemployee_statutorydeductions_list'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/statutorydeduction/update/(?P<id>[0-9,a-z,A-Z]+)/$', PayrollStatutoryDeductionsUpdateView, name='crm_crmemployee_manageemployee_statutorydeductions_update'),
    
    
    url(r'^hrms-employee/emplyeesservices/managepayroll/salaryvoucher/list/$', PayrollSalaryVoucherListAddView.as_view(), name='crm_crmemployee_manageemployee_salaryvoucher_list'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/salaryvoucher/update/(?P<id>[0-9,a-z,A-Z]+)/$', PayrollSalaryVoucherListUpdateView, name='crm_crmemployee_manageemployee_salaryvoucher_update'),
    
    url(r'^hrms-employee/emplyeesservices/managepayroll/salarydisbursement/list/$', PayrollSalaryDisbursementListAddView.as_view(), name='crm_crmemployee_manageemployee_salarydisbursement_list'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/salarydisbursement/add/$', PayrollSalaryDisbursementListAddFormView, name='crm_crmemployee_manageemployee_salarydisbursement_add'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/salarydisbursement/update/(?P<id>[0-9,a-z,A-Z]+)/$', PayrollSalaryDisbursementListUpdate, name='crm_crmemployee_manageemployee_salarydisbursement_update'),
   
   
    # Key Responsibility Areas & Targets
    url(r'^hrms/employeeservices/update/kraandtarget/$', AddEditKeyResponsibilityAreasUpdateTargetsKRATargetsView.as_view(), name='crm_employee_services_payroll_keyresponsibilityareas_update_kra'),
    url(r'^hrms/employeeservices/kraandtarget/performance/list/$', KeyResponsibilityAreasTargetsKRATargetsPerformanceListView.as_view(), name='crm_employee_services_payroll_kra_target_performance_list'),
    url(r'^hrms/employeeservices/kraandtarget/review/list/$', KeyResponsibilityAreasTargetsKRATargetsReviewListView.as_view(), name='crm_employee_services_payroll_kra_target_review_list'),
    url(r'^hrms/employeeservices/kraandtarget/performance/update/(?P<id>[0-9,a-z,A-Z]+)/$', KeyResponsibilityAreasTargetsKRATargetsPerformanceUpdateView.as_view(), name='crm_employee_services_kra_target_performance_update'),
    # Resignation 
    url(r'^hrms/employeeservices/employee/resignation/$', EmployeeExitEmployeeResignationLetterView.as_view(), name='employee_services_employee_resignation'),
    url(r'^hrms/employeeservices/employee/resignation/list/$', EmployeeExitEmployeeResignationLetterListView.as_view(), name='employee_services_employee_resignation_list'),
    url(r'^hrms/employeeservices/employee/relieving/list/$', EmployeeExitEmployeeEmployeeRelievingView.as_view(), name='employee_services_employee_relieving_list'),
    url(r'^hrms/employeeservices/employee/fullandfinalsettlement/list/$', EmployeeExitEmployeeFullandFinalSettlementListView.as_view(), name='employee_services_employee_fullandfinalsettlement_list'),
    url(r'^hrms/employeeservices/employee/resignation/status/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeExitEmployeeResignationLetterResignationStatusView.as_view(), name='employee_services_employee_resignation_status'),
    url(r'^hrms/employeeservices/employee/relieving/status/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeExitEmployeeResignationRelievingStatusView.as_view(), name='employee_services_employee_relieving_status'),
    url(r'^hrms/employeeservices/employee/fullandfinalsettlement/status/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeeExitEmployeeFullandFinalSettlementUpdateStatusView.as_view(), name='employee_services_employee_fullandfinalsettlement_status'),
    url(r'^website/employeeservices/employee/holidaysandleaves/days/list/$', WebsiteHolidaysListView.as_view(), name='website_list_holi_days_add'),
    url(r'^website/employeeservices/employee/holidaysandleaves/days/add/$', WebsiteAddUpdateHoliDaysView.as_view(), name='website_add_update_holi_days'),
    url(r'^website/employeeservices/employee/holidaysandleaves/days/list/(?P<holidaysdaysid>[0-9]+)/$', WebsiteAddUpdateHoliDaysView.as_view(), name='website_list_holi_days_update'),
    url(r'^website/employeeservices/employee/holidaysandleaves/days/delete/(?P<holidaysdaysid>[0-9]+)/$', WebsiteHolidaysDeletView.as_view(), name='website_holi_days_delete'),
    
    url(r'^website/employeeservices/employee/update/overttime/list/$', OvertimeManagementUpdateOvertimeListView.as_view(), name='website_edit_update_over_time_list'),
    
    
    url(r'^website/employeeservices/employee/update/overttime/add/$', OvertimeManagementUpdateOvertimeAddView.as_view(), name='website_edit_update_over_time_add'),
    url(r'^website/employeeservices/employee/update/overttime/status/list/$', OvertimeManagementUpdateOvertimeStatusListView.as_view(), name='website_edit_update_over_time_status_list'),
    url(r'^website/employeeservices/employee/update/overttime/delete/(?P<id>[0-9]+)/$', OvertimeManagementUpdateOvertimeDeletView.as_view(), name='website_edit_update_over_time_delete'),
    url(r'^website/employeeservices/employee/update/overttime/update/(?P<id>[0-9]+)/$', OvertimeManagementUpdateOvertimeStatusListViewUpdateStatusView.as_view(), name='website_edit_update_over_time_status_update'),
    url(r'^website/employeeservices/employee/travel/request/list/$', TravelClaimManagementTravelConveyanceTravelRequestListView.as_view(), name='website_travel_request_list'),
    # url(r'^website/employeeservices/employee/travel/request/status/list/$', TravelClaimManagementTravelConveyanceTravelRequestStatusView.as_view(), name='website_travel_request_status_list'),
##
    url(r'^website/employeeservices/employee/travel/request/status/Pending/list/$', TravelClaimManagementTravelConveyanceTravelRequestStatusView.as_view(), name='website_travel_request_status_list'),
    url(r'^website/employeeservices/employee/travel/request/status/Approved/list/$', TravelClaimManagementTravelConveyanceTravelRequestStatusApprovedView.as_view(), name='website_travel_request_status_Approved_list1'),
    url(r'^website/employeeservices/employee/travel/request/status/Rejected/list/$', TravelClaimManagementTravelConveyanceTravelRequestStatusRejectedView.as_view(), name='website_travel_request_status_Rejected_list1'),
    
    url(r'^website/employeeservices/employee/travel/request/add/$', TravelClaimManagementTravelConveyanceTravelRequestAddView.as_view(), name='website_travel_request_add'),
    url(r'^website/employeeservices/employee/travel/request/update/status/(?P<id>[0-9]+)/$', TravelClaimManagementTravelConveyanceTravelRequestUpdateStatusView.as_view(), name='website_travel_request_update_status'),
    url(r'^website/employeeservices/employee/submit/request/$', EmployeeAdvancesSubmitAdvanceRequestView.as_view(), name='website_travel_advance_request_submit_request'),
    url(r'^website/employeeservices/employee/advancerequest/status/request/list/$', EmployeeAdvancesSubmitAdvanceRequestListView.as_view(), name='website_travel_advance_request_status_list'),
    url(r'^website/employeeservices/employee/advancerequest/processing/request/list/$', EmployeeAdvancesSubmitAdvanceRequestProcessingListView.as_view(), name='website_travel_advance_request_processing_list'),
    url(r'^website/employeeservices/employee/advancerequest/processed/request/list/$', EmployeeAdvancesSubmitAdvanceRequestProcessedListView.as_view(), name='website_travel_advance_request_processed_list'),
    url(r'^website/employeeservices/employee/advancerequest/status/request/update/(?P<id>[0-9]+)/$', EmployeeAdvancesSubmitAdvanceRequestUpdateView.as_view(), name='website_travel_advance_request_status_update'),
    url(r'^website/employeeservices/employee/incentive/bonus/add/$', IncentiveBonusUpdateIncentiveBonusAddView.as_view(), name='website_travel_incentive_bonus_add'),
    url(r'^website/employeeservices/employee/incentive/bonus/status/list/$', IncentiveBonusUpdateIncentiveBonusIncentiveBonusApprovalListView.as_view(), name='website_travel_incentive_bonus_status_list'),
    url(r'^website/employeeservices/employee/incentive/bonus/status/update/(?P<id>[0-9]+)/$', IncentiveBonusUpdateIncentiveBonusIncentiveBonusApprovalUpdateView.as_view(), name='website_travel_incentive_bonus_status_update'),
    url(r'^website/employeeservices/employee/incentive/bonus/processing/list/$', IncentiveBonusUpdateIncentiveBonusIncentiveBonusProcessingListView.as_view(), name='website_incentive_bonus_status_processing_list'),
    url(r'^website/employeeservices/employee/incentive/bonus/processed/list/$', IncentiveBonusUpdateIncentiveBonusIncentiveBonusProcessedListView.as_view(), name='website_incentive_bonus_status_processed_list'),  
    # Knowledge and Training
    url(r'^hrms/knowledgeandtraining/update/documents/$', KnowledgeandTrainingUpdateDocumentsView.as_view(), name='crm_knowledgeandtraining_update_documents_view'),
    url(r'^hrms/knowledgeandtraining/update/training/$', KnowledgeandTrainingUpdateTrainingView.as_view(), name='crm_knowledgeandtraining_update_training_view'),
    url(r'^hrms/knowledgeandtraining/update/promotions/$', KnowledgeandTrainingUpdatePromotionsView.as_view(), name='crm_knowledgeandtraining_update_promotions_view'),
    url(r'^hrms/knowledgeandtraining/knowledge/sharing/$', KnowledgeandTrainingKnowledgeSharingView.as_view(), name='crm_knowledgeandtraining_update_knowledge_sharing'),
    url(r'^hrms/knowledgeandtraining/upcoming/traning/list/$', KnowledgeandTrainingUpcomingTraningListView.as_view(), name='crm_knowledgeandtraining_update_upcoming_training_list'),
    url(r'^hrms/knowledgeandtraining/current/promotions/list/$', KnowledgeandTrainingCurrentPromotionsListView.as_view(), name='crm_knowledgeandtraining_update_current_promotions_list'),
    
    url(r'^hrms/knowledgeandtraining/current/promotions/update/(?P<id>[0-9A-Za-z]+)/$', KnowledgeandTrainingCurrentPromotionsUpdateView.as_view(), name='crm_knowledgeandtraining_update_current_promotions_update'),
    url(r'^hrms/knowledgeandtraining/upcoming/promotions/list/$', KnowledgeandTrainingUpcomingPromotionsListView.as_view(), name='crm_knowledgeandtraining_update_current_upcoming_list'),
    url(r'^hrms/knowledgeandtraining/past/promotions/list/$', KnowledgeandTrainingPastPromotionsListView.as_view(), name='crm_knowledgeandtraining_update_current_past_list'),
    url(r'^hrms/knowledgeandtraining/current/traning/list/$', KnowledgeandTrainingCurrentTraningListView.as_view(), name='crm_knowledgeandtraining_update_current_traning_list'),
    url(r'^hrms/knowledgeandtraining/past/traning/list/$', KnowledgeandTrainingPastraningListView.as_view(), name='crm_knowledgeandtraining_update_current_past_traning_list'),
    url(r'^hrms/knowledgeandtraining/request/received/traning/list/$', KnowledgeandTrainingRequestReceivedForTrainignListView.as_view(), name='crm_knowledgeandtraining_request_recevied_for_training'),
    url(r'^hrms/vendorsupport/send/wish/to/attend/$', send_request_to_for_attend_traning.as_view(), name='crm_vendorsupport_send_wish_to_attend'),
    url(r'^traning/attend/$', TrainingAttendListView.as_view(), name='traning_attend'),


###### EmployeeHolidaysAndLeaves
    url(r'^website/employee/services/employee/holidaysandleaves/days/list/$', EmployeeHolidaysAndLeavesList.as_view(), name='EmployeeHolidaysAndLeaveslist'),
    url(r'^website/employee/services/employee/holidaysandleaves/days/add/$', AddEmployeeHolidaysAndLeaves.as_view(), name='EmployeeHolidaysAndLeavesadd'),
    url(r'^website/employee/services/employee/holidaysandleaves/days/edit/(?P<id>[0-9]+)/$', AddEditEmployeeHolidaysAndLeaves, name='EmployeeHolidaysAndLeavesedit'),
    url(r'^website/employee/services/employee/holidaysandleaves/days/delete/(?P<id>[0-9]+)/$', EmployeeHolidaysAndLeavesDelete.as_view(), name='EmployeeHolidaysAndLeavesdelete'),  



###
    url(r'^hrms/employeeservices/recruitement/publishvacancies/add/$', Datapost.as_view(), name='crm_website_employeeservices_recruitement_publishvacancies_update'),
    url(r'^hrms/employeeservices/recruitement/publishvacancies1/add/$', Datapost1.as_view(), name='crm_website_employeeservices_recruitement_publishvacancies_update'),
    
   ### payrollprocessed    EmployeePayrollProcessedListView
    url(r'^hrms-employee/emplyeesservices/payroll/payroll-processed/add/$', EmployeePayrollProcessedAddView, name='crm_crmemployee_manageemployee_payrollprocessed_add'),
    url(r'^hrms-employee/emplyeesservices/payroll/payroll-processed/list/$', EmployeePayrollProcessedListView.as_view(), name='crm_crmemployee_manageemployee_payrollprocessed_list'),
    url(r'^hrms-employee/emplyeesservices/payroll/payroll-processed/pending/list/$', EmployeePayrollProcessedPendingListView.as_view(), name='crm_crmemployee_manageemployee_payrollprocessed_pending_list'),
    url(r'^hrms-employee/emplyeesservices/payroll/payroll-processed/update/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeePayrollProcessedListViewUpdate, name='crm_crmemployee_manageemployee_payrollprocessed_update'),
    url(r'^website/employee/services/employee/payroll-processed/days/delete/(?P<id>[0-9]+)/$', EmployeePayrollProcessedListViewDelete.as_view(), name='EmployeePayrollProcessedListViewdelete'),  
    url(r'^website/employee/services/employee/payroll-processed/list/$', EmployeePayrollstatusListView.as_view(), name='EmployeePayrollstatusListViews'),  
    
    url(r'^website/employee/services/employee/payroll-processing/list/$', EmployeePayrollProcessingListView.as_view(), name='EmployeePayrollProcessingListViews'),  

    url(r'^hrms-employee/emplyeesservices/payroll/payroll-processed/add/$', EmployeesalarySlipAddView, name='EmployeesalarySlipAddView_add'),
    url(r'^website/employee/services/employee/payroll-processed/salary/slip/list/(?P<id>[0-9,a-z,A-Z]+)/$', EmployeePayrollSlipListView.as_view(), name='EmployeePayrollSlipListView'),  

]
# 