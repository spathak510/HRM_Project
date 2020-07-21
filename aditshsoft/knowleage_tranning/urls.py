from knowleage_tranning.views import *
from django.conf.urls import include
from django.conf.urls import url


# Knowledge and Training
urlpatterns = [
    url(r'^knowledgetraining/knowledgetype/list/$', CrmKnowledgeandTrainingDefineKnowledgeTypeList.as_view(), name='crm_crmemployee_knowledgetraining_knowledgetype_list'),
    url(r'^knowledgetraining/knowledgetype/add/$', CrmAddEditCrmKnowledgeandTrainingDefineKnowledgeType.as_view(), name='crm_crmemployee_knowledgetraining_knowledgetype_add'),
    url(r'^knowledgetraining/knowledgetype/edit/(?P<id>[0-9]+)/$', CrmAddEditCrmKnowledgeandTrainingDefineKnowledgeType.as_view(), name="crm_crmemployee_knowledgetraining_knowledgetype_edit"),
    url(r'^knowledgetraining/knowledgetype/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmKnowledgeandTrainingDefineKnowledgeTypeDelete.as_view(), name='crm_crmemployee_knowledgetraining_knowledgetype_delete'),
    url(r'^knowledgetraining/defineknowledgelevel/list/$', CrmKnowledgeandTrainingDefineKnowledgeLevelList.as_view(), name='crm_crmemployee_knowledgetraining_defineknowledgelevel_list'),
    url(r'^knowledgetraining/defineknowledgelevel/add/$', CrmAddEditCrmKnowledgeandTrainingDefineKnowledgeLevel.as_view(), name='crm_crmemployee_knowledgetraining_defineknowledgelevel_add'),
    url(r'^knowledgetraining/defineknowledgelevel/edit/(?P<id>[0-9]+)/$', CrmAddEditCrmKnowledgeandTrainingDefineKnowledgeLevel.as_view(), name="crm_crmemployee_knowledgetraining_defineknowledgelevel_edit"),
    url(r'^knowledgetraining/defineknowledgelevel/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmKnowledgeandTrainingDefineKnowledgeLevelDelete.as_view(), name='crm_crmemployee_knowledgetraining_defineknowledgelevel_delete'),
    url(r'^knowledgetraining/manageknowledge/list/$', CrmKnowledgeandTrainingManageKnowledgeList.as_view(), name='crm_crmemployee_knowledgetraining_manageknowledge_list'),
    url(r'^knowledgetraining/manageknowledge/add/$', CrmAddEditCrmKnowledgeandTrainingManageKnowledge.as_view(), name='crm_crmemployee_knowledgetraining_manageknowledge_add'),
    url(r'^knowledgetraining/manageknowledge/edit/(?P<id>[0-9]+)/$', CrmAddEditCrmKnowledgeandTrainingManageKnowledge.as_view(), name="crm_crmemployee_knowledgetraining_manageknowledge_edit"),
    url(r'^knowledgetraining/manageknowledge/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmKnowledgeandTrainingManageKnowledgeDelete.as_view(), name='crm_crmemployee_knowledgetraining_manageknowledge_delete'),
    url(r'^knowledgetraining/defineproductraining/list/$', CrmKnowledgeandTrainingDefineProductTainingList.as_view(), name='crm_crmemployee_knowledgetraining_defineproductraining_list'),
    url(r'^knowledgetraining/defineproductraining/add/$', CrmAddEditCrmKnowledgeandTrainingDefineProductTaining.as_view(), name='crm_crmemployee_knowledgetraining_defineproductraining_add'),
    url(r'^knowledgetraining/defineproductraining/edit/(?P<id>[0-9]+)/$', CrmAddEditCrmKnowledgeandTrainingDefineProductTaining.as_view(), name="crm_crmemployee_knowledgetraining_defineproductraining_edit"),
    url(r'^knowledgetraining/defineproductraining/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmKnowledgeandTrainingDefineProductTainingDelete.as_view(), name='crm_crmemployee_knowledgetraining_defineproductraining_delete'),
    url(r'^knowledgetraining/manageproducttraining/list/$', CrmKnowledgeandTrainingManageProductTrainingList.as_view(), name='crm_crmemployee_knowledgetraining_manageproducttraining_list'),
    url(r'^knowledgetraining/manageproducttraining/add/$', CrmAddEditCrmKnowledgeandTrainingManageProductTraining.as_view(), name='crm_crmemployee_knowledgetraining_manageproducttraining_add'),
    url(r'^knowledgetraining/manageproducttraining/edit/(?P<id>[0-9]+)/$', CrmAddEditCrmKnowledgeandTrainingManageProductTraining.as_view(), name="crm_crmemployee_knowledgetraining_manageproducttraining_edit"),
    url(r'^knowledgetraining/manageproducttraining/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmKnowledgeandTrainingManageProductTrainingDelete.as_view(), name='crm_crmemployee_knowledgetraining_manageproducttraining_delete'),
    url(r'^knowledgetraining/defineproductpromotions/list/$', CrmKnowledgeandTrainingDefineProductPromotionsList.as_view(), name='crm_crmemployee_knowledgetraining_defineproductpromotions_list'),
    url(r'^knowledgetraining/defineproductpromotions/add/$', CrmAddEditCrmKnowledgeandTrainingDefineProductPromotions.as_view(), name='crm_crmemployee_knowledgetraining_defineproductpromotions_add'),
    url(r'^knowledgetraining/defineproductpromotions/edit/(?P<id>[0-9]+)/$', CrmAddEditCrmKnowledgeandTrainingDefineProductPromotions.as_view(), name="crm_crmemployee_knowledgetraining_defineproductpromotions_edit"),
    url(r'^knowledgetraining/defineproductpromotions/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmKnowledgeandTrainingDefineProductPromotionsDelete.as_view(), name='crm_crmemployee_knowledgetraining_defineproductpromotions_delete'),
    url(r'^knowledgetraining/manageproductpromotions/list/$', CrmKnowledgeandTrainingManageProductPromotionsList.as_view(), name='crm_crmemployee_knowledgetraining_manageproductpromotions_list'),
    url(r'^knowledgetraining/manageproductpromotions/add/$', CrmAddEditCrmKnowledgeandManageProductPromotions.as_view(), name='crm_crmemployee_knowledgetraining_manageproductpromotions_add'),
    url(r'^knowledgetraining/manageproductpromotions/edit/(?P<id>[0-9]+)/$', CrmAddEditCrmKnowledgeandManageProductPromotions.as_view(), name="crm_crmemployee_knowledgetraining_manageproductpromotions_edit"),
    url(r'^knowledgetraining/manageproductpromotions/delete/(?P<id>[0-9,a-z,A-Z]+)/$', CrmKnowledgeandTrainingManageProductPromotionsDelete.as_view(), name='crm_crmemployee_knowledgetraining_manageproductpromotions_delete'),
]