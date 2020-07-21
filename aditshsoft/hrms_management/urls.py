from hrms_management.views import *
from django.conf.urls import include
from django.conf.urls import url


urlpatterns = [
    url(r'^dashboard/(?P<string>[\w\-]+)/$', CrmDashBoard.as_view(), name='crmdashboard'),
    url(r'^checkemail/$', CrmCheckUserExists.as_view(), name='check_username_exists'),
    url(r'^checkphonenumber/$', CrmCheckPhonenumberxists.as_view(), name='check_phone_exists'),
    url(r'^setupmanagement/allocation/data/user/detail/$', CrmGetUserDetails.as_view(), name='crmgetuserdetail'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/department/list/$', CrmDepartmentList.as_view(), name='crmdepartmentlist'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/department/add/$', CrmDepartmentAdd.as_view(), name='crmdepartmentadd'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/department/edit/(?P<delete>[0-9,a-z,A-Z]+)/$', CrmDepartmentEdit, name="crmdepartmentedit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/department/delete/(?P<delete>[0-9,a-z,A-Z]+)/$', CrmDepartmentdelete.as_view(), name='crmdepartmentdelete'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/designation/list/$', CrmDesignationList.as_view(), name='crmdesignationlist'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/designation/add/$', CrmDesignationAdd.as_view(), name='crmdesignationadd'),  
    url(r'^hrms-employee/emplyeesservices/manageemployee/designation/edit/(?P<delete>[0-9,a-z,A-Z]+)/$', CrmDesignationEdit, name="crmdesignationedit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/designation/delete/(?P<delete>[0-9,a-z,A-Z]+)/$', CrmDesignationdelete.as_view(), name='crmdesignationdelete'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/responselist/list/$', CrmResponsibilityList.as_view(), name='crmresposibilitylist'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/responselist/add/$', CrmResposibilityAdd.as_view(), name='crmresponsibilityadd'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/responselist/edit/(?P<delete>[0-9,a-z,A-Z]+)/$', CrmResponsibilityEdit, name="crmresponsibilityedit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/responselist/delete/(?P<delete>[0-9,a-z,A-Z]+)/$', CrmResponsibilitydelete.as_view(), name='crmresponsibilitydelete'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/role/list/$', RoleManagementList.as_view(), name='crmrolelist'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/role/add/$', AddEditUserRoleManagement.as_view(), name='crm_role_edit_add'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/role/edit/(?P<responseid>[0-9]+)/$', AddEditUserRoleManagement.as_view(), name="crm_role_edit_add"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/role/delete/(?P<delete>[0-9,a-z,A-Z]+)/$', CrmRoleManagementDelete.as_view(), name='crmroledelete'),
    # Manage Financial Year URL
    url(r'^setupmanagement/calender/financial/year/list/$', FinancialYearListView.as_view(), name='crm_list_financial_year'),
    url(r'^setupmanagement/calender/financial/year/add/$', AddFinancialYearView.as_view(), name='crm_add_financial_year'),
    url(r'^setupmanagement/calender/financial/year/edit/(?P<financialid>[0-9]+)/$', AddFinancialYearView.as_view(), name='crm_add_financial_year'),
    url(r'^setupmanagement/calender/financial/year/delete/(?P<financialreportid>[0-9]+)/$', CrmFinancialYearDeletView.as_view(), name='crm_financial_year_delete'),
    # Manage Financial Report URL
    url(r'^setupmanagement/calender/financial/report/list/$', FinancialReportListView.as_view(), name='crm_list_financial_report_year'),
    url(r'^setupmanagement/calender/financial/report/add/$', AddFinancialReportView.as_view(), name='crm_add_financial_report'),
    url(r'^setupmanagement/calender/financial/report/edit/(?P<financialreportid>[0-9]+)/$', AddFinancialReportView.as_view(), name='crm_add_financial_report'),
    url(r'^setupmanagement/calender/financial/report/delete/(?P<financialreportid>[0-9]+)/$', CrmFinancialReportDeletView.as_view(), name='crm_financial_report_delete'),
    # Manage Working Hours URL
    url(r'^setupmanagement/calender/working/hours/list/$', WorkingHoursListView.as_view(), name='crm_list_working_hours'),
    url(r'^setupmanagement/calender/working/hours/add/$', AddWorkingHoursView.as_view(), name='crm_add_working_hours'),
    url(r'^setupmanagement/calender/working/hours/edit/(?P<workinghoursid>[0-9]+)/$', AddWorkingHoursView.as_view(), name='crm_add_working_hours'),
    url(r'^setupmanagement/calender/working/hours/delete/(?P<workinghoursid>[0-9]+)/$', CrmWorkingHoursDeletView.as_view(), name='crm_working_hours_delete'),
    #Manage Working days URL
    url(r'^setupmanagement/calender/working/days/list/$', WorkingDaysListView.as_view(), name='crm_list_working_days'),
    url(r'^setupmanagement/calender/working/days/add/$', AddWorkingDaysView.as_view(), name='crm_add_working_days'),
    url(r'^setupmanagement/calender/working/days/edit/(?P<workingdaysid>[0-9]+)/$', AddWorkingDaysView.as_view(), name='crm_add_working_days'),
    url(r'^setupmanagement/calender/working/days/delete/(?P<workingdaysid>[0-9]+)/$', CrmWorkingDaysDeletView.as_view(), name='crm_working_days_delete'),
    #Manage Over time
    url(r'^setupmanagement/calender/holidaysandleaves/days/list/$', HolidaysListView.as_view(), name='crm_list_holi_days'),
    url(r'^setupmanagement/calender/holidaysandleaves/days/add/$', AddUpdateHoliDaysView.as_view(), name='crm_add_update_holi_days'),
    url(r'^setupmanagement/calender/holidaysandleaves/days/edit/(?P<holidaysdaysid>[0-9]+)/$', AddUpdateHoliDaysView.as_view(), name='crm_add_update_holi_days'),
    url(r'^crm-employee/calender/holidaysandleaves/days/delete/(?P<holidaysdaysid>[0-9]+)/$', HolidaysDeleteView.as_view(), name='crm_holi_days_delete'),
    #Manage Over time
    url(r'^setupmanagement/calender/over/time/list/$', OvertimeListView.as_view(), name='crm_list_over_time'),
    url(r'^setupmanagement/calender/over/time/add/$', AddUpdateOvertimeView.as_view(), name='crm_add_update_over_time'),
    url(r'^setupmanagement/calender/over/time/edit/(?P<overtimeid>[0-9]+)/$', AddUpdateOvertimeView.as_view(), name='crm_add_update_over_time'),
    url(r'^setupmanagement/calender/over/time/delete/(?P<overtimeid>[0-9]+)/$', CrmOvertimeDeletView.as_view(), name='crm_over_time_delete'),
 #Manage Assessment Year #rajesh
    url(r'^setupmanagement/calender/assessment/year/list/$', AssessmentYearListView.as_view(), name='crm_list_assessment_year'),
    url(r'^setupmanagement/calender/assessment/year/add/$', AddAssessmentYearView.as_view(), name='crm_add_assessment_year'),
    url(r'^setupmanagement/calender/assessment/year/edit/(?P<financialid>[0-9]+)/$', AddAssessmentYearView.as_view(), name='crm_add_assessment_year'),
    url(r'^setupmanagement/calender/assessment/year/delete/(?P<financialreportid>[0-9]+)/$', CrmAssessmentYearDeletView.as_view(), name='crm_assessment_year_delete'),
 
    # Manage Response Management URL
    url(r'^setupmanagement/response/list/$', ResponseManagementList.as_view(), name='responselist'),
    url(r'^setupmanagement/response/add/$', AddUpdateResponseManagement.as_view(), name='add_response'),
    url(r'^setupmanagement/response/edit/(?P<responseid>[0-9]+)/$', AddUpdateResponseManagement.as_view(), name='add_response'),
    url(r'^setupmanagement/response/delete/(?P<responseid>[0-9]+)/$', CrmResponseManagementDelete.as_view(), name='delete_response'),
 	# Define Client URLs
    url(r'^setupmanagement/allocation/define/clienttype/list/$', DefineClientypeList.as_view(), name='defineclienttypelist'),
    url(r'^setupmanagement/allocation/define/clienttype/add/$', AddDefineClientType.as_view(), name='defineclienttypeadd'),
    url(r'^setupmanagement/allocation/define/clienttype/edit/(?P<defineclientid>[0-9]+)/$', AddDefineClientType.as_view(), name='defineclienttypeadd'),
    url(r'^setupmanagement/allocation/define/clienttype/delete/(?P<defineclientid>[0-9]+)/$', CrmDefineClientTypeDelete.as_view(), name='defineclienttypedelete'),
    url(r'^setupmanagement/allocation/define/clientcategory/list/$', DefineClientCategoryList.as_view(), name='defineclientcategorylist'),
    url(r'^setupmanagement/allocation/define/clientcategory/add/$', AddDefineClientCategory.as_view(), name='definecliencategorytadd'),
    url(r'^setupmanagement/allocation/define/clientcategory/edit/(?P<defineclientid>[0-9]+)/$', AddDefineClientCategory.as_view(), name='definecliencategorytadd'),
    url(r'^setupmanagement/allocation/define/clientcategory/delete/(?P<defineclientid>[0-9]+)/$', CrmDefineClientCategoryeDelete.as_view(), name='definecliencategorytdelete'),
    url(r'^setupmanagement/allocation/define/clientlead/list/$', DefineClientLeadList.as_view(), name='defineclientleadlist'),
    url(r'^setupmanagement/allocation/define/clientlead/add/$', AddDefineClientLead.as_view(), name='defineclientleadadd'),
    url(r'^setupmanagement/allocation/define/clientlead/edit/(?P<defineclientid>[0-9]+)/$', AddDefineClientLead.as_view(), name='defineclientleadadd'),
    url(r'^setupmanagement/allocation/define/clientlead/delete/(?P<defineclientid>[0-9]+)/$', CrmDefineClientLeadeDelete.as_view(), name='defineclientleaddelete'),
    url(r'^setupmanagement/allocation/define/clienttypeofdata/list/$', DefineClientTypeOfdataList.as_view(), name='defineclienttypeoflistlist'),
    url(r'^setupmanagement/allocation/define/clienttypeofdata/add/$', AddDefineClientTypeOfdata.as_view(), name='defineclienttypeofdataadd'),
    url(r'^setupmanagement/allocation/define/clienttypeofdata/edit/(?P<defineclientid>[0-9]+)/$', AddDefineClientTypeOfdata.as_view(), name='defineclienttypeofdataadd'),
    url(r'^setupmanagement/allocation/define/clienttypeofdata/delete/(?P<defineclientid>[0-9]+)/$', CrmDefineTypeOfDataDelete.as_view(), name='defineclienttypeofdatadelete'),
    url(r'^setupmanagement/allocation/clientsupport/matrix/list/$', CrmAllocationMatrixClientSupportAllocationList.as_view(), name='clientsupportsupportallocationallocationmatrixlist'),
    url(r'^setupmanagement/allocation/clientsupport/matrix/add/$', CrmAddAllocationMatrixClientSupportAllocation.as_view(), name='clientsupportsupportallocationallocationmatrixadd'),
    url(r'^setupmanagement/allocation/clientsupport/matrix/edit/(?P<allocationsetuid>[0-9]+)/$', CrmAddAllocationMatrixClientSupportAllocation.as_view(), name='clientsupportallocationallocationmatrixedit'),
    url(r'^setupmanagement/allocation/clientsupport/matrix/delete/(?P<allocationsetuid>[0-9]+)/$', CrmAllocationMatrixClientSupportDelete.as_view(), name='clientsupportallocationallocationmatrixdelete'),
    url(r'^setupmanagement/allocation/vendorsupport/matrix/list/$', CrmAllocationMatrixVendorSupportAllocationList.as_view(), name='vendorsupportallocationallocationmatrixlist'),
    url(r'^setupmanagement/allocation/vendorsupport/matrix/add/$', CrmAddAllocationMatrixVendorSupportAllocation.as_view(), name='vendorsupportallocationallocationmatrixadd'),
    url(r'^setupmanagement/allocation/vendorsupport/matrix/edit/(?P<allocationsetuid>[0-9]+)/$', CrmAddAllocationMatrixVendorSupportAllocation.as_view(), name='vendorsupportallocationallocationmatrixedit'),
    url(r'^setupmanagement/allocation/vendorsupport/matrix/delete/(?P<allocationsetuid>[0-9]+)/$', CrmAllocationMatrixVendorSupportDelete.as_view(), name='vendorsupportallocationallocationmatrixdelete'),
    # CRM Company Set  
    url(r'^setupmanagement/companyset/company/list/$', CrmCompanySetUpList.as_view(), name='crmparentcompanylist'),   
    url(r'^setupmanagement/companyset/company/addnew/$', CrmAddCompanySetUp, name="addcrmparentcompany"),
    url(r'^setupmanagement/companyset/company/edit/(?P<company_id>[0-9,a-z,A-Z]+)/$', CrmEditCompanySetUp, name="editcrmparentcompany"),
    url(r'^setupmanagement/companyset/company/companydelete/(?P<company_id>[0-9,a-z,A-Z]+)/$', CrmCompanyDataDelete.as_view(), name='crmaparentcompanydelete'),
    # CRM Manage Head Office
    url(r'^setupmanagement/companyset/head/office/list/$', CrmManageHeadOfficeList.as_view(), name='crmmanageheadoffice'),   
    url(r'^setupmanagement/companyset/head/office/add/$', CrmManageHeadOfficeAdd.as_view(), name='crmmanageheadofficeadd'),
    url(r'^setupmanagement/companyset/head/office/edit/(?P<hod_id>[0-9,a-z,A-Z]+)/$', CrmManageHeadOfficeEdit, name='crmmanageheadofficeedit'),
    url(r'^setupmanagement/companyset/head/office/delete/(?P<hod_id>[0-9,a-z,A-Z]+)/$', CrmOfficeDataDelete.as_view(), name='crmofficedelete'),
    # Manage branch
    url(r'^setupmanagement/companyset/manage/branch/list/$', CrmManageBranchList.as_view(), name='crmmanagebranchlist'),
    url(r'^setupmanagement/companyset/manage/branch/add/$', CrmManageBranchAdd.as_view(), name='crmmanagebranchadd'),
    url(r'^setupmanagement/companyset/manage/branch/edit/(?P<branch_id>[0-9,a-z,A-Z]+)/$', CrmManageBranchEdit, name="crmManageBranchEdit"),
    url(r'^setupmanagement/companyset/manage/branch/delete/(?P<branch_id>[0-9,a-z,A-Z]+)/$', CrmBranchDataDelete.as_view(), name='crmbranchdelete'),
    # managecity
    url(r'^setupmanagement/companyset/manage/city/list/$', CrmManageCityList.as_view(), name='crmmanagecitylist'),
    url(r'^setupmanagement/companyset/manage/city/add/$', CrmManageCitiesAdd.as_view(), name='crmmanagecityadd'), 
    url(r'^setupmanagement/companyset/manage/country/add/$', CrmManageCountryAdd.as_view(), name='crmmanagecitycountryadd'), 
    url(r'^setupmanagement/companyset/manage/state/add/$', CrmManageStateAdd.as_view(), name='crmmanagecitystateadd'), 
    url(r'^setupmanagement/companyset/Manage/City/edit/(?P<id>[0-9,a-z,A-Z]+)/$', CrmManageCityEdit, name="crmmanagcityedit"),
    url(r'^setupmanagement/companyset/manage/city/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmCityDelete.as_view(), name='crmcitydelete'),
    # mapcity with branch
    url(r'^setupmanagement/companyset/map/city/list/$', CrmMapCityList.as_view(), name='crmmapcitylist'),   
    url(r'^setupmanagement/companyset/map/city/add/$', CrmMapCityAdd.as_view(), name='crmmapcityadd'),
    url(r'^setupmanagement/companyset/map/city/add/(?P<branch_id_id>[0-9]+)/$', CrmMapCityAdd.as_view(), name='crmmapcityadd'),
    url(r'^setupmanagement/companyset/map/city/delete/(?P<branch_id>[0-9,a-z,A-Z]+)/$', CrmMapCityDelete.as_view(), name='crmmapcitydelete'),
    # UserList
    url(r'^setupmanagement/user/setup/list$', CrmUserSetupList.as_view(), name='crmusersetuplist'),
    url(r'^setupmanagement/user/setup/add/$', CrmUserAdd.as_view(), name='crmusersetupadd'),
    url(r'^setupmanagement/user/setup/edit/(?P<id>[0-9,a-z,A-Z]+)/$', CrmManageUserEdit, name="crmusersetupedit"),
    url(r'^setupmanagement/user/setup/list/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmUserDelete.as_view(), name='crmuserdelete'),
    # # ***** Administrator ************
    # url(r'^setupmanagement/administrator/setup/list$', CrmAdministratorSetupList.as_view(), name='crm_administrator_setup_list'),
    # url(r'^setupmanagement/administrator/setup/add/$', CrmCreateAdministratorUserAddEdit.as_view(), name="crm_create_administrator_user_add"),
    # url(r'^setupmanagement/administrator/setup/edit/(?P<id>[0-9,a-z,A-Z]+)/$', CrmCreateAdministratorUserAddEdit.as_view(), name="crm_create_administrator_user_edit"),
    # url(r'^setupmanagement/administrator/setup/list/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmAdministratorUserDelete.as_view(), name='crm_create_administrator_user_delete'),
    # # Product Managemnt
    url(r'^setupmanagement/product/setup/list/$', CrmProductSetupList.as_view(), name='crmproductsetuplist'),
    url(r'^setupmanagement/product/setup/add/$', CrmProductAdd.as_view(), name='crmproductadd'), 
    url(r'^setupmanagement/product/setup/edit/(?P<id>[0-9,a-z,A-Z]+)/$', CrmManageProductEdit, name="crmmanageproductedit"),
    url(r'^setupmanagement/product/setup/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmProductDelete.as_view(), name='crmproductdelete'),
    
    
    url(r'^setupmanagement/product/productcategory/list/$', CrmManageProductCategoryList.as_view(), name='crm_productcategorylist'),
    url(r'^setupmanagement/product/productcategory/add/$', CrmManageProductCategoryAdd.as_view(), name='crm_productcategoryadd'),
    url(r'^setupmanagement/product/productcategory/edit/(?P<id>[0-9,a-z,A-Z]+)/$', CrmManageProductCategoryEdit, name="crm_productcategoryedit"),
    url(r'^setupmanagement/product/productcategory/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmManageProductCategoryDelete.as_view(), name='crm_productcategorydelete'),
    url(r'^setupmanagement/product/productname/list/$', ManageProductNameList.as_view(), name='productnamelist'),
    url(r'^setupmanagement/product/productname/add/$', ManageProductNameAdd.as_view(), name='productnameadd'),
    url(r'^setupmanagement/product/productname/edit/(?P<id>[0-9,a-z,A-Z]+)/$', ManageProductNameEdit, name="productnameedit"),
    url(r'^setupmanagement/product/productname/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManageProductNameDelete.as_view(), name='productnamedelete'),
    
    
    url(r'^setupmanagement/product/productfacility/list/$', ManageProductFacilityList.as_view(), name='productfacilitylist'),
    url(r'^setupmanagement/product/productfacility/add/$', ManageProductFacilityAdd.as_view(), name='productfacilityadd'), 
    url(r'^setupmanagement/product/productfacility/edit/(?P<id>[0-9,a-z,A-Z]+)/$', ManageProductFacilityEdit, name="productfacilityedit"),
    url(r'^setupmanagement/product/productfacility/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManageProductFacilityDelete.as_view(), name='productfacilitydelete'),
    


    # Bind Country City
    url(r'^setupmanagement/companyset/state/binddata/$', CrmBindData.as_view(), name='crmbinddata'),
    url(r'^setupmanagement/companyset/city/binddatacity/$', CrmBindDataCity.as_view(), name='crmbinddatacity'),
    # Parent Company, Head Office, Branches
    url(r'^setupmanagement/bind/head/office/binddata/$', CrmBindHeadOfficeData.as_view(), name='crmbindheadoffice'),
    url(r'^setupmanagement/bind/branches/binddata/$', CrmBindBranchesData.as_view(), name='crmbindbranches'),
    # Template Set UP >>>>>>>>>>>> Client type
    url(r'^setupmanagement/template/setup/clienttype/list/$', CrmTemapleSetUpClientTypeList.as_view(), name='crmtemapltesetupclienttypelist'),   
    url(r'^setupmanagement/template/setup/clienttype/addnew/$', CrmAddTemaplateClientTypeSetUp, name="crmaddtemapltesetupclienttype"),
    url(r'^setupmanagement/template/setup/clienttype/edit/(?P<temapalte_id>[0-9]+)/$', CrmEditTemaplateClientTypeSetUp, name="crmedittemapltesetupclienttype"),
    url(r'^setupmanagement/template/setup/clienttype/delete/(?P<temapalte_id>[0-9]+)/$', CrmEditTemaplateClientTypeSetUpDelete.as_view(), name='crmdeletetemapltesetupclienttype'),
    # Client Category
    url(r'^setupmanagement/template/setup/clientcategory/list/$', CrmTemapleSetUpClientCategoryList.as_view(), name='crmtemapltesetupclientcategorylist'),   
    url(r'^setupmanagement/template/setup/clientcategory/addnew/$', CrmAddTemaplateClientCategorySetUp, name="crmaddtemapltesetuplientcategory"),
    url(r'^setupmanagement/template/setup/clientcategory/edit/(?P<temapalte_id>[0-9]+)/$', CrmEditTemaplateClientCategorySetUp, name="crmedittemapltesetuplientcategory"),
    url(r'^setupmanagement/template/setup/clientcategory/delete/(?P<temapalte_id>[0-9]+)/$', CrmEditTemaplateClientCategorySetUpDelete.as_view(), name='crmdeletetemapltesetuplientcategory'),
    #customize Template
    url(r'^setupmanagement/template/setup/customizetemplate/list/$', CrmCustomizeTemplateList.as_view(), name='customizetemplatelist'),
    url(r'^setupmanagement/template/setup/customizetemplate/add/$', CrmCustomizeTemplateAdd.as_view(), name='customizetemplateadd'), 
    url(r'^setupmanagement/template/setup/customizetemplate/edit/(?P<id>[0-9,a-z,A-Z]+)/$', CrmCustomizeTemplateEdit, name='customizetemplateedit'),
    url(r'^setupmanagement/template/setup/customizetemplate/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmCustomizeTemplateDelete.as_view(), name='customizetemplatedelete'),
    
    #****************** Currency Set up
    url(r'^setupmanagement/currencysetup/typecurrency/list/$', CrmTypeofCurrencyList.as_view(), name='crmtypeofcurrencylist'),   
    url(r'^setupmanagement/currencysetup/typecurrency/add/$', CrmAddTypeofCurrency, name="crmaddtypeofcurrency"),
    url(r'^setupmanagement/currencysetup/typeurrency/edit/(?P<id>[0-9]+)/$', CrmEditTypeofCurrency, name="crmedittypeofcurrency"),
    url(r'^setupmanagement/currencysetup/typecurrency/delete/(?P<id>[0-9]+)/$', CrmTypeofCurrencyDelete.as_view(), name='crmtypeofcurrencydelete'),
    url(r'^setupmanagement/currencysetup/purposecurrency/list/$', CrmPurposeofCurrencyList.as_view(), name='crmpurposeofcurrencylist'),   
    url(r'^setupmanagement/currencysetup/purposecurrency/add/$', CrmAddPurposeofCurrency, name="crmaddpurposeofcurrency"),
    url(r'^setupmanagement/currencysetup/purposeurrency/edit/(?P<id>[0-9]+)/$', CrmEditPurposeofCurrency, name="crmeditpurposeofcurrency"),
    url(r'^setupmanagement/currencysetup/purposecurrency/delete/(?P<id>[0-9]+)/$', CrmPurposeofCurrencyDelete.as_view(), name='crmpurposeofcurrencydelete'),
    url(r'^setupmanagement/currencysetup/list/$', CrmCurrencySetUpList.as_view(), name='crmcurrecncysetuplist'),   
    url(r'^setupmanagement/currencysetup/add/$', CrmAddCurrencySetUp, name="crmaddcurrecncysetup"),
    url(r'^setupmanagement/currencysetup/edit/(?P<id>[0-9]+)/$', CrmEditCurrencySetUp, name="crmeditcurrecncysetup"),
    url(r'^setupmanagement/currencysetup/delete/(?P<id>[0-9]+)/$', CrmCurrencySetUpDelete.as_view(), name='crmcurrecncysetupdelete'),
##########  Manage Currency Rates  ##Rajesh
    url(r'^setupmanagement/currencysetup/currencyrate/list/$', CrmCurrencyRateList.as_view(), name='crmcurrencyratelist'),   
    url(r'^setupmanagement/currencysetup/currencyrate/add/$', CrmAddCurrencyRate, name="crmaddcurrencyrate"),
    url(r'^setupmanagement/currencysetup/currencyrate/edit/(?P<id>[0-9]+)/$', CrmEditCurrencyRate, name="crmeditcurrencyrate"),
    url(r'^setupmanagement/currencysetup/currencyrate/delete/(?P<id>[0-9]+)/$', CrmCurrencyRateDelete.as_view(), name='crmcurrencyrate'),


    # ============= Bulk and Mail Set Up ============================
    url(r'^setupmanagement/bulkmail/smsmessages/list/$', CrmBulkSmsList.as_view(), name='crmbulkmessageslist'),
    url(r'^setupmanagement/bulkmail/emailmessages/list/$', CrmMailSmsList.as_view(), name='crmmailmessageslist'),
    # ============= Notification Set Up ============================
    url(r'^setupmanagement/escalation/define/level/list/$', CrmEscalationMatrixDefineLevelsList.as_view(), name='crmescalationmatrixdefinelevelslist'),
    url(r'^setupmanagement/escalation/define/level/add/$', CrmAddEscalationMatrixDefineLevels, name="crmaddescalationmatrixdefinelevels"),
    url(r'^setupmanagement/escalation/define/level/edit/(?P<id>[0-9]+)/$', CrmEditEscalationMatrixDefineLevels, name="crm_edit_escalation_matrix_define_levels"),
    url(r'^setupmanagement/escalation/define/level/delete/(?P<id>[0-9]+)/$', CrmEscalationMatrixDefineLevelsDelete.as_view(), name='crm_escalation_matrix_define_delete'),
    url(r'^setupmanagement/escalation/define/tat/list/$', CrmEscalationMatrixDefineTurnAroundTimeList.as_view(), name='crm_escalation_matrix_tot_list'),
    url(r'^setupmanagement/escalation/define/tat/add/$', CrmAddEscalationMatrixDefineTurnAroundTime, name="crm_add_escalation_matrix_tot"),
    url(r'^setupmanagement/escalation/define/tat/edit/(?P<id>[0-9]+)/$', CrmEditEscalationMatrixDefineTurnAroundTime, name="crm_edit_escalation_matrix_tot_list"),
    url(r'^setupmanagement/escalation/define/tat/delete/(?P<id>[0-9]+)/$', CrmEscalationMatrixDefineTurnAroundTimeDelete.as_view(), name='crm_escalation_matrix_tot_delete'),
    # ========== SMS Notification ===================================
    url(r'^setupmanagement/notificationsetup/define/subject/list/$', CrmSmsNotificationSubjectList.as_view(), name='crm_define_notification_subject_list'),
    url(r'^setupmanagement/notificationsetup/define/subject/add/$', CrmAddSmsNotificationSubject, name="crm_add_define_notification_subject_list"),
    url(r'^setupmanagement/notificationsetup/define/subject/edit/(?P<id>[0-9]+)/$', CrmEditSmsNotificationSubject, name="crm_edit_define_notification_subject_list"),
    url(r'^setupmanagement/notificationsetup/define/subject/delete/(?P<id>[0-9]+)/$', CrmSmsNotificationSubjectDelete.as_view(), name='crm_define_notification_subject_delete'),
    # ========== Notification Type ===================================
    url(r'^setupmanagement/notificationsetup/notification/type/list/$', CrmSmsNotificationTypeList.as_view(), name='crm_define_notification_type_list'),
    url(r'^setupmanagement/notificationsetup/notification/type/add/$', CrmAddSmsNotificationType, name="crm_add_define_notification_type_list"),
    url(r'^setupmanagement/notificationsetup/notification/type/edit/(?P<id>[0-9]+)/$', CrmEditSmsNotificationType, name="crm_edit_define_notification_type_list"),
    url(r'^setupmanagement/notificationsetup/notification/type/delete/(?P<id>[0-9]+)/$', CrmSmsNotificationTypeDelete.as_view(), name='crm_define_notification_type_delete'),
    # ========== Notification Type ===================================
    url(r'^setupmanagement/notificationsetup/notification/frequency/list/$', CrmSmsNotificationFrequencyList.as_view(), name='crm_define_notification_frequency_list'),
    url(r'^setupmanagement/notificationsetup/notification/frequency/add/$', CrmAddSmsNotificationFrequency, name="crm_add_define_notification_frequency_list"),
    url(r'^setupmanagement/notificationsetup/notification/frequency/edit/(?P<id>[0-9]+)/$', CrmEditSmsNotificationFrequency, name="crm_edit_define_notification_frequency_list"),
    url(r'^setupmanagement/notificationsetup/notification/frequency/delete/(?P<id>[0-9]+)/$', CrmSmsNotificationFrequencyDelete.as_view(), name='crm_define_notification_frequency_delete'),
    # ========== Import Motification ===================================
    url(r'^setupmanagement/notificationsetup/import/notification/list/$', CrmSmsNotificationTypeofMessageList.as_view(), name='crm_define_notification_type_message_list'),
    url(r'^setupmanagement/notificationsetup/import/notification/add/$', CrmAddSmsNotificationTypeofMessage, name="crm_add_define_notification_frequency_type_message_list"),
    url(r'^setupmanagement/notificationsetup/import/notification/edit/(?P<id>[0-9]+)/$', CrmEditSmsNotificationTypeofMessage, name="crm_edit_define_notificatio_type_message_list"),
    url(r'^setupmanagement/notificationsetup/import/notification/delete/(?P<id>[0-9]+)/$', CrmSmsNotificationTypeofMessageDelete.as_view(), name='crm_define_notification_type_message_delete'),
    # ========== Import Of Message ===================================
    url(r'^setupmanagement/notificationsetup/target/audience/list/$', CrmSmsTargetAudienceMessageList.as_view(), name='crm_define_notification_import_message_list'),
    url(r'^setupmanagement/notificationsetup/target/audience/add/$', CrmSmsTargetAudienceMessageAddView, name="crm_add_define_notification_frequency_import_message"),
    url(r'^setupmanagement/notificationsetup/target/audience/edit/(?P<id>[0-9]+)/$', CrmSmsTargetAudienceMessageEditView, name="crm_edit_define_notificatio_import_message"),
    url(r'^setupmanagement/notificationsetup/target/audience/delete/(?P<id>[0-9]+)/$', CrmSmsTargetAudienceMessageeDelete.as_view(), name='crm_define_notification_import_message_delete'),
    # ========== Group Messages ===================================
    url(r'^setupmanagement/notificationsetup/group/message/list/$', CrmSmsGroupofMessageList.as_view(), name='crm_define_notification_group_message_list'),
    url(r'^setupmanagement/notificationsetup/group/message/add/$', CrmAddGroupofMessage, name="crm_add_define_notification_frequency_group_message"),
    url(r'^setupmanagement/notificationsetup/group/message/edit/(?P<id>[0-9]+)/$', CrmEditGroupofMessage, name="crm_edit_define_notificatio_group_message"),
    url(r'^setupmanagement/notificationsetup/group/message/delete/(?P<id>[0-9]+)/$', CrmSmsSmsGroupeofMessageeDelete.as_view(), name='crm_define_notification_group_message_delete'),
    # ========== Define Template For Notification ===================================
    url(r'^setupmanagement/notificationsetup/template/for/notification/list/(?P<id>[0-9]+)/$', CrmDefineTemplateForNotificationList.as_view(), name='crm_define_template_for_notification_list'),
    url(r'^setupmanagement/notificationsetup/template/for/notification/add/(?P<id>[0-9]+)/$', CrmDefineTemplateForNotificationAddView, name="crm_define_template_for_notification_add"),
    url(r'^setupmanagement/notificationsetup/template/for/notification/edit/(?P<id>[0-9]+)/$', CrmDefineTemplateForNotificationEditView, name="crm_define_template_for_notification_edit"),
    url(r'^setupmanagement/notificationsetup/template/for/notification/delete/(?P<id>[0-9]+)/$', CrmDefineTemplateForNotificationDelete.as_view(), name='crm_define_template_for_notification_delete'),
    # ================================ Audit Trail Setup ================================================
    url(r'^setupmanagement/auditrail/audit/trail/list/$', CrmAuditTrailSetupList.as_view(), name='crm_gps_audit_trail_list'),
    # =================== Table and Code Set Up ======================================================
    url(r'^setupmanagement/tablecodesetup/table/code/list/$', CrmTableCodeList.as_view(), name='crm_table_code_list'),
    # =================== MIS and Reporting  >> Manage Performance > Define Targets ======================================================
    url(r'^setupmanagement/misreporting/manage/performance/define/target/list/$', CrmMisReportingManagePerformanceList.as_view(), name='crm_mis_reporting_manage_performance_list'),
    url(r'^setupmanagement/misreporting/manage/performance/define/target/add/$', CrmMisReportingManagePerformanceAddView, name='crm_mis_reporting_manage_performance_add'),
    url(r'^setupmanagement/misreporting/manage/performance/define/target/edit/(?P<id>[0-9]+)/$', CrmMisReportingManagePerformanceEditView, name='crm_mis_reporting_manage_performance_edit'),
    url(r'^setupmanagement/misreporting/manage/performance/define/target/delete/(?P<id>[0-9]+)/$', CrmMisReportingManagePerformanceDeleteView.as_view(), name='crm_mis_reporting_manage_performance_delete'),
    # *************** Manage Reportting
    url(r'^setupmanagement/misreporting/manage/Reportting/report/format/list/$', CrmMisReportingManageReportFormatList.as_view(), name='crm_mis_reporting_manage_report_format_list'),
    url(r'^setupmanagement/misreporting/manage/Reportting/report/format/add/$', CrmMisReportingManageReportFormatAddView, name='crm_mis_reporting_manage_report_format_add'),
    url(r'^setupmanagement/misreporting/manage/Reportting/report/format/edit/(?P<id>[0-9]+)/$', CrmMisReportingManageReportFormatEditView, name='crm_mis_reporting_manage_report_format_edit'),
    url(r'^setupmanagement/misreporting/manage/Reportting/report/format/delete/(?P<id>[0-9]+)/$', CrmMisReportingManageReportFormatDeleteView.as_view(), name='crm_mis_reporting_manage_report_format_delete'),
    # *************** Manage Frequency
    url(r'^setupmanagement/misreporting/manage/Reportting/report/frequency/list/$', CrmMisReportingManageReportFrequencyList.as_view(), name='crm_mis_reporting_manage_report_frequency_list'),
    url(r'^setupmanagement/misreporting/manage/Reportting/report/frequency/add/$', CrmMisReportingManageReportFrequencyAddView, name='crm_mis_reporting_manage_report_frequency_add'),
    url(r'^setupmanagement/misreporting/manage/Reportting/report/frequency/edit/(?P<id>[0-9]+)/$', CrmMisReportingManageReportFrequencyEditView, name='crm_mis_reporting_manage_report_frequency_edit'),
    url(r'^setupmanagement/misreporting/manage/Reportting/report/frequency/delete/(?P<id>[0-9]+)/$', CrmMisReportingManageReportFrequencyDeleteView.as_view(), name='crm_mis_reporting_manage_report_frequency_delete'),
    # *************** Manage Template
    url(r'^setupmanagement/misreporting/manage/reportting/report/template/list/$', CrmMisReportingManageReportTemplateList.as_view(), name='crm_mis_reporting_manage_report_template_list'),
    url(r'^setupmanagement/misreporting/manage/reportting/report/template/add/$', CrmMisReportingManageReportTemplateEditView.as_view(), name='crm_mis_reporting_manage_report_template_edit'),
    url(r'^setupmanagement/misreporting/manage/reportting/report/template/edit/(?P<id>[0-9]+)/$', CrmMisReportingManageReportTemplateEditView.as_view(), name='crm_mis_reporting_manage_report_template_edit'),
    url(r'^setupmanagement/misreporting/manage/reportting/report/template/delete/(?P<id>[0-9]+)/$', CrmMisReportingManageReportTemplateDeleteView.as_view(), name='crm_mis_reporting_manage_report_template_delete'),
    # ***************************** DownLoad MIS
    url(r'^setupmanagement/misreporting/download/location/tracking/$', CrmMisReportingForDownloadLocationTrackingUserView.as_view(), name='crm_mis_reporting_download_location_tracking'),
    url(r'^setupmanagement/misreporting/download/user/attendance/$', CrmMisReportingForDownloadAttendenceUserView.as_view(), name='crm_mis_reporting_download_user_attendence'),
    # ================================ Access and Permisson ================================
    url(r'^setupmanagement/accesspermisson/permission/type/list/$', CrmAccessPermissonList.as_view(), name='crm_access_permisson_list'),
    url(r'^setupmanagement/accesspermisson/permission/type/add/$', CrmAddPermissonType, name='crm_add_access_permisson_type'),
    url(r'^setupmanagement/accesspermisson/permission/type/edit/(?P<id>[0-9]+)/$', CrmEditPermissonType, name='crm_edit_access_permisson_type'),
    url(r'^setupmanagement/accesspermisson/permission/type/delete/(?P<id>[0-9]+)/$', CrmPermissonTypeDelete.as_view(), name='crm_access_permisson_type_delete'),
    url(r'^setupmanagement/accesspermisson/permission/level/list/$', CrmAccessPermissonLevelList.as_view(), name='crm_access_permisson_level_list'),
    url(r'^setupmanagement/accesspermisson/permission/level/add/$', CrmAddPermissonLevelType, name='crm_add_access_permisson_level'),
    url(r'^setupmanagement/accesspermisson/permission/level/edit/(?P<id>[0-9]+)/$', CrmEditPermissonLevelType, name='crm_edit_access_permisson_level'),
    url(r'^setupmanagement/accesspermisson/permission/level/delete/(?P<id>[0-9]+)/$', CrmPermissonTypeLevelDelete.as_view(), name='crm_access_permisson_level_delete'),
    url(r'^setupmanagement/accesspermisson/reporting/type/list/$', CrmAccessPermissonReprtingTypeList.as_view(), name='crm_access_permisson_reporting_type_list'),
    url(r'^setupmanagement/accesspermisson/reporting/type/add/$', CrmAddPermissonReprtingType, name='crm_add_access_permisson_reprting_type'),
    url(r'^setupmanagement/accesspermisson/reporting/type/edit/(?P<id>[0-9]+)/$', CrmEditPermissonReprtingType, name='crm_edit_access_permisson_reporting_type'),
    url(r'^setupmanagement/accesspermisson/reporting/type/delete/(?P<id>[0-9]+)/$', CrmPermissonTypeReprtingTypeDelete.as_view(), name='crm_access_permisson_reporting_type_delete'),
    url(r'^setupmanagement/accesspermisson/reporting/level/list/$', CrmAccessPermissonReprtingLevelList.as_view(), name='crm_access_permisson_reporting_level_list'),
    url(r'^setupmanagement/accesspermisson/reporting/level/add/$', CrmAddPermissonReprtingLevel, name='crm_add_access_permisson_reprting_level'),
    url(r'^setupmanagement/accesspermisson/reporting/level/edit/(?P<id>[0-9]+)/$', CrmEditPermissonReprtingLevel, name='crm_edit_access_permisson_reporting_level'),
    url(r'^setupmanagement/accesspermisson/reporting/level/delete/(?P<id>[0-9]+)/$', CrmPermissonTypeReprtingLevelDelete.as_view(), name='crm_access_permisson_reporting_level_delete'),
    url(r'^setupmanagement/accesspermisson/define/hierarchy/list/$', CrmAccessPermissonHierarchyList.as_view(), name='crm_access_permisson_hierarchy_list'),
    url(r'^setupmanagement/accesspermisson/define/hierarchy/add/$', CrmAddPermissonHierarchyType, name='crm_add_access_permisson_hierarchy'),
    url(r'^setupmanagement/accesspermisson/define/hierarchy/edit/(?P<id>[0-9]+)/$', CrmEditPermissonHierarchyType, name='crm_edit_access_permisson_hierarchy'),
    url(r'^setupmanagement/accesspermisson/define/hierarchy/delete/(?P<id>[0-9]+)/$', CrmPermissonTypeHierarchyDelete.as_view(), name='crm_access_permisson_hierarchy_delete'),
    url(r'^setupmanagement/accesspermisson/provide/permission/$', ProvideAccessAndPermissionView.as_view(), name='crm_provide_permission_access_permission'),
    url(r'^setupmanagement/accesspermisson/user/list/$', AccessPermissionUserLisView.as_view(), name='crm_access_user_permission_user_list'),





    
    
    url(r'^file/uploader/$', UploadImage.as_view(), name='uploadimage'),
    # Approval Matrix
    url(r'^setupmanagement/approvalmatrix/definelevel/list/$', CrmApprovalMatrixiDefineApprovalLevelList.as_view(), name='crm_approval_matrix_define_approval_level_list'),
    url(r'^setupmanagement/approvalmatrix/definelevel/add/$', CrmAddEditCrmApprovalMatrixiDefineApprovalLevel.as_view(), name='crm_approval_matrix_define_approval_level_add'),
    url(r'^setupmanagement/approvalmatrix/definelevel/edit/(?P<id>[0-9]+)/$', CrmAddEditCrmApprovalMatrixiDefineApprovalLevel.as_view(), name="crm_approval_matrix_define_approval_level_edit"),
    url(r'^setupmanagement/approvalmatrix/definelevel/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmApprovalMatrixiDefineApprovalLevelDelete.as_view(), name='crm_approval_matrix_define_approval_level_delete'),
    url(r'^setupmanagement/approvalmatrix/processlevel/list/$', CrmApprovalMatrixiDefineProcessLevelList.as_view(), name='crm_approval_matrix_define_process_level_list'),
    url(r'^setupmanagement/approvalmatrix/processlevel/add/$', CrmAddEditCrmApprovalMatrixiDefineProcessLevel.as_view(), name='crm_approval_matrix_define_process_level_add'),
    url(r'^setupmanagement/approvalmatrix/processlevel/edit/(?P<id>[0-9]+)/$', CrmAddEditCrmApprovalMatrixiDefineProcessLevel.as_view(), name="crm_approval_matrix_define_process_level_edit"),
    url(r'^setupmanagement/approvalmatrix/processlevel/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmApprovalMatrixiDefineProcessLevelDelete.as_view(), name='crm_approval_matrix_define_process_level_delete'),
    url(r'^setupmanagement/approvalmatrix/mapwithprocess/list/$', CrmApprovalMatrixMapApprovalLevelWithUsersList.as_view(), name='crm_approval_matrix_define_mapwithprocess_list'),
    url(r'^setupmanagement/approvalmatrix/mapwithprocess/add/$', CrmAddEditCrmApprovalMatrixMapApprovalLevelWithUsers.as_view(), name='crm_approval_matrix_mapwithprocess_add'),
    url(r'^setupmanagement/approvalmatrix/mapwithprocess/edit/(?P<id>[0-9]+)/$', CrmAddEditCrmApprovalMatrixMapApprovalLevelWithUsers.as_view(), name="crm_approval_matrix_define_mapwithprocess_edit"),
    url(r'^setupmanagement/approvalmatrix/mapwithprocess/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmApprovalMatrixMapApprovalLevelWithUsersDelete.as_view(), name='crm_approval_matrix_define_mapwithprocess_delete'),
    # Product Category
    url(r'^setupmanagement/product/updaterevenue/list/$', CrmManageUpdateRevenueList.as_view(), name='crm_productcategorylist'),
    url(r'^setupmanagement/product/updaterevenue/add/$', CrmManageUpdateRevenueAdd.as_view(), name='crm_productcategoryadd'),
    url(r'^setupmanagement/product/updaterevenue/edit/(?P<id>[0-9,a-z,A-Z]+)/$', CrmManageUpdateRevenueEdit, name="crm_productcategoryedit"),
    url(r'^setupmanagement/product/updaterevenue/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmManageUpdateRevenueDelete.as_view(), name='crm_productcategorydelete'),
    # Notification Action
    url(r'^setupmanagement/notificationsetup/define/action/list/$', DefineSmsNotificationActionList.as_view(), name='definesmsnotificationactionlist'),
    url(r'^setupmanagement/notificationsetup/define/action/add/$', DefineSmsNotificationActionAdd, name="definesmsnotificationactionadd"),
    url(r'^setupmanagement/notificationsetup/define/action/edit/(?P<id>[0-9]+)/$', DefineSmsNotificationActionEdit, name="definesmsnotificationactionedit"),
    url(r'^setupmanagement/notificationsetup/define/action/delete/(?P<id>[0-9]+)/$', DefineSmsNotificationActionDelete.as_view(), name='definesmsnotificationactiondelete'),



    url(r'^setupmanagement/userprofile/department/view/$', ViewDepartmentList.as_view(), name='viewdepartmentuserprofile'),
    url(r'^setupmanagement/userprofile/designation/view/$', ViewDesignationList.as_view(), name='viewdesignationuserprofile'),
    url(r'^setupmanagement/userprofile/responsibility/view/$', ViewResponsibilityList.as_view(), name='viewresponsibilityuserprofile'),
    url(r'^setupmanagement/userprofile/rolemanagement/view/$', ViewRoleManagementList.as_view(), name='viewrolesuserprofile'),

# USer Type

    url(r'^setupmanagement/userprofile/usertype/list/$', UserTypeList.as_view(), name='usertypelist'),
    url(r'^setupmanagement/userprofile/usertype/edit/(?P<id>[0-9,a-z,A-Z]+)/$', UserTypeEdit, name="usertypeedit"),
    url(r'^setupmanagement/userprofile/usertype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UserTypeDelete.as_view(), name='usertypedelete'),
    url(r'^setupmanagement/userprofile/usertype/$', UserTypeAdd.as_view(), name='usertypeadd'),


# ***** Administrator ************
    url(r'^setupmanagement/userprofile/administrator/setup/list$', CrmAdministratorSetupList.as_view(), name='crm_administrator_setup_list'),
    url(r'^setupmanagement/userprofile/administrator/setup/add/$', CrmCreateAdministratorUserAddEdit.as_view(), name="crm_create_administrator_user_add"),
    url(r'^setupmanagement/userprofile/administrator/setup/edit/(?P<id>[0-9,a-z,A-Z]+)/$', CrmCreateAdministratorUserAddEdit.as_view(), name="crm_create_administrator_user_edit"),
    url(r'^setupmanagement/userprofile/administrator/setup/list/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmAdministratorUserDelete.as_view(), name='crm_create_administrator_user_delete'),
    
 #Define Unit Value 

    url(r'^setupmanagement/unitvalue/list/$', ManageUnitValueList.as_view(), name='unitvaluelist'),
    url(r'^setupmanagement/unitvalue/add/$', ManageUnitValueAdd.as_view(), name='unitvalueadd'), 
    url(r'^setupmanagement/unitvalue/edit/(?P<id>[0-9,a-z,A-Z]+)/$', ManageUnitValueEdit, name="unitvalueedit"),
    url(r'^setupmanagement/unitvalue/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManageUnitValueDelete.as_view(), name='unitvaluedelete'),



# ############## allocational location  Rajesh
    url(r'^setupmanagement/allocation/defineprocess/list/$', ManageProcessAllocationList.as_view(), name='defineprocesslist'),
    url(r'^setupmanagement/allocation/defineprocess/add/$', ManageProcessAllocationAdd.as_view(), name='defineprocessadd'), 
    url(r'^setupmanagement/allocation/defineprocess/edit/(?P<id>[0-9,a-z,A-Z]+)/$', ManageProcessAllocationEdit, name="defineprocessedit"),
    url(r'^setupmanagement/allocation/defineprocess/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManageProcessAllocationDelete.as_view(), name='defineprocessdelete'),

    url(r'^setupmanagement/allocation/reallocation/criteria/list/$', AllocationManagementUpdateReallocationCriteriaList.as_view(), name='approval_matrix_reallocation_criteria_list'),
    url(r'^setupmanagement/allocation/reallocation/criteria/add/$', AddAllocationManagementUpdateReallocationCriteria, name='approval_matrix_reallocation_criteria_add'),
    url(r'^setupmanagement/allocation/reallocation/criteria/edit/(?P<id>[0-9]+)/$', EditAllocationManagementUpdateReallocationCriteria, name="approval_matrix_reallocation_criteria_edit"),
    url(r'^setupmanagement/allocation/reallocation/criteria/delete/(?P<id>[0-9,a-z,A-Z]+)/$', EditAllocationManagementUpdateReallocationCriteriaDelete.as_view(), name='approval_matrix_reallocation_criteria_delete'),


    url(r'^setupmanagement/allocation/manage/reallocation/list/$', AllocationManagementManageReallocationList.as_view(), name='approval_matrix_manage_reallocation_list'),
    url(r'^setupmanagement/allocation/manage/reallocation/add/$', AddAllocationManagementManageReallocation, name='approval_matrix_manage_reallocation_add'),
    url(r'^setupmanagement/allocation/manage/reallocation/edit/(?P<id>[0-9]+)/$', EditAllocationManagementManageReallocation, name="approval_matrix_manage_reallocation_edit"),
    url(r'^setupmanagement/allocation/manage/reallocation/delete/(?P<id>[0-9,a-z,A-Z]+)/$', EditAllocationManagementManageReallocationDelete.as_view(), name='approval_matrix_manage_reallocation_delete'),
  
  	url(r'^setupmanagement/allocation/lead/matrix/list/$', AllocationMatrixLeadAllocationList.as_view(), name='leadallocationallocationmatrixlist'),
    url(r'^setupmanagement/allocation/lead/matrix/add/$', AddAllocationMatrixLeadAllocation.as_view(), name='leadallocationallocationmatrixadd'),
    url(r'^setupmanagement/allocation/lead/matrix/edit/(?P<allocationsetuid>[0-9]+)/$', AddAllocationMatrixLeadAllocation.as_view(), name='leadallocationallocationmatrixedit'),
    url(r'^setupmanagement/allocation/lead/matrix/delete/(?P<allocationsetuid>[0-9]+)/$', AllocationMatrixLeadDelete.as_view(), name='leadallocationallocationmatrixdelete'),
    # url(r'^accesspermisson/define/hierarchy/binddata/$', GetUserDetails.as_view(), name='getuserdetails'),   

#@\
    #Mapp Approval level with joint Users
    url(r'^setupmanagement/approvalmatrix/mapapprovaluser/list/$', MapApprovallevelWithJointUserList.as_view(), name='mapapprovaluser_list'),
    url(r'^setupmanagement/approvalmatrix/mapapprovaluser/add/$', AddEditMapApprovallevelWithJointUser.as_view(), name='mapapprovaluser_add'),
    url(r'^setupmanagement/approvalmatrix/mapapprovaluser/edit/(?P<id>[0-9,a-z,A-Z]+)/$', AddEditMapApprovallevelWithJointUser.as_view(), name="mapapprovaluser_edit"),
    url(r'^setupmanagement/approvalmatrix/mapapprovaluser/delete/(?P<id>[0-9,a-z,A-Z]+)/$', MapApprovallevelWithJointUserDelete.as_view(), name='mapapprovaluser_delete'),

####
    url(r'^escalationmatrix/notificationsetup/manage/escalation/list/$', EscalationManagementManageEscalationList.as_view(), name='escalation_manage_escalation_list'),
    url(r'^escalationmatrix/notificationsetup/manage/escalation/add/$', AddEscalationManagementManageEscalation, name='escalation_manage_escalation_add'),
    url(r'^escalationmatrix/notificationsetup/manage/escalation/edit/(?P<id>[0-9,a-z,A-Z]+)/$', EditEscalationManagementManageEscalation, name="escalation_manage_escalation_edit"),
    url(r'^escalationmatrix/notificationsetup/manage/escalation/delete/(?P<id>[0-9,a-z,A-Z]+)/$', EditEscalationManagementManageEscalationDelete.as_view(), name='escalation_manage_escalation_delete'),
#Month End
    url(r'^Setupmanagement/month-end/managemonthendprocess/list/$', ManageMonthEndProcessList.as_view(), name='managemonthendprocesslist'),
    url(r'^Setupmanagement/month-end/managemonthendprocess/add/$', ManageMonthEndProcessAdd, name='managemonthendprocessadd'), 
    url(r'^Setupmanagement/month-end/managemonthendprocess/edit/(?P<id>[0-9,a-z,A-Z]+)/$', ManageMonthEndProcessEdit, name="managemonthendprocessedit"),
    url(r'^Setupmanagement/month-end/managemonthendprocess/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManageMonthEndProcessDelete.as_view(), name='managemonthendprocessdelete'),

    # #Update Tax Rates 
    url(r'^setupmanagement/product/updatetax/rates/list/$', CrmUpdateTaxRatesList.as_view(), name='crmupdatetaxlist'),
    url(r'^setupmanagement/product/updatetax/rates/add/$', CrmUpdateTaxRatesAdd.as_view(), name='crmupdatetaxadd'), 
    url(r'^setupmanagement/product/updatetax/rates/edit/(?P<id>[0-9,a-z,A-Z]+)/$', CrmUpdateTaxRatesEdit, name="crmupdatetaxedit"),
    url(r'^setupmanagement/product/updatetax/rates/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmUpdateTaxRatesDelete.as_view(), name='crmupdatetaxdelete'),
###############  Manage Pricing 
    url(r'^setupmanagement/product/managepricing/list/$', ManagePricinglist.as_view(), name='managepricinglist'),
    url(r'^setupmanagement/product/managepricing/add/$', ManagePricingAdd.as_view(), name='managepricingadd'), 
    url(r'^setupmanagement/product/managepricing/edit/(?P<id>[0-9,a-z,A-Z]+)/$', ManagePricingEdit, name="managepricingedit"),
    url(r'^setupmanagement/product/managepricing/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManagePricingDelete.as_view(), name='managepricingdelete'),
     
###################### updateemploymentype
    url(r'^hrms-employee/emplyeesservices/manageemployee/updateemploymentype/list/$', CrmUpdateEmploymentTypeList.as_view(), name='crmupdateemploymentypelist'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/updateemploymentype/add/$', CrmUpdateEmploymentTypeAdd.as_view(), name='crmupdateemploymentypeadd'),
    url(r'^hrms-employee/emplyeesservices/manageemployee/updateemploymentype/edit/(?P<delete>[0-9,a-z,A-Z]+)/$', CrmUpdateEmploymentTypeEdit, name="crmupdateemploymentypeedit"),
    url(r'^hrms-employee/emplyeesservices/manageemployee/updateemploymentype/delete/(?P<delete>[0-9,a-z,A-Z]+)/$', CrmUpdateEmploymentTypedelete.as_view(), name='crmupdateemploymentypedelete'),
######Country 
    url(r'^setupmanagement/companyset/manage/countrys/list/$', ManageCountryList.as_view(), name='countrylist'),
    url(r'^setupmanagement/companyset/manage/countrys/add/$', ManageCountryAdd.as_view(), name='countryadd'), 
    url(r'^setupmanagement/companyset/manage/countrys/edit/(?P<id>[0-9,a-z,A-Z]+)/$', ManageCountryEdit, name="countryedit"),
    url(r'^setupmanagement/companyset/manage/countrys/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManageCountryDelete.as_view(), name='countrydelete'),
#######State
    url(r'^setupmanagement/companyset/manage/state/list/$', ManageStateList.as_view(), name='statelist'),
    url(r'^ssetupmanagement/companyset/manage/state/add/$', ManageStateAdd.as_view(), name='stateadd'), 
    url(r'^setupmanagement/companyset/manage/state/edit/(?P<id>[0-9,a-z,A-Z]+)/$', ManageStateEdit, name="stateedit"),
    url(r'^setupmanagement/companyset/manage/state/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ManageStateDelete.as_view(), name='statedelete'),

####################Update Template Type
    url(r'^setupmanagement/template/setup/updatetemplatetype/list/$', UpdateTemplateTypeList.as_view(), name='updatetemplatetypelist'),
    url(r'^setupmanagement/template/setup/updatetemplatetype/add/$', UpdateTemplateTypeAdd.as_view(), name='updatetemplatetypeadd'), 
    url(r'^setupmanagement/template/setup/updatetemplatetype/edit/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateTemplateTypeEdit, name="updatetemplatetypeedit"),
    url(r'^setupmanagement/template/setup/updatetemplatetype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateTemplateTypeDelete.as_view(), name='updatetemplatetypedelete'),


#################### UpdatePurposeofTemplate
    url(r'^setupmanagement/template/setup/updatepurposeoftemplate/list/$', UpdatePurposeofTemplateList.as_view(), name='updatepurposeoftemplatelist'),
    url(r'^setupmanagement/template/setup/updatepurposeoftemplate/add/$', UpdatePurposeofTemplateAdd.as_view(), name='updatepurposeoftemplateeadd'), 
    url(r'^setupmanagement/template/setup/updatepurposeoftemplate/edit/(?P<id>[0-9,a-z,A-Z]+)/$', UpdatePurposeofTemplateEdit, name="updatepurposeoftemplateedit"),
    url(r'^setupmanagement/template/setup/updatepurposeoftemplate/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UpdatePurposeofTemplateDelete.as_view(), name='updatepurposeoftemplatedelete'),


#################### UpdateTemplateRequirement 
    url(r'^setupmanagement/template/setup/updatetemplaterequirement/list/$', UpdateTemplateRequirementList.as_view(), name='updatetemplaterequirementlist'),
    url(r'^setupmanagement/template/setup/updatetemplaterequirement/add/$', UpdateTemplateRequirementAdd.as_view(), name='updatetemplaterequirementadd'), 
    url(r'^setupmanagement/template/setup/updatetemplaterequirement/edit/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateTemplateRequirementEdit, name="updatetemplaterequirementedit"),
    url(r'^setupmanagement/template/setup/updatetemplaterequirement/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateTemplateRequirementDelete.as_view(), name='updatetemplaterequirementdelete'),
############UpdateFieldMasters 

    url(r'^setupmanagement/template/setup/updatefieldmasters/list/$', UpdateFieldMastersList.as_view(), name='updatefieldmasterslist'),
    url(r'^setupmanagement/template/setup/updatefieldmasters/add/$', UpdateFieldMastersAdd.as_view(), name='updatefieldmastersadd'), 
    url(r'^setupmanagement/template/setup/updatefieldmasters/edit/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateFieldMastersEdit, name="updatefieldmastersedit"),
    url(r'^setupmanagement/template/setup/updatefieldmasters/delete/(?P<id>[0-9,a-z,A-Z]+)/$', UpdateFieldMastersDelete.as_view(), name='updatefieldmastersdelete'),


### AdditionalTemplate 
    url(r'^setupmanagement/template/setup/additionaltemplate/list/$', AdditionalTemplateList.as_view(), name='additionaltemplatelist'),
    url(r'^setupmanagement/template/setup/additionaltemplate/add/$', AdditionalTemplateAdd.as_view(), name='additionaltemplateadd'), 
    url(r'^setupmanagement/template/setup/additionaltemplate/edit/(?P<id>[0-9,a-z,A-Z]+)/$', AdditionalTemplateEdit, name="additionaltemplateedit"),
    url(r'^setupmanagement/template/setup/additionaltemplate/delete/(?P<id>[0-9,a-z,A-Z]+)/$', AdditionalTemplateDelete.as_view(), name='additionaltemplatedelete'),

###     ApplicationForm
                                            
    url(r'^setupmanagement/template/setup/applicationform/list/$', ApplicationFormList.as_view(), name='applicationformlist'),
    url(r'^setupmanagement/template/setup/applicationform/add/$', ApplicationFormAdd.as_view(), name='applicationformadd'), 
    url(r'^setupmanagement/template/setup/applicationform/edit/(?P<id>[0-9,a-z,A-Z]+)/$', ApplicationFormEdit, name="applicationformedit"),
    url(r'^setupmanagement/template/setup/applicationform/delete/(?P<id>[0-9,a-z,A-Z]+)/$', ApplicationFormDelete.as_view(), name='applicationformdelete'),



#################
    url(r'^setupmanagement/allocation/clientsupport/matrixs/list/$', CrmAllocationMatrixClientSupportList.as_view(), name='clientsupportsupportallocationallocationmatrixlist1'),
    url(r'^setupmanagement/allocation/clientsupport/matrixs/add/$', CrmAddAllocationMatrixClientSupport.as_view(), name='clientsupportsupportallocationallocationmatrixadd'),
    url(r'^setupmanagement/allocation/clientsupport/matrixs/edit/(?P<id>[0-9]+)/$', CrmAddEditAllocationMatrixClientSupport, name='clientsupportallocationedit'),
    url(r'^setupmanagement/allocation/clientsupport/matrixs/delete/(?P<id>[0-9]+)/$', CrmAllocationMatrixClientSupportsDelete.as_view(), name='clientsupportallocationdelete'),  



###############
    url(r'^setupmanagement/allocation/manage-allocation/list/$', AllocationMatrixsLeadAllocationList.as_view(), name='leadallocationallocationmatrixslist1'),
    url(r'^setupmanagement/allocation/manage-allocation/add/$', AddAllocationMatrixsLeadAllocation.as_view(), name='leadallocationallocationmatrixsadd1'),
    url(r'^setupmanagement/allocation/manage-allocation/edit/(?P<allocationsetuid>[0-9]+)/$', AddAllocationMatrixsLeadAllocation.as_view(), name='leadallocationallocationmatrixsedit1'),
    url(r'^setupmanagement/allocation/manage-allocation/delete/(?P<allocationsetuid>[0-9]+)/$', AllocationMatrixsLeadDelete.as_view(), name='leadallocationallocationmatrixsdelete1'),

#################
    url(r'^setupmanagement/accesspermisson/user/setup/access/permission/(?P<id>[0-9]+)/$', CrmProvideAccessPermisson.as_view(), name='crm_provide_access_permisson'),
    
############
   url(r'^accesspermisson/user/access1/permission/(?P<id>[0-9]+)/$',ProvideAccessPermisson.as_view(), name='provide_access_permisson'),

   url(r'^accesspermisson/provide1/permission/$', HrmProvideAccessAndPermissionView.as_view(), name='provide_permission_access_permission'),






]
