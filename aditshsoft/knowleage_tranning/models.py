from django.db import models
from hrms_management.models import *
# Create your models here.


class ManageKnowledgeType(models.Model):
	knowledge_type = models.CharField(unique = True, max_length=200, blank=False, null=False,default='', verbose_name="Knowledge Type")
	start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
	description = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Description")
	is_active = models.BooleanField(default=1, verbose_name="Is Active")
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.knowledge_type

	class Meta:
		db_table = "manage_knowledge_type"


class ManageKnowledgeLevel(models.Model):
	knowledge_level = models.CharField(unique = True, max_length=200, blank=False, null=False,default='', verbose_name="Knowledge Level")
	start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
	description = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Description")
	is_active = models.BooleanField(default=1, verbose_name="Is Active")
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.knowledge_level

	class Meta:
		db_table = "manage_knowledge_level"


class ManageKnowledgeTraningWithType(models.Model):
	knowledge_type = models.ForeignKey(ManageKnowledgeType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Knowledge Type")
	knowledge_level = models.ForeignKey(ManageKnowledgeLevel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Knowledge Level")
	knowledge_name = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Knowledge Name")
	upload_documents = models.FileField(upload_to='documents/%Y/%m/%d/', verbose_name="Upload Documents")
	start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
	is_active = models.BooleanField(default=1, verbose_name="Is Active")
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "manage_knowledge_traning_with_type"


class ManageKnowledgeProductTrainingType(models.Model):
	training_type  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Training Type")
	product  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Product")
	nature_of_training  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Nature of Training")
	training_name   = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Training Name")
	purpose   = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Purpose")
	start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
	is_active = models.BooleanField(default=1, verbose_name="Is Active")
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.product

	class Meta:
		db_table = "manage_knowledge_product_training_type"


class ManageKnowledgeProductTraining(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
	approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
	approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)
	location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
	department = models.ForeignKey(ManageDepartment, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Department")
	designation = models.ForeignKey(ManageDesignation, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Designation")
	product = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Product")
	training_type  = models.ForeignKey(ManageKnowledgeProductTrainingType, on_delete=models.SET_NULL, blank=True, null=True,  verbose_name="Training Type")
	nature_of_training  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Nature of Training")
	training_name  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Training Name")
	purpose_of_training  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Purpose of Training")
	max_no_of_participant  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Max No of Participant")
	faculty  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Faculty")
	venue_of_training  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Venue of Training")
	training_calander  = models.DateField(blank=True, null=True, verbose_name="Training Calander")
	start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
	is_active = models.BooleanField(default=1, verbose_name="Is Active")
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = "manage_knowledge_product_training"


class ManageKnowledgeProductPromotionType(models.Model):
	promotion_type  = models.CharField(unique = True, max_length=200, blank=False, null=False,default='', verbose_name="Promotion Type")
	details_of_promotion  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Details of Promotion")
	start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
	is_active = models.BooleanField(default=1, verbose_name="Is Active")
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.promotion_type

	class Meta:
		db_table = "manage_knowledge_product_promotion_type"


class ManageKnowledgeProductPromotions(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank= False, null=True)
	location  = models.ForeignKey(ManageBranch, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Location")
	product = models.ForeignKey(ManageKnowledgeProductTrainingType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Product")
	promotion_type = models.ForeignKey(ManageKnowledgeProductPromotionType, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Promotion Type")
	details_of_promotion  = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Details of Promotion")
	applicable_to   = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Applicable to")
	purpose_of_promotion   = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Purpose of promotion")
	promotion_period    = models.CharField(max_length=200, blank=False, null=False,default='', verbose_name="Promotion Period")
	start_date = models.DateField(blank=True, null=True, verbose_name="Start Date")
	is_active = models.BooleanField(default=1, verbose_name="Is Active")
	added = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	approval_level = models.ForeignKey(ApprovalMatrixiDefineApprovalLevel, blank=False, null=True, on_delete=models.SET_NULL, verbose_name="Approval Level")
	approval_level_all_status   = models.CharField(default='', blank=True, null=True, max_length=200)

	class Meta:
		db_table = "manage_knowledge_product_promotions"


