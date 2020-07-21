from hrms_employees.views import *
from django.conf.urls import include
from django.conf.urls import url


urlpatterns = [
    url(r'^hrms-employee/emplyeesservices/manageemployee/reportingstructure/list/$', DefineReportingStructureList.as_view(), name='crm_crmemployee_manageemployee_reportingstructure_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/reportingstructure/add/$', AddEditDefineReportingStructure.as_view(), name='crm_crmemployee_manageemployee_reportingstructure_add'),
    url(r'^hrms-employee/emplyeesservices/semanageemployeetup/reportingstructure/edit/(?P<id>[0-9]+)/$',AddEditDefineReportingStructure.as_view(), name="crm_crmemployee_manageemployee_reportingstructure_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/reportingstructure/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineReportingStructureDelete.as_view(), name='crm_crmemployee_manageemployee_reportingstructure_delete'),

    url(r'^hrms-employee/emplyeesservices/manageemployee/employeeid/list/$',DefineEmployeeIDList.as_view(), name='crm_crmemployee_manageemployee_employeeid_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/employeeid/add/$',AddEditDefineEmployeeID.as_view(), name='crm_crmemployee_manageemployee_employeeid_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/employeeid/edit/(?P<id>[0-9]+)/$',AddEditDefineEmployeeID.as_view(), name="crm_crmemployee_manageemployee_employeeid_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/employeeid/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineEmployeeIDDelete.as_view(), name='crm_crmemployee_manageemployee_employeeid_delete'),

    url(r'^hrms-employee/emplyeesservices/manageemployee/managegrade/list/$',ManageGradeList.as_view(), name='crm_crmemployee_manageemployee_managegrade_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/managegrade/add/$',AddEditManageGrade.as_view(), name='crm_crmemployee_manageemployee_managegrade_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/managegrade/edit/(?P<id>[0-9]+)/$',AddEditManageGrade.as_view(), name="crm_crmemployee_manageemployee_managegrade_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/managegrade/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageGradeDelete.as_view(), name='crm_crmemployee_manageemployee_managegrade_delete'),

    url(r'^hrms-employee/emplyeesservices/manageemployee/managesalaryrange/list/$',ManageSalaryRangeList.as_view(), name='crm_crmemployee_manageemployee_managesalaryrange_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/managesalaryrange/add/$',AddEditManageSalaryRange.as_view(), name='crm_crmemployee_manageemployee_managesalaryrange_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/managesalaryrange/edit/(?P<id>[0-9]+)/$',AddEditManageSalaryRange.as_view(), name="crm_crmemployee_manageemployee_managesalaryrange_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/managesalaryrange/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageSalaryRangeDelete.as_view(), name='crm_crmemployee_managesalaryrange_managegrade_delete'),

    url(r'^hrms-employee/emplyeesservices/manageemployee/definesalary/list/$',DefineSalaryList.as_view(), name='crm_crmemployee_manageemployee_definesalary_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/definesalary/add/$',AddEditDefineSalary.as_view(), name='crm_crmemployee_manageemployee_definesalary_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/definesalary/edit/(?P<id>[0-9]+)/$',AddEditDefineSalary.as_view(), name="crm_crmemployee_manageemployee_definesalary_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/definesalary/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineSalaryDelete.as_view(), name='crm_crmemployee_managesalaryrange_definesalary_delete'),

    url(r'^hrms-employee/emplyeesservices/manageemployee/definedeductions/list/$',DefineDeductionsStuctureList.as_view(), name='crm_crmemployee_manageemployee_define_deductions_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/definedeductions/add/$',AddEditDefineDeductionsStucture.as_view(), name='crm_crmemployee_manageemployee_define_deductions_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/definedeductions/edit/(?P<id>[0-9]+)/$',AddEditDefineDeductionsStucture.as_view(), name="crm_crmemployee_manageemployee_define_deductions_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/definedeductions/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineDeductionsStuctureDelete.as_view(), name='crm_crmemployee_managesalaryrange_define_deductions_delete'),

    url(r'^hrms-employee/emplyeesservices/manageemployee/otherincome/list/$',DefineOtherIncomeList.as_view(), name='crm_crmemployee_manageemployee_otherincome_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/otherincome/add/$',AddEditDefineOtherIncome.as_view(), name='crm_crmemployee_manageemployee_otherincome_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/otherincome/edit/(?P<id>[0-9]+)/$',AddEditDefineOtherIncome.as_view(), name="crm_crmemployee_manageemployee_otherincome_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/otherincome/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineOtherIncomeDelete.as_view(), name='crm_crmemployee_managesalaryrange_otherincome_delete'),

    url(r'^hrms-employee/emplyeesservices/manageemployee/language/list/$',ManageLanguageList.as_view(), name='crm_crmemployee_manageemployee_language_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/language/add/$',AddEditManageLanguage.as_view(), name='crm_crmemployee_manageemployee_language_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/language/edit/(?P<id>[0-9]+)/$',AddEditManageLanguage.as_view(), name="crm_crmemployee_manageemployee_language_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/language/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageLanguageDelete.as_view(), name='crm_crmemployee_managesalaryrange_language_delete'),

    url(r'^hrms-employee/emplyeesservices/manageemployee/qualification/list/$',ManageQualificationList.as_view(), name='crm_crmemployee_manageemployee_qualification_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/qualification/add/$',AddEditManageQualification.as_view(), name='crm_crmemployee_manageemployee_qualification_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/qualification/edit/(?P<id>[0-9]+)/$',AddEditManageQualification.as_view(), name="crm_crmemployee_manageemployee_qualification_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/qualification/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageQualificationDelete.as_view(), name='crm_crmemployee_managesalaryrange_qualification_delete'),

    url(r'^hrms-employee/emplyeesservices/manageemployee/expereince/list/$',ManageExpereinceList.as_view(), name='crm_crmemployee_manageemployee_expereince_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/expereince/add/$',AddEditManageExpereince.as_view(), name='crm_crmemployee_manageemployee_expereince_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/expereince/edit/(?P<id>[0-9]+)/$',AddEditManageExpereince.as_view(), name="crm_crmemployee_manageemployee_expereince_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/expereince/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageExpereinceDelete.as_view(), name='crm_crmemployee_managesalaryrange_expereince_delete'),

    url(r'^hrms-employee/emplyeesservices/manageemployee/family/list/$',ManageFamilyList.as_view(), name='crm_crmemployee_manageemployee_family_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/family/add/$',AddEditManageFamily.as_view(), name='crm_crmemployee_manageemployee_family_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/family/edit/(?P<id>[0-9]+)/$',AddEditManageFamily.as_view(), name="crm_crmemployee_manageemployee_family_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/family/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageFamilyDelete.as_view(), name='crm_crmemployee_managesalaryrange_family_delete'),

    # Manage  PayRoll 
    url(r'^hrms-employee/emplyeesservices/managepayroll/taxstructure/list/$',DefineTaxStructureList.as_view(), name='crm_crmemployee_manageemployee_taxstructure_list'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/taxstructure/add/$',AddEditDefineTaxStructure.as_view(), name='crm_crmemployee_manageemployee_taxstructure_add'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/taxstructure/edit/(?P<id>[0-9]+)/$',AddEditDefineTaxStructure.as_view(), name="crm_crmemployee_manageemployee_taxstructure_edit"),
    url(r'^hrms-employee/emplyeesservices/managepayroll/taxstructure/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineTaxStructureDelete.as_view(), name='crm_crmemployee_managesalaryrange_taxstructure_delete'),

    url(r'^hrms-employee/emplyeesservices/managepayroll/reimbursement/list/$',DefineReimbursementList.as_view(), name='crm_crmemployee_manageemployee_reimbursement_list'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/reimbursement/add/$',AddEditDefineReimbursement.as_view(), name='crm_crmemployee_manageemployee_reimbursement_add'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/reimbursement/edit/(?P<id>[0-9]+)/$',AddEditDefineReimbursement.as_view(), name="crm_crmemployee_manageemployee_reimbursement_edit"),
    url(r'^hrms-employee/emplyeesservices/managepayroll/reimbursement/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineReimbursementDelete.as_view(), name='crm_crmemployee_managesalaryrange_reimbursement_delete'),

    url(r'^hrms-employee/emplyeesservices/managepayroll/exemptedincome/list/$',DefineExemptedIncomeList.as_view(), name='crm_crmemployee_manageemployee_exemptedincome_list'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/exemptedincome/add/$',AddEditDefineExemptedIncome.as_view(), name='crm_crmemployee_manageemployee_exemptedincome_add'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/exemptedincome/edit/(?P<id>[0-9]+)/$',AddEditDefineExemptedIncome.as_view(), name="crm_crmemployee_manageemployee_exemptedincome_edit"),
    url(r'^hrms-employee/emplyeesservices/managepayroll/exemptedincome/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineExemptedIncomeDelete.as_view(), name='crm_crmemployee_managesalaryrange_exemptedincome_delete'),

    url(r'^hrms-employee/emplyeesservices/managepayroll/statutorydeductions/list/$',DefineStatutoryDeductionsList.as_view(), name='crm_crmemployee_manageemployee_statutorydeductions_list'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/statutorydeductions/add/$',AddEditDefineStatutoryDeductions.as_view(), name='crm_crmemployee_manageemployee_statutorydeductions_add'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/statutorydeductions/edit/(?P<id>[0-9]+)/$',AddEditDefineStatutoryDeductions.as_view(), name="crm_crmemployee_manageemployee_statutorydeductions_edit"),
    url(r'^hrms-employee/emplyeesservices/managepayroll/statutorydeductions/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineStatutoryDeductionsDelete.as_view(), name='crm_crmemployee_managesalaryrange_statutorydeductions_delete'),

    url(r'^hrms-employee/emplyeesservices/managepayroll/advances/list/$',DefineAdvancesList.as_view(), name='crm_crmemployee_manageemployee_advances_list'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/advances/add/$',AddEditDefineAdvances.as_view(), name='crm_crmemployee_manageemployee_advances_add'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/advances/edit/(?P<id>[0-9]+)/$',AddEditDefineAdvances.as_view(), name="crm_crmemployee_manageemployee_advances_edit"),
    url(r'^hrms-employee/emplyeesservices/managepayroll/advances/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineAdvancesDelete.as_view(), name='crm_crmemployee_managesalaryrange_advances_delete'),

    url(r'^hrms-employee/emplyeesservices/managepayroll/deductions/list/$',DefineDeductionsList.as_view(), name='crm_crmemployee_manageemployee_deductions_list'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/deductions/add/$',AddEditDefineDeductions.as_view(), name='crm_crmemployee_manageemployee_deductions_add'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/deductions/edit/(?P<id>[0-9]+)/$',AddEditDefineDeductions.as_view(), name="crm_crmemployee_manageemployee_deductions_edit"),
    url(r'^hrms-employee/emplyeesservices/managepayroll/deductions/delete/(?P<id>[0-9,a-z,A-Z]+)/$',DefineDeductionsDelete.as_view(), name='crm_crmemployee_managesalaryrange_deductions_delete'),

    # Holidays and Leaves
    url(r'^hrms-employee/emplyeesservices/holidaysandleaves/defineleavetype/list/$',HolidaysandLeavesDefineLeaveTypeList.as_view(), name='crm_crmemployee_holidaysandleaves_defineleavetype_list'),
    url(r'^hrms-employee/emplyeesservices/holidaysandleaves/holidays/list/$', LeaveHolidaysManagementHolidaysListView.as_view(), name='crm_crmemployee_holidaysandleaves_holidays_list'),
    url(r'^hrms-employee/emplyeesservices/holidaysandleaves/defineleavetype/add/$',AddEditHolidaysandLeavesDefineLeaveTypeList.as_view(), name='crm_crmemployee_holidaysandleaves_defineleavetype_add'),
    url(r'^hrms-employee/emplyeesservices/holidaysandleaves/defineleavetype/edit/(?P<id>[0-9]+)/$',AddEditHolidaysandLeavesDefineLeaveTypeList.as_view(), name="crm_crmemployee_holidaysandleaves_defineleavetype_edit"),
    url(r'^hrms-employee/emplyeesservices/holidaysandleaves/defineleavetype/delete/(?P<id>[0-9,a-z,A-Z]+)/$',HolidaysandLeavesDefineLeaveTypeDelete.as_view(), name='crm_crmemployee_holidaysandleaves_defineleavetype_delete'),
    
    url(r'^hrms-employee/emplyeesservices/holidaysandleaves/manageleaveqouta/list/$',HolidaysandLeavesManageLeaveQoutaList.as_view(), name='crm_crmemployee_holidaysandleaves_manageleaveqouta_list'),
    url(r'^hrms-employee/emplyeesservices/holidaysandleaves/manageleaveqouta/add/$',AddEditHolidaysandLeavesManageLeaveQoutaList.as_view(), name='crm_crmemployee_holidaysandleaves_manageleaveqouta_add'),
    url(r'^hrms-employee/emplyeesservices/holidaysandleaves/manageleaveqouta/edit/(?P<id>[0-9]+)/$',AddEditHolidaysandLeavesManageLeaveQoutaList.as_view(), name="crm_crmemployee_holidaysandleaves_manageleaveqouta_edit"),
    url(r'^hrms-employee/emplyeesservices/holidaysandleaves/manageleaveqouta/delete/(?P<id>[0-9,a-z,A-Z]+)/$',HolidaysandLeavesManageLeaveQoutaDelete.as_view(), name='crm_crmemployee_holidaysandleaves_manageleaveqouta_delete'),
    url(r'^hrms-employee/emplyeesservices/attendanceovertimemanagement/overtime/list/$', AttendanceOvertimeManagementOvertimeListView.as_view(), name='crm_crmemployee_attendanceovertimemanagement_overtime_list'),



    # Manage Claims
    url(r'^hrms-employee/emplyeesservices/manageclaims/claimtype/list/$',ManageClaimsDefineClaimTypeList.as_view(), name='crm_crmemployee_manageclaims_claimtype_list'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/claimtype/add/$',AddEditCrmManageClaimsDefineClaimType.as_view(), name='crm_crmemployee_manageclaims_claimtype_add'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/claimtype/edit/(?P<id>[0-9]+)/$',AddEditCrmManageClaimsDefineClaimType.as_view(), name="crm_crmemployee_manageclaims_claimtype_edit"),
    url(r'^hrms-employee/emplyeesservices/manageclaims/claimtype/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageClaimsDefineClaimTypeDelete.as_view(), name='crm_crmemployee_manageclaims_claimtype_delete'),
    
    url(r'^hrms-employee/emplyeesservices/manageclaims/claimentitlement/list/$',ManageClaimsClaimEntitlementList.as_view(), name='crm_crmemployee_manageclaims_claimentitlement_list'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/claimentitlement/add/$',AddEditCrmManageClaimsClaimEntitlement.as_view(), name='crm_crmemployee_manageclaims_claimentitlement_add'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/claimentitlement/edit/(?P<id>[0-9]+)/$',AddEditCrmManageClaimsClaimEntitlement.as_view(), name="crm_crmemployee_manageclaims_claimentitlement_edit"),
    url(r'^hrms-employee/emplyeesservices/manageclaims/claimentitlement/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageClaimsClaimEntitlementDelete.as_view(), name='crm_crmemployee_manageclaims_claimentitlement_delete'),


    url(r'^hrms-employee/emplyeesservices/manageclaims/modeoftravel/list/$', TravelandClaimTravelManagementDefineModeofTravelList.as_view(), name='crm_crmemployee_manageclaims_modeoftravel_list'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/modeoftravel/add/$', AddEditTravelandClaimTravelManagementDefineModeofTravel.as_view(), name='crm_crmemployee_manageclaims_modeoftravel_add'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/modeoftravel/edit/(?P<id>[0-9]+)/$', AddEditTravelandClaimTravelManagementDefineModeofTravel.as_view(), name="crm_crmemployee_manageclaims_modeoftravel_edit"),
    url(r'^hrms-employee/emplyeesservices/manageclaims/modeoftravel/delete/(?P<id>[0-9,a-z,A-Z]+)/$', TravelandClaimTravelManagementDefineModeofTravelDelete.as_view(), name='crm_crmemployee_manageclaims_modeoftravel_delete'),


    url(r'^hrms-employee/emplyeesservices/manageclaims/traveltype/list/$', TravelandClaimTravelManagementDefineTravelTypeList.as_view(), name='crm_crmemployee_manageclaims_traveltype_list'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/traveltype/add/$', AddEditTravelandClaimTravelManagementDefineTravelType.as_view(), name='crm_crmemployee_manageclaims_traveltype_add'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/traveltype/edit/(?P<id>[0-9]+)/$', AddEditTravelandClaimTravelManagementDefineTravelType.as_view(), name="crm_crmemployee_manageclaims_traveltype_edit"),
    url(r'^hrms-employee/emplyeesservices/manageclaims/traveltype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', TravelandClaimTravelManagementDefineTravelTypeDelete.as_view(), name='crm_crmemployee_manageclaims_traveltype_delete'),


    url(r'^hrms-employee/emplyeesservices/manageclaims/travelpolicy/list/$', TravelandClaimTravelManagementDefineTravelPolicyList.as_view(), name='crm_crmemployee_manageclaims_travelpolicy_list'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/travelpolicy/add/$', AddEditTravelandClaimTravelManagementDefineTravelPolicy.as_view(), name='crm_crmemployee_manageclaims_travelpolicy_add'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/travelpolicy/edit/(?P<id>[0-9]+)/$', AddEditTravelandClaimTravelManagementDefineTravelPolicy.as_view(), name="crm_crmemployee_manageclaims_travelpolicy_edit"),
    url(r'^hrms-employee/emplyeesservices/manageclaims/travelpolicy/delete/(?P<id>[0-9,a-z,A-Z]+)/$', TravelandClaimTravelManagementDefineTravelPolicyDelete.as_view(), name='crm_crmemployee_manageclaims_travelpolicy_delete'),
        

    url(r'^hrms-employee/emplyeesservices/manageclaims/managetravel/list/$', TravelandClaimTravelManagementManageTravelList.as_view(), name='crm_crmemployee_manageclaims_managetravel_list'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/managetravel/add/$', AddEditTravelandClaimTravelManagementManageTravel.as_view(), name='crm_crmemployee_manageclaims_managetravel_add'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/managetravel/edit/(?P<id>[0-9]+)/$', AddEditTravelandClaimTravelManagementManageTravel.as_view(), name="crm_crmemployee_manageclaims_managetravel_edit"),
    url(r'^hrms-employee/emplyeesservices/manageclaims/managetravel/delete/(?P<id>[0-9,a-z,A-Z]+)/$', TravelandClaimTravelManagementManageTravelDelete.as_view(), name='crm_crmemployee_manageclaims_managetravel_delete'),
    
    # Manage Reimbursement 
    url(r'^hrms-employee/emplyeesservices/manageclaims/reimbursementtype/list/$',ManageReimbursementDefineReimbursementList.as_view(), name='crm_crmemployee_managereimbursement_reimbursementtype_list'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/reimbursementtype/add/$',AddEditCrmManageReimbursementDefineReimbursement.as_view(), name='crm_crmemployee_managereimbursement_reimbursementtype_add'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/reimbursementtype/edit/(?P<id>[0-9]+)/$',AddEditCrmManageReimbursementDefineReimbursement.as_view(), name="crm_crmemployee_managereimbursement_reimbursementtype_edit"),
    url(r'^hrms-employee/emplyeesservices/manageclaims/reimbursementtype/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageReimbursementDefineReimbursementDelete.as_view(), name='crm_crmemployee_managereimbursement_reimbursementtype_delete'),
    
    url(r'^hrms-employee/emplyeesservices/manageclaims/reimbursementclaimentitlement/list/$',ManageReimbursementReimbursementEntitilementList.as_view(), name='crm_crmemployee_managereimbursement_claimentitlement_list'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/reimbursementclaimentitlement/add/$',AddEditCrmManageReimbursementReimbursementEntitilement.as_view(), name='crm_crmemployee_managereimbursement_claimentitlement_add'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/reimbursementclaimentitlement/edit/(?P<id>[0-9]+)/$',AddEditCrmManageReimbursementReimbursementEntitilement.as_view(), name="crm_crmemployee_managereimbursement_claimentitlement_edit"),
    url(r'^hrms-employee/emplyeesservices/manageclaims/reimbursementclaimentitlement/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageReimbursementReimbursementEntitilementDelete.as_view(), name='crm_crmemployee_managereimbursement_claimentitlement_delete'),

    # Recruitement Policies
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/employeestrength/list/$',RecruitementPoliciesDefineEmployeeStrengthList.as_view(), name='crm_crmemployee_recruitementpolicies_employeestrength_list'),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/employeestrength/add/$',AddEditCrmRecruitementPoliciesDefineEmployeeStrength.as_view(), name='crm_crmemployee_recruitementpolicies_employeestrength_add'),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/employeestrength/edit/(?P<id>[0-9]+)/$',AddEditCrmRecruitementPoliciesDefineEmployeeStrength.as_view(), name="crm_crmemployee_recruitementpolicies_employeestrength_edit"),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/employeestrength/delete/(?P<id>[0-9,a-z,A-Z]+)/$',RecruitementPoliciesDefineEmployeeStrengthDelete.as_view(), name='crm_crmemployee_recruitementpolicies_employeestrength_delete'),


    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/qualification/list/$',RecruitementPoliciesDefineQualificationModelList.as_view(), name='crm_crmemployee_recruitementpolicies_qualification_list'),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/qualification/add/$',AddEditCrmRecruitementPoliciesDefineQualificationModel.as_view(), name='crm_crmemployee_recruitementpolicies_qualification_add'),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/qualification/edit/(?P<id>[0-9]+)/$',AddEditCrmRecruitementPoliciesDefineQualificationModel.as_view(), name="crm_crmemployee_recruitementpolicies_qualification_edit"),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/qualification/delete/(?P<id>[0-9,a-z,A-Z]+)/$',RecruitementPoliciesDefineQualificationModelDelete.as_view(), name='crm_crmemployee_recruitementpolicies_qualification_delete'),


    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/experience/list/$',RecruitementPoliciesDefineExperienceModelList.as_view(), name='crm_crmemployee_recruitementpolicies_experience_list'),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/experience/add/$',AddEditCrmRecruitementPoliciesDefineExperienceModel.as_view(), name='crm_crmemployee_recruitementpolicies_experience_add'),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/experienceexperience/edit/(?P<id>[0-9]+)/$',AddEditCrmRecruitementPoliciesDefineExperienceModel.as_view(), name="crm_crmemployee_recruitementpolicies_experience_edit"),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/experience/delete/(?P<id>[0-9,a-z,A-Z]+)/$',RecruitementPoliciesDefineExperienceModelDelete.as_view(), name='crm_crmemployee_recruitementpolicies_experience_delete'),


    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/recruitmentrules/list/$',RecruitementPoliciesManageRecruitmentRulesModelList.as_view(), name='crm_crmemployee_recruitementpolicies_recruitmentrules_list'),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/recruitmentrules/add/$',AddEditCrmRecruitementPoliciesManageRecruitmentRulesModel.as_view(), name='crm_crmemployee_recruitementpolicies_recruitmentrules_add'),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/recruitmentrules/edit/(?P<id>[0-9]+)/$',AddEditCrmRecruitementPoliciesManageRecruitmentRulesModel.as_view(), name="crm_crmemployee_recruitementpolicies_recruitmentrules_edit"),
    url(r'^hrms-employee/emplyeesservices/recruitementpolicies/recruitmentrules/delete/(?P<id>[0-9,a-z,A-Z]+)/$',RecruitementPoliciesManageRecruitmentRulesModelDelete.as_view(), name='crm_crmemployee_recruitementpolicies_recruitmentrules_delete'),


    url(r'^hrms-employee/emplyeesservices/hrpolicies/policytype/list/$',HRPoliciesDefinePolicyTypeModelList.as_view(), name='crm_crmemployee_hrpolicies_policytype_list'),
    url(r'^hrms-employee/emplyeesservices/hrpolicies/policytype/add/$',AddEditCrmHRPoliciesDefinePolicyTypeModel.as_view(), name='crm_crmemployee_hrpolicies_policytype_add'),
    url(r'^hrms-employee/emplyeesservices/hrpolicies/policytype/edit/(?P<id>[0-9]+)/$',AddEditCrmHRPoliciesDefinePolicyTypeModel.as_view(), name="crm_crmemployee_hrpolicies_policytype_edit"),
    url(r'^hrms-employee/emplyeesservices/hrpolicies/policytype/delete/(?P<id>[0-9,a-z,A-Z]+)/$',HRPoliciesDefinePolicyTypeModelDelete.as_view(), name='crm_crmemployee_hrpolicies_recruitmentrules_delete'),


    url(r'^hrms-employee/emplyeesservices/hrpolicies/form/list/$', PoliciesandFormsManagementHRPoliciesFormList.as_view(), name='crm_crm_employee_hrpolicies_form_list'),
    url(r'^hrms-employee/emplyeesservices/hrpolicies/form/add/$', AddEditPoliciesandFormsManagementHRPoliciesForm.as_view(), name='crm_crm_employee_hrpolicies_form_add'),
    url(r'^hrms-employee/emplyeesservices/hrpolicies/form/edit/(?P<id>[0-9]+)/$', AddEditPoliciesandFormsManagementHRPoliciesForm.as_view(), name="crm_crm_employee_hrpolicies_form_edit"),
    url(r'^hrms-employee/emplyeesservices/hrpolicies/form/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PoliciesandFormsManagementHRPoliciesFormDelete.as_view(), name='crm_crm_employee_hrpolicies_form_delete'),
    # Recruitment Management

    url(r'^hrms-employee/recruitmentmanagement/employeestrength/list/$', RecruitmentManagementRecruitmentPlanningDefineEmployeeStrengthList.as_view(), name='crm_crmemployee_recruitmentmanagement_employeestrength_list'),
    url(r'^hrms-employee/recruitmentmanagement/employeestrength/add/$',AddEditRecruitmentManagementRecruitmentPlanningDefineEmployeeStrength.as_view(), name='crm_crmemployee_recruitmentmanagement_employeestrength_add'),
    url(r'^hrms-employee/recruitmentmanagement/employeestrength/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementRecruitmentPlanningDefineEmployeeStrength.as_view(), name="crm_crmemployee_recruitmentmanagement_employeestrength_edit"),
    url(r'^hrms-employee/recruitmentmanagement/employeestrength/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementRecruitmentPlanningDefineEmployeeStrengthDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_employeestrength_delete'),

    url(r'^hrms-employee/recruitmentmanagement/qualification/list/$', RecruitmentManagementRecruitmentPlanningDefineQualificationList.as_view(), name='crm_crmemployee_recruitmentmanagement_qualification_list'),
    url(r'^hrms-employee/recruitmentmanagement/qualification/add/$',AddEditRecruitmentManagementRecruitmentPlanningDefineQualification.as_view(), name='crm_crmemployee_recruitmentmanagement_qualification_add'),
    url(r'^hrms-employee/recruitmentmanagement/qualification/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementRecruitmentPlanningDefineQualification.as_view(), name="crm_crmemployee_recruitmentmanagement_qualification_edit"),
    url(r'^hrms-employee/recruitmentmanagement/qualification/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementRecruitmentPlanningDefineQualificationDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_qualification_delete'),

    url(r'^hrms-employee/recruitmentmanagement/experience/list/$', RecruitmentManagementRecruitmentPlanningDefineExperienceList.as_view(), name='crm_crmemployee_recruitmentmanagement_experience_list'),
    url(r'^hrms-employee/recruitmentmanagement/experience/add/$',AddEditRecruitmentManagementRecruitmentPlanningDefineExperience.as_view(), name='crm_crmemployee_recruitmentmanagement_experience_add'),
    url(r'^hrms-employee/recruitmentmanagement/experience/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementRecruitmentPlanningDefineExperience.as_view(), name="crm_crmemployee_recruitmentmanagement_experience_edit"),
    url(r'^hrms-employee/recruitmentmanagement/experience/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementRecruitmentPlanningDefineExperienceDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_experience_delete'),

    url(r'^hrms-employee/recruitmentmanagement/recruitmentrules/list/$', RecruitmentManagementRecruitmentPlanningManageRecruitmentRulesList.as_view(), name='crm_crmemployee_recruitmentmanagement_recruitmentrules_list'),
    url(r'^hrms-employee/recruitmentmanagement/recruitmentrules/add/$',AddEditRecruitmentManagementRecruitmentPlanningManageRecruitmentRules.as_view(), name='crm_crmemployee_recruitmentmanagement_recruitmentrules_add'),
    url(r'^hrms-employee/recruitmentmanagement/recruitmentrules/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementRecruitmentPlanningManageRecruitmentRules.as_view(), name="crm_crmemployee_recruitmentmanagement_recruitmentrules_edit"),
    url(r'^hrms-employee/recruitmentmanagement/recruitmentrules/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementRecruitmentPlanningManageRecruitmentRulesDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_recruitmentrules_delete'),

    url(r'^hrms-employee/recruitmentmanagement/candidatesourcing/list/$', RecruitmentManagementCandidateSourcingManageJobPublishmentList.as_view(), name='crm_crmemployee_recruitmentmanagement_candidatesourcing_list'),
    url(r'^hrms-employee/recruitmentmanagement/candidatesourcing/add/$',AddEditRecruitmentManagementCandidateSourcingManageJobPublishment.as_view(), name='crm_crmemployee_recruitmentmanagement_candidatesourcing_add'),
    url(r'^hrms-employee/recruitmentmanagement/candidatesourcing/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementCandidateSourcingManageJobPublishment.as_view(), name="crm_crmemployee_recruitmentmanagement_candidatesourcing_edit"),
    url(r'^hrms-employee/recruitmentmanagement/candidatesourcing/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementCandidateSourcingManageJobPublishmentDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_candidatesourcing_delete'),

    url(r'^hrms-employee/recruitmentmanagement/managereceiptofresume/list/$', RecruitmentManagementCandidateSourcingManageReceiptofResumeList.as_view(), name='crm_crmemployee_recruitmentmanagement_managereceiptofresume_list'),
    url(r'^hrms-employee/recruitmentmanagement/managereceiptofresume/add/$',AddEditRecruitmentManagementCandidateSourcingManageReceiptofResume.as_view(), name='crm_crmemployee_recruitmentmanagement_managereceiptofresume_add'),
    url(r'^hrms-employee/recruitmentmanagement/managereceiptofresume/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementCandidateSourcingManageReceiptofResume.as_view(), name="crm_crmemployee_recruitmentmanagement_managereceiptofresume_edit"),
    url(r'^hrms-employee/recruitmentmanagement/managereceiptofresume/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementCandidateSourcingManageReceiptofResumeDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_managereceiptofresume_delete'),

    url(r'^hrms-employee/recruitmentmanagement/screenlevel/list/$', RecruitmentManagementInterveiwProcessDefineScreeningLevelList.as_view(), name='crm_crmemployee_recruitmentmanagement_interveiwprocess_list'),
    url(r'^hrms-employee/recruitmentmanagement/screenlevel/add/$',AddEditRecruitmentManagementInterveiwProcessDefineScreeningLevel.as_view(), name='crm_crmemployee_recruitmentmanagement_interveiwprocess_add'),
    url(r'^hrms-employee/recruitmentmanagement/screenlevel/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementInterveiwProcessDefineScreeningLevel.as_view(), name="crm_crmemployee_recruitmentmanagement_interveiwprocess_edit"),
    url(r'^hrms-employee/recruitmentmanagement/screenlevel/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementInterveiwProcessDefineScreeningLevelDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_interveiwprocess_delete'),


    url(r'^hrms-employee/recruitmentmanagement/manageinterviewprocess/list/$', RecruitmentManagementInterveiwProcessManageInterviewProcessList.as_view(), name='crm_crmemployee_recruitmentmanagement_manageinterviewprocess_list'),
    url(r'^hrms-employee/recruitmentmanagement/manageinterviewprocess/add/$',AddEditRecruitmentManagementInterveiwProcessManageInterviewProcess.as_view(), name='crm_crmemployee_recruitmentmanagement_manageinterviewprocess_add'),
    url(r'^hrms-employee/recruitmentmanagement/manageinterviewprocess/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementInterveiwProcessManageInterviewProcess.as_view(), name="crm_crmemployee_recruitmentmanagement_manageinterviewprocess_edit"),
    url(r'^hrms-employee/recruitmentmanagement/manageinterviewprocess/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementInterveiwProcessManageInterviewProcessDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_manageinterviewprocess_delete'),

    url(r'^hrms-employee/recruitmentmanagement/scorecard/list/$', RecruitmentManagementInterveiwProcessDefineScorecardList.as_view(), name='crm_crmemployee_recruitmentmanagement_scorecard_list'),
    url(r'^hrms-employee/recruitmentmanagement/scorecard/add/$',AddEditRecruitmentManagementInterveiwProcessDefineScorecard.as_view(), name='crm_crmemployee_recruitmentmanagement_scorecard_add'),
    url(r'^hrms-employee/recruitmentmanagement/scorecard/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementInterveiwProcessDefineScorecard.as_view(), name="crm_crmemployee_recruitmentmanagement_scorecard_edit"),
    url(r'^hrms-employee/recruitmentmanagement/scorecard/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementInterveiwProcessDefineScorecardDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_scorecard_delete'),
#Manage approvingauthority
    url(r'^hrms-employee/recruitmentmanagement/approvingauthority/list/$', RecruitmentManagementInterveiwManageCandidateShortlistingAuthorityList.as_view(), name='crm_crmemployee_recruitmentmanagement_managecandidateshortlistingauthority_list'),
    url(r'^hrms-employee/recruitmentmanagement/approvingauthority/add/$',AddEditRecruitmentManagementInterveiwManageCandidateShortlistingAuthority.as_view(), name='crm_crmemployee_recruitmentmanagement_managecandidateshortlistingauthority_add'),
    url(r'^hrms-employee/recruitmentmanagement/approvingauthority/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementInterveiwManageCandidateShortlistingAuthority.as_view(), name="crm_crmemployee_recruitmentmanagement_managecandidateshortlistingauthority_edit"),
    url(r'^hrms-employee/recruitmentmanagement/approvingauthority/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementInterveiwManageCandidateShortlistingAuthorityDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_managecandidateshortlistingauthority_delete'),

    url(r'^hrms-employee/recruitmentmanagement/manageselectionprocess/list/$', RecruitmentManagementInterveiwManageSelectionProcessList.as_view(), name='crm_crmemployee_recruitmentmanagement_manageselectionprocess_list'),
    url(r'^hrms-employee/recruitmentmanagement/manageselectionprocess/add/$',AddEditRecruitmentManagementInterveiwManageSelectionProcess.as_view(), name='crm_crmemployee_recruitmentmanagement_manageselectionprocess_add'),
    url(r'^hrms-employee/recruitmentmanagement/manageselectionprocess/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagementInterveiwManageSelectionProcess.as_view(), name="crm_crmemployee_recruitmentmanagement_manageselectionprocess_edit"),
    url(r'^hrms-employee/recruitmentmanagement/manageselectionprocess/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagementInterveiwManageSelectionProcessDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_manageselectionprocess_delete'),

    # Type of Job
    url(r'^hrms-employee/emplyeesservices/manageemployee/typeofjob/list/$', ManagementEmployeeTypeofJobList.as_view(), name='employee_emplyeesservices_typeofjob_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/typeofjob/add/$',AddEditManagementEmployeeTypeofJob.as_view(), name='employee_emplyeesservices_typeofjob_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/typeofjob/edit/(?P<id>[0-9]+)/$',AddEditManagementEmployeeTypeofJob.as_view(), name="employee_emplyeesservices_typeofjob_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/typeofjob/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManagementEmployeeTypeofJobDelete.as_view(), name='employee_emplyeesservices_typeofjob_delete'),
    
    # Payroll of 
    url(r'^hrms-employee/emplyeesservices/manageemployee/payrollof/list/$', ManagementEmployeePayrollofJobList.as_view(), name='employee_emplyeesservices_payrollof_list'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/payrollof/add/$',AddEditManagementEmployeePayrollofJob.as_view(), name='employee_emplyeesservices_payrollof_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/payrollof/edit/(?P<id>[0-9]+)/$',AddEditManagementEmployeePayrollofJob.as_view(), name="employee_emplyeesservices_payrollof_edit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/payrollof/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManagementEmployeePayrollofJobDelete.as_view(), name='employee_emplyeesservices_payrollof_delete'),

    # On boarding & Exit Management Master
    url(r'^hrms-employee/onbboardingexitmanagement/remuneration/list/$', OnboardingExitRemunerationManagementList.as_view(), name='onbboardingexitmanagement_remuneration_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/remuneration/add/$', AddEditOnboardingExitRemunerationManagement.as_view(), name='onbboardingexitmanagement_remuneration_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/remuneration/edit/(?P<id>[0-9]+)/$', AddEditOnboardingExitRemunerationManagement.as_view(), name="onbboardingexitmanagement_remuneration_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/remuneration/delete/(?P<id>[0-9,a-z,A-Z]+)/$', OnboardingExitRemunerationManagementDelete.as_view(), name='onbboardingexitmanagement_remuneration_delete'),

    # Registration Management > Define Employment Type 
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/employmenttype/list/$', RegistrationManagementDefineEmploymentTypeList.as_view(), name='registrationmanagment_employmenttype_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/employmenttype/add/$', AddEditRegistrationManagementDefineEmploymentType.as_view(), name='registrationmanagment_employmenttype_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/employmenttype/edit/(?P<id>[0-9]+)/$', AddEditRegistrationManagementDefineEmploymentType.as_view(), name="registrationmanagment_employmenttype_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/employmenttype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RegistrationManagementDefineEmploymentTypeDelete.as_view(), name='registrationmanagment_employmenttype_delete'),


    # Registration Management > Define Payroll Type 
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/payrolltype/list/$', RegistrationManagementDefinePayrollTypeList.as_view(), name='registrationmanagment_payrolltype_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/payrolltype/add/$', AddEditRegistrationManagementDefinePayrollType.as_view(), name='registrationmanagment_payrolltype_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/payrolltype/edit/(?P<id>[0-9]+)/$', AddEditRegistrationManagementDefinePayrollType.as_view(), name="registrationmanagment_payrolltype_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/payrolltype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RegistrationManagementDefinePayrollTypeDelete.as_view(), name='registrationmanagment_payrolltype_delete'),

    # Registration Management > Define Payroll Agency 
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/payrollagency/list/$', RegistrationManagementDefinePayrollAgencyList.as_view(), name='registrationmanagment_payrollagency_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/payrollagency/add/$', AddEditRegistrationManagementDefinePayrollAgency.as_view(), name='registrationmanagment_payrollagency_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/payrollagency/edit/(?P<id>[0-9]+)/$', AddEditRegistrationManagementDefinePayrollAgency.as_view(), name="registrationmanagment_payrollagency_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/payrollagency/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RegistrationManagementDefinePayrollAgencyDelete.as_view(), name='registrationmanagment_payrollagency_delete'),

    # Registration Management > Define Key Responsibility Areas  
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/keyresponsibilityareas/list/$', RegistrationManagementDefineKeyResponsibilityAreasList.as_view(), name='registrationmanagment_keyresponsibilityareas_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/keyresponsibilityareas/add/$', AddEditRegistrationManagementDefineKeyResponsibilityAreas.as_view(), name='registrationmanagment_keyresponsibilityareas_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/keyresponsibilityareas/edit/(?P<id>[0-9]+)/$', AddEditRegistrationManagementDefineKeyResponsibilityAreas.as_view(), name="registrationmanagment_keyresponsibilityareas_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/registrationmanagment/keyresponsibilityareas/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RegistrationManagementDefineKeyResponsibilityAreasDelete.as_view(), name='registrationmanagment_keyresponsibilityareas_delete'),

    # Exit Management > Define Exit Type
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/exittype/list/$', ExitManagementDefineExitTypeList.as_view(), name='exitmanagement_exittype_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/exittype/add/$', AddEditExitManagementDefineExitType.as_view(), name='exitmanagement_exittype_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/exittype/edit/(?P<id>[0-9]+)/$', AddEditExitManagementDefineExitType.as_view(), name="exitmanagement_exittype_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/exittype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ExitManagementDefineExitTypeDelete.as_view(), name='exitmanagement_exittype_delete'),

    # Exit Management > Define Notice Period
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/noticeperiod/list/$', ExitManagementDefineNoticePeriodList.as_view(), name='exitmanagement_noticeperiod_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/noticeperiod/add/$', AddEditExitManagementDefineNoticePeriod.as_view(), name='exitmanagement_noticeperiod_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/noticeperiod/edit/(?P<id>[0-9]+)/$', AddEditExitManagementDefineNoticePeriod.as_view(), name="exitmanagement_noticeperiod_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/noticeperiod/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ExitManagementDefineNoticePeriodDelete.as_view(), name='exitmanagement_noticeperiod_delete'),

    # Exit Management > Define Final Settlement 
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/finaldsettlement/list/$', ExitManagementDefineFinalSettlementList.as_view(), name='exitmanagement_finaldsettlement_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/finaldsettlement/add/$', AddEditExitManagementDefineFinalSettlement.as_view(), name='exitmanagement_finaldsettlement_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/finaldsettlement/edit/(?P<id>[0-9]+)/$', AddEditExitManagementDefineFinalSettlement.as_view(), name="exitmanagement_finaldsettlement_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/finaldsettlement/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ExitManagementDefineFinalSettlementDelete.as_view(), name='exitmanagement_finaldsettlement_delete'),


    # Exit Management > Define Exit Interview 
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/exitinterview/list/$', ExitManagementDefineExitInterviewList.as_view(), name='exitmanagement_exitinterview_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/exitinterview/add/$', AddEditExitManagementDefineExitInterview.as_view(), name='exitmanagement_exitinterview_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/exitinterview/edit/(?P<id>[0-9]+)/$', AddEditExitManagementDefineExitInterview.as_view(), name="exitmanagement_exitinterview_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/exitmanagement/exitinterview/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ExitManagementDefineExitInterviewDelete.as_view(), name='exitmanagement_exitinterview_delete'),


    # Exit Management > Asset Type
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/assettype/list/$', AssetManagementDefineAssetsTypeList.as_view(), name='assetmanagement_assettype_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/assettype/add/$', AddEditAssetManagementDefineAssetsType.as_view(), name='assetmanagement_assettype_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/assettype/edit/(?P<id>[0-9]+)/$', AddEditAssetManagementDefineAssetsType.as_view(), name="assetmanagement_assettype_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/assettype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', AssetManagementDefineAssetsTypeDelete.as_view(), name='assetmanagement_assettype_delete'),

    # Exit Management > Manage Assets
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/manageasset/list/$', AssetManagementManageAssetsList.as_view(), name='assetmanagement_manageasset_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/manageasset/add/$', AddEditAssetManagementManageAssets.as_view(), name='assetmanagement_manageasset_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/manageasset/edit/(?P<id>[0-9]+)/$', AddEditAssetManagementManageAssets.as_view(), name="assetmanagement_manageasset_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/manageasset/delete/(?P<id>[0-9,a-z,A-Z]+)/$', AssetManagementManageAssetsDelete.as_view(), name='assetmanagement_manageasset_delete'),

    # Exit Management > Define Allocation Policy
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/allocationpolicy/list/$', AssetManagementDefineAllocationPolicyList.as_view(), name='assetmanagement_allocationpolicy_list'),
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/allocationpolicy/add/$', AddEditAssetManagementDefineAllocationPolicy.as_view(), name='assetmanagement_allocationpolicy_add'),
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/allocationpolicy/edit/(?P<id>[0-9]+)/$', AddEditAssetManagementDefineAllocationPolicy.as_view(), name="assetmanagement_allocationpolicy_edit"),
    url(r'^hrms-employee/onbboardingexitmanagement/assetmanagement/allocationpolicy/delete/(?P<id>[0-9,a-z,A-Z]+)/$', AssetManagementDefineAllocationPolicyDelete.as_view(), name='assetmanagement_allocationpolicy_delete'),


    # Performance & Appraisal Management > Performance Management > Define Targets
    url(r'^hrms-employee/performanceappraisalmanagement/performancemanagementtarget/list/$', PerformanceAppraisalManagementPerformanceManagementDefineTargetsList.as_view(), name='performanceappraisalmanagement_performancemanagementtarget_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/performancemanagementtarget/add/$', AddEditPerformanceAppraisalManagementPerformanceManagementDefineTargets.as_view(), name='performanceappraisalmanagement_performancemanagementtarget_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/performancemanagementtarget/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalManagementPerformanceManagementDefineTargets.as_view(), name="performanceappraisalmanagement_performancemanagementtarget_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/performancemanagementtarget/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalManagementPerformanceManagementDefineTargetsDelete.as_view(), name='performanceappraisalmanagement_performancemanagementtarget_delete'),


    # Performance & Appraisal Management > Performance Management >Define Incentive 
    url(r'^hrms-employee/performanceappraisalmanagement/performancemanagementincentive/list/$', PerformanceAppraisalManagementPerformanceManagementDefineIncentiveList.as_view(), name='performanceappraisalmanagement_performancemanagementincentive_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/performancemanagementincentive/add/$', AddEditPerformanceAppraisalManagementPerformanceManagementDefineIncentive.as_view(), name='performanceappraisalmanagement_performancemanagementincentive_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/performancemanagementincentive/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalManagementPerformanceManagementDefineIncentive.as_view(), name="performanceappraisalmanagement_performancemanagementincentive_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/performancemanagementincentive/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalManagementPerformanceManagementDefineIncentiveDelete.as_view(), name='performanceappraisalmanagement_performancemanagementincentive_delete'),


    # Performance & Appraisal Management > Performance Management > Manage Performance Incentive 
    url(r'^hrms-employee/performanceappraisalmanagement/manageperformanceincentive/list/$', PerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentiveList.as_view(), name='performanceappraisalmanagement_manageperformanceincentive_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/manageperformanceincentive/add/$', AddEditPerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentive.as_view(), name='performanceappraisalmanagement_manageperformanceincentive_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/manageperformanceincentive/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentive.as_view(), name="performanceappraisalmanagement_manageperformanceincentive_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/manageperformanceincentive/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalManagementPerformanceManagementManagePerformanceIncentiveDelete.as_view(), name='performanceappraisalmanagement_manageperformanceincentive_delete'),


    url(r'^hrms-employee/performanceappraisalmanagement/appraisalmanagementdefineappraisalfrequency/list/$', PerformanceAppraisalManagementDefineAppraisalFrequencyList.as_view(), name='performanceappraisalmanagement_appraisalmanagementdefineappraisalfrequency_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalmanagementdefineappraisalfrequency/add/$', AddEditPerformanceAppraisalManagementDefineAppraisalFrequency.as_view(), name='performanceappraisalmanagement_appraisalmanagementdefineappraisalfrequency_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalmanagementdefineappraisalfrequency/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalManagementDefineAppraisalFrequency.as_view(), name="performanceappraisalmanagement_appraisalmanagementdefineappraisalfrequency_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalmanagementdefineappraisalfrequency/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalManagementDefineAppraisalFrequencyDelete.as_view(), name='performanceappraisalmanagement_appraisalmanagementdefineappraisalfrequency_delete'),


    url(r'^hrms-employee/performanceappraisalmanagement/appraisalmanagementcrossdepartment/list/$', PerformanceAppraisalManagementDefineCrossDepartmentList.as_view(), name='performanceappraisalmanagement_appraisalmanagementcrossdepartment_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalmanagementcrossdepartment/add/$', AddEditPerformanceAppraisalManagementDefineCrossDepartment.as_view(), name='performanceappraisalmanagement_appraisalmanagementcrossdepartment_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalmanagementcrossdepartment/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalManagementDefineCrossDepartment.as_view(), name="performanceappraisalmanagement_appraisalmanagementcrossdepartment_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalmanagementcrossdepartment/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalManagementDefineCrossDepartmentDelete.as_view(), name='performanceappraisalmanagement_appraisalmanagementcrossdepartment_delete'),


    # Weightage
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalratingdefineweightage/list/$', PerformanceAppraisalDefineAppraisalRatingDefineWeightageList.as_view(), name='performanceappraisalmanagement_appraisalratingdefineweightage_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalratingdefineweightage/add/$', AddEditPerformanceAppraisalDefineAppraisalRatingDefineWeightage.as_view(), name='performanceappraisalmanagement_appraisalratingdefineweightage_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalratingdefineweightage/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalDefineAppraisalRatingDefineWeightage.as_view(), name="performanceappraisalmanagement_appraisalratingdefineweightage_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalratingdefineweightage/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalDefineAppraisalRatingDefineWeightageDelete.as_view(), name='performanceappraisalmanagement_appraisalratingdefineweightage_delete'),


    # Manage Rating
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalratingmanagerating/list/$', PerformanceAppraisalDefineAppraisalRatingManageRatingList.as_view(), name='performanceappraisalmanagement_appraisalratingmanagerating_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalratingmanagerating/add/$', AddEditPerformanceAppraisalDefineAppraisalRatingManageRating.as_view(), name='performanceappraisalmanagement_appraisalratingmanagerating_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalratingmanagerating/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalDefineAppraisalRatingManageRating.as_view(), name="performanceappraisalmanagement_appraisalratingmanagerating_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/appraisalratingmanagerating/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalDefineAppraisalRatingManageRatingDelete.as_view(), name='performanceappraisalmanagement_appraisalratingmanagerating_delete'),


    # Define Appraisal Committee 
    url(r'^hrms-employee/performanceappraisalmanagement/defineappraisalcommittee/list/$', PerformanceAppraisalDefineAppraisalCommitteeList.as_view(), name='performanceappraisalmanagement_defineappraisalcommittee_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/defineappraisalcommittee/add/$', AddEditPerformanceAppraisalDefineAppraisalCommittee.as_view(), name='performanceappraisalmanagement_defineappraisalcommittee_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/defineappraisalcommittee/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalDefineAppraisalCommittee.as_view(), name="performanceappraisalmanagement_defineappraisalcommittee_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/defineappraisalcommittee/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalDefineAppraisalCommitteeDelete.as_view(), name='performanceappraisalmanagement_defineappraisalcommittee_delete'),

    # @@@@@@@@@@@@@@@@@@@@

    # Define Change in Grade
    url(r'^hrms-employee/performanceappraisalmanagement/definechangegrade/list/$', PerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGradeList.as_view(), name='performanceappraisalmanagement_definechangeingrade_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/definechangegrade/add/$', AddEditPerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGrade.as_view(), name='performanceappraisalmanagement_definechangeingrade_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/definechangegrade/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGrade.as_view(), name="performanceappraisalmanagement_definechangeingrade_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/definechangegrade/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalDefineAppraisalBenefitsDefineChangeinGradeDelete.as_view(), name='performanceappraisalmanagement_definechangeingrade_delete'),

   
    # Define Increment 
    url(r'^hrms-employee/performanceappraisalmanagement/defineincrement/list/$', PerformanceAppraisalDefineAppraisalBenefitsDefineIncrementList.as_view(), name='performanceappraisalmanagement_defineincrement_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/defineincrement/add/$', AddEditPerformanceAppraisalDefineAppraisalBenefitsDefineIncrement.as_view(), name='performanceappraisalmanagement_defineincrement_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/defineincrement/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalDefineAppraisalBenefitsDefineIncrement.as_view(), name="performanceappraisalmanagement_defineincrement_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/defineincrement/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalDefineAppraisalBenefitsDefineIncrementDelete.as_view(), name='performanceappraisalmanagement_defineincrement_delete'),


    # Define Appraisal Incentive 
    url(r'^hrms-employee/performanceappraisalmanagement/defineappraisalincentive/list/$', PerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentiveList.as_view(), name='performanceappraisalmanagement_defineappraisalincentive_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/defineappraisalincentive/add/$', AddEditPerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentive.as_view(), name='performanceappraisalmanagement_defineappraisalincentive_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/defineappraisalincentive/edit/(?P<id>[0-9]+)/$', AddEditPerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentive.as_view(), name="performanceappraisalmanagement_defineappraisalincentive_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/defineappraisalincentive/delete/(?P<id>[0-9,a-z,A-Z]+)/$', PerformanceAppraisalDefineAppraisalBenefitsDefineAppraisalIncentiveDelete.as_view(), name='performanceappraisalmanagement_defineappraisalincentive_delete'),

    ############# managepsychometrictest 
    url(r'^hrms-employee/recruitmentmanagement/managepsychometrictest/list/$', RecruitmentManagePsychometricTestList.as_view(), name='crm_crmemployee_recruitmentmanagement_managepsychometrictest_list'),
    url(r'^hrms-employee/recruitmentmanagement/managepsychometrictest/add/$',AddEditRecruitmentManagePsychometricTest.as_view(), name='crm_crmemployee_recruitmentmanagement_managepsychometrictest_add'),
    url(r'^hrms-employee/recruitmentmanagement/managepsychometrictest/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManagePsychometricTest.as_view(), name="crm_crmemployee_recruitmentmanagement_managepsychometrictest_edit"),
    url(r'^hrms-employee/recruitmentmanagement/managepsychometrictest/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManagePsychometricTestDelete.as_view(), name='crm_crmemployee_recruitmentmanagement_managepsychometrictest_delete'),
#
  ############# managetestresult
    url(r'^hrms-employee/recruitmentmanagement/managetestresult/list/$', RecruitmentManageTestResultList.as_view(), name='crm_crmemployee_managetestresult_list'),
    url(r'^hrms-employee/recruitmentmanagement/managetestresult/add/$',AddEditRecruitmentManageTestResult.as_view(), name='crm_crmemployee_managetestresult_add'),
    url(r'^hrms-employee/recruitmentmanagement/managetestresult/edit/(?P<id>[0-9]+)/$',AddEditRecruitmentManageTestResult.as_view(), name="crm_managetestresult_edit"),
    url(r'^hrms-employee/recruitmentmanagement/managetestresult/delete/(?P<id>[0-9,a-z,A-Z]+)/$', RecruitmentManageTestResultDelete.as_view(), name='crm_managetestresult_delete'),

#################updateadvancetype   111  
                          
    url(r'^hrms-employee/emplyeesservices/manageclaims/updateadvancetype/list/$', UpdateAdvanceTypeList.as_view(), name='updateadvancetype_list'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/mupdateadvancetype/add/$', AddEditUpdateAdvanceType.as_view(), name='cupdateadvancetype_add'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/updateadvancetype/edit/(?P<id>[0-9]+)/$', AddEditUpdateAdvanceType.as_view(), name="updateadvancetype_edit"),
    url(r'^hrms-employee/emplyeesservices/manageclaims/updateadvancetype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateAdvanceTypeDelete.as_view(), name='updateadvancetype_delete'),

##############Advance entitlement
    url(r'^hrms-employee/emplyeesservices/manageclaims/dvanceentitlement/list/$', AdvanceEntitlementList.as_view(), name='dvanceentitlement_list'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/dvanceentitlement/add/$', AddEditAdvanceEntitlement.as_view(), name='dvanceentitlement_add'),
    url(r'^hrms-employee/emplyeesservices/manageclaims/dvanceentitlement/edit/(?P<id>[0-9]+)/$', AddEditAdvanceEntitlement.as_view(), name="dvanceentitlement_edit"),
    url(r'^hrms-employee/emplyeesservices/manageclaims/dvanceentitlement/delete/(?P<id>[0-9,a-z,A-Z]+)/$', AdvanceEntitlementDelete.as_view(), name='dvanceentitlement_delete'),

#####updateotherdeductions
    url(r'^hrms-employee/emplyeesservices/managepayroll/updateotherdeductions/list/$',UpdateOtherDeductionsList.as_view(), name='crm_crmemployee_manageemployee_updateotherdeductions_list'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/updateotherdeductions/add/$',AddEditUpdateOtherDeductions.as_view(), name='crm_crmemployee_manageemployee_updateotherdeductions_add'),
    url(r'^hrms-employee/emplyeesservices/managepayroll/updateotherdeductions/edit/(?P<id>[0-9]+)/$',AddEditUpdateOtherDeductions.as_view(), name="crm_crmemployee_manageemployee_updateotherdeductions_edit"),
    url(r'^hrms-employee/emplyeesservices/managepayroll/updateotherdeductions/delete/(?P<id>[0-9,a-z,A-Z]+)/$',UpdateOtherDeductionsDelete.as_view(), name='crm_crmemployee_updateotherdeductions_delete'),


    # UpdateIncentiveType
    url(r'^hrms-employee/performanceappraisalmanagement/updateincentivetype/list/$', UpdateIncentiveTypeList.as_view(), name='performanceappraisalmanagement_updateincentivetype_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/updateincentivetype/add/$', AddEditUpdateIncentiveType.as_view(), name='performanceappraisalmanagement_updateincentivetype_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/updateincentivetype/edit/(?P<id>[0-9]+)/$', AddEditUpdateIncentiveType.as_view(), name="performanceappraisalmanagement_updateincentivetype_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/updateincentivetype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateIncentiveTypeDelete.as_view(), name='performanceappraisalmanagement_updateincentivetype_delete'),

 # UpdateBonus UpdateBonusList
    url(r'^hrms-employee/performanceappraisalmanagement/updatebonus/list/$', UpdateBonusList.as_view(), name='performanceappraisalmanagement_updatebonus_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/updatebonus/add/$', AddEditUpdateBonus.as_view(), name='performanceappraisalmanagement_updatebonus_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/updatebonus/edit/(?P<id>[0-9]+)/$', AddEditUpdateBonus.as_view(), name="performanceappraisalmanagement_updatebonus_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/updatebonus/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateBonusDelete.as_view(), name='performanceappraisalmanagement_updatebonus_delete'),
 # ManageBonus 
    url(r'^hrms-employee/performanceappraisalmanagement/managebonus/list/$', ManageBonusList.as_view(), name='p_managebonus_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/managebonus/add/$', AddEditManageBonus.as_view(), name='p_managebonus_add1'),
    url(r'^hrms-employee/performanceappraisalmanagement/managebonus/edit/(?P<id>[0-9]+)/$', AddEditManageBonus.as_view(), name="p_managebonus_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/managebonus/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManageBonusDelete.as_view(), name='p_managebonus_delete'),

#Update exitapprovalauthority  
    url(r'^hrms-employee/recruitmentmanagement/exitapprovalauthority/list/$', ExitApprovalAuthoritylistingAuthorityList.as_view(), name='crm_exitapprovalauthority_list'),
    url(r'^hrms-employee/recruitmentmanagement/exitapprovalauthority/add/$',AddEditExitApprovalAuthority.as_view(), name='crm_exitapprovalauthority_add'),
    url(r'^hrms-employee/recruitmentmanagement/exitapprovalauthority/edit/(?P<id>[0-9]+)/$',AddEditExitApprovalAuthority.as_view(), name="crm_exitapprovalauthority_edit"),
    url(r'^hrms-employee/recruitmentmanagement/exitapprovalauthority/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ExitApprovalAuthorityDelete.as_view(), name='crm_exitapprovalauthority_delete'),

    ## update appraisal process type
    url(r'^hrms-employee/performanceappraisalmanagement/updateappraisalprocesstype/list/$', UpdateAppraisalProcessTypeList.as_view(), name='performanceappraisalmanagement_updateappraisalprocesstype_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/updateappraisalprocesstype/add/$', AddEditUpdateAppraisalProcessType.as_view(), name='performanceappraisalmanagement_updateappraisalprocesstype_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/updateappraisalprocesstype/edit/(?P<id>[0-9]+)/$', AddEditUpdateAppraisalProcessType.as_view(), name="performanceappraisalmanagement_updateappraisalprocesstype_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/updateappraisalprocesstype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateAppraisalProcessTypelete.as_view(), name='performanceappraisalmanagement_updateappraisalprocesstype_delete'),
####UpdatePyschometricTest
     url(r'^hrms-employee/performanceappraisalmanagement/updatepyschometricest/list/$', UpdatePyschometricTestList.as_view(), name='performanceappraisalmanagement_updatepyschometricest_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/updatepyschometricest/add/$', AddEditUpdatePyschometricTest.as_view(), name='performanceappraisalmanagement_updatepyschometricest_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/updatepyschometricest/edit/(?P<id>[0-9]+)/$', AddEditUpdatePyschometricTest.as_view(), name="performanceappraisalmanagement_updatepyschometricest_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/updatepyschometricest/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UpdatePyschometricTestdelete.as_view(), name='performanceappraisalmanagement_updatepyschometricest_delete'),

######   UpdateAppraisalBenefitType

    url(r'^hrms-employee/performanceappraisalmanagement/updateappraisalbenefittype/list/$',UpdateAppraisalBenefitTypeList.as_view(), name='performanceappraisalmanagement_updateappraisalbenefittype_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/updateappraisalbenefittype/add/$', AddEditUpdateAppraisalBenefitType.as_view(), name='performanceappraisalmanagement_updateappraisalbenefittype_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/updateappraisalbenefittype/edit/(?P<id>[0-9]+)/$', AddEditUpdateAppraisalBenefitType.as_view(), name="performanceappraisalmanagement_updateappraisalbenefittype_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/updateappraisalbenefittype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateAppraisalBenefitTypeDelete.as_view(), name='performanceappraisalmanagement_updateappraisalbenefittype_delete'),

###########ManageGradeChange 
    url(r'^hrms-employee/performanceappraisalmanagement/managegradechange/list/$',ManageGradeChangeList.as_view(), name='performanceappraisalmanagement_managegradechange_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/managegradechange/add/$', AddEditManageGradeChange.as_view(), name='performanceappraisalmanagement_managegradechange_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/managegradechange/edit/(?P<id>[0-9]+)/$', AddEditManageGradeChange.as_view(), name="performanceappraisalmanagement_managegradechange_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/managegradechange/delete/(?P<id>[0-9,a-z,A-Z]+)/$',ManageGradeChangeDelete.as_view(), name='performanceappraisalmanagement_managegradechange_delete'),
 # ManageIncrements
    url(r'^hrms-employee/performanceappraisalmanagement/manageincrements/list/$', ManageIncrementsList.as_view(), name='performanceappraisalmanagement_manageincrements_list1'),
    url(r'^hrms-employee/performanceappraisalmanagement/manageincrements/add/$', AddEditManageIncrements.as_view(), name='performanceappraisalmanagement_manageincrements_add1'),
    url(r'^hrms-employee/performanceappraisalmanagement/manageincrements/edit/(?P<id>[0-9]+)/$', AddEditManageIncrements.as_view(), name="performanceappraisalmanagement_manageincrements_edit1"),
    url(r'^hrms-employee/performanceappraisalmanagement/manageincrements/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManageIncrementsDelete.as_view(), name='performanceappraisalmanagement_manageincrements_delete1'),

### ManageAppraisalIncentive 
    url(r'^hrms-employee/performanceappraisalmanagement/manageappraisalincentive/list/$', ManageAppraisalIncentiveList.as_view(), name='performanceappraisalmanagement_manageappraisalincentive_list'),
    url(r'^hrms-employee/performanceappraisalmanagement/manageappraisalincentive/add/$', AddEditManageAppraisalIncentive.as_view(), name='performanceappraisalmanagement_manageappraisalincentive_add'),
    url(r'^hrms-employee/performanceappraisalmanagement/manageappraisalincentive/edit/(?P<id>[0-9]+)/$', AddEditManageAppraisalIncentive.as_view(), name="performanceappraisalmanagement_manageappraisalincentive_edit"),
    url(r'^hrms-employee/performanceappraisalmanagement/manageappraisalincentive/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManageAppraisalIncentiveDelete.as_view(), name='performanceappraisalmanagement_manageappraisalincentive_delete'),
##
    url(r'^salary/slip/$', ManageSaalry, name= ''),



]   