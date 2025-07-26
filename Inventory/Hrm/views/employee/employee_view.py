from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.utils import timezone
from django.db.models import Q, Prefetch
from django.contrib.auth.mixins import PermissionRequiredMixin

from Hrm.models import (
    Employee, EducationLevel, EducationQualification, JobExperience,
    DocumentType, EmployeeDocument, FamilyMember
)
from Hrm.forms import (
    EmployeeForm, EmployeeFilterForm, EducationLevelForm, EducationLevelFilterForm,
    EducationQualificationForm, EducationQualificationFilterForm,
    JobExperienceForm, JobExperienceFilterForm, DocumentTypeForm, DocumentTypeFilterForm,
    EmployeeDocumentForm, EmployeeDocumentFilterForm,
    FamilyMemberForm, FamilyMemberFilterForm
)
from config.views import GenericFilterView, GenericDeleteView, BaseExportView, BaseBulkDeleteConfirmView

# ==================== EMPLOYEE VIEWS ====================

class EmployeeListView(GenericFilterView):
    model = Employee
    template_name = 'employee/employee_list.html'
    context_object_name = 'objects'
    paginate_by = 10
    filter_form_class = EmployeeFilterForm
    permission_required = 'Hrm.view_employee'
    
    def apply_filters(self, queryset):
        filters = self.filter_form.cleaned_data
        if filters.get('search'):
            queryset = queryset.filter(
                Q(employee_id__icontains=filters['search']) |
                Q(first_name__icontains=filters['search']) |
                Q(last_name__icontains=filters['search']) |
                Q(email__icontains=filters['search'])
            )
        if filters.get('department'):
            queryset = queryset.filter(department=filters['department'])
        if filters.get('designation'):
            queryset = queryset.filter(designation=filters['designation'])
        if filters.get('employment_status'):
            queryset = queryset.filter(employment_status=filters['employment_status'])
        if filters.get('is_active') == 'true':
            queryset = queryset.filter(is_active=True)
        elif filters.get('is_active') == 'false':
            queryset = queryset.filter(is_active=False)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('hrm:employee_create')
        context['can_create'] = self.request.user.has_perm('Hrm.add_employee')
        context['can_view'] = self.request.user.has_perm('Hrm.view_employee')
        context['can_update'] = self.request.user.has_perm('Hrm.change_employee')
        context['can_delete'] = self.request.user.has_perm('Hrm.delete_employee')
        return context

class EmployeeCardView(GenericFilterView):
    model = Employee
    template_name = 'employee/employee_card_view.html'
    context_object_name = 'objects'
    paginate_by = 12
    filter_form_class = EmployeeFilterForm
    permission_required = 'Hrm.view_employee'
    
    def apply_filters(self, queryset):
        filters = self.filter_form.cleaned_data
        if filters.get('search'):
            queryset = queryset.filter(
                Q(employee_id__icontains=filters['search']) |
                Q(first_name__icontains=filters['search']) |
                Q(last_name__icontains=filters['search']) |
                Q(email__icontains=filters['search'])
            )
        if filters.get('department'):
            queryset = queryset.filter(department=filters['department'])
        if filters.get('designation'):
            queryset = queryset.filter(designation=filters['designation'])
        if filters.get('employment_status'):
            queryset = queryset.filter(employment_status=filters['employment_status'])
        if filters.get('is_active') == 'true':
            queryset = queryset.filter(is_active=True)
        elif filters.get('is_active') == 'false':
            queryset = queryset.filter(is_active=False)
        return queryset

class EmployeeAllView(GenericFilterView):
    model = Employee
    template_name = 'employee/employee_all_view.html'
    context_object_name = 'objects'
    filter_form_class = EmployeeFilterForm
    permission_required = 'Hrm.view_employee'
    
    def apply_filters(self, queryset):
        filters = self.filter_form.cleaned_data
        if filters.get('search'):
            queryset = queryset.filter(
                Q(employee_id__icontains=filters['search']) |
                Q(first_name__icontains=filters['search']) |
                Q(last_name__icontains=filters['search']) |
                Q(email__icontains=filters['search'])
            )
        if filters.get('department'):
            queryset = queryset.filter(department=filters['department'])
        if filters.get('designation'):
            queryset = queryset.filter(designation=filters['designation'])
        if filters.get('employment_status'):
            queryset = queryset.filter(employment_status=filters['employment_status'])
        if filters.get('is_active') == 'true':
            queryset = queryset.filter(is_active=True)
        elif filters.get('is_active') == 'false':
            queryset = queryset.filter(is_active=False)
        return queryset

class EmployeeCreateView(PermissionRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'common/tabs-form.html'
    permission_required = 'Hrm.add_employee'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Employee'
        context['subtitle'] = 'Add a new employee to the system'
        context['cancel_url'] = reverse_lazy('hrm:employee_list')
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()
        messages.success(self.request, f'Employee {self.object.get_full_name()} created successfully.')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('hrm:employee_detail', kwargs={'pk': self.object.pk})

class EmployeeUpdateView(PermissionRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'common/tabs-form.html'
    permission_required = 'Hrm.change_employee'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Employee'
        context['subtitle'] = f'Edit employee {self.object.get_full_name()}'
        context['cancel_url'] = reverse_lazy('hrm:employee_detail', kwargs={'pk': self.object.pk})
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        self.object = form.save()
        messages.success(self.request, f'Employee {self.object.get_full_name()} updated successfully.')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('hrm:employee_detail', kwargs={'pk': self.object.pk})

class EmployeeDetailView(PermissionRequiredMixin, DetailView):
    model = Employee
    template_name = 'employee/employee_detail.html'
    context_object_name = 'employee'
    permission_required = 'Hrm.view_employee'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Employee Details'
        context['subtitle'] = f'Employee: {self.object.get_full_name()}'
        context['cancel_url'] = reverse_lazy('hrm:employee_list')
        context['update_url'] = reverse_lazy('hrm:employee_update', kwargs={'pk': self.object.pk})
        context['delete_url'] = reverse_lazy('hrm:employee_delete', kwargs={'pk': self.object.pk})
        
        # Get related data
        context['education_qualifications'] = self.object.education_qualifications.all()
        context['job_experiences'] = self.object.job_experiences.all()
        context['documents'] = self.object.documents.all()
        context['family_members'] = self.object.family_members.all()
        
        return context

class EmployeeDeleteView(GenericDeleteView):
    model = Employee
    success_url = reverse_lazy('hrm:employee_list')
    permission_required = 'Hrm.delete_employee'

class EmployeeExportView(BaseExportView):
    model = Employee
    permission_required = 'Hrm.view_employee'

class EmployeeBulkDeleteView(BaseBulkDeleteConfirmView):
    model = Employee
    success_url = reverse_lazy('hrm:employee_list')
    permission_required = 'Hrm.delete_employee'

# ==================== EDUCATION LEVEL VIEWS ====================

class EducationLevelListView(GenericFilterView):
    model = EducationLevel
    template_name = 'education/education_level_list.html'
    context_object_name = 'objects'
    paginate_by = 10
    filter_form_class = EducationLevelFilterForm
    permission_required = 'Hrm.view_educationlevel'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('hrm:education_level_create')
        context['can_create'] = self.request.user.has_perm('Hrm.add_educationlevel')
        context['can_view'] = self.request.user.has_perm('Hrm.view_educationlevel')
        context['can_update'] = self.request.user.has_perm('Hrm.change_educationlevel')
        context['can_delete'] = self.request.user.has_perm('Hrm.delete_educationlevel')
        return context

class EducationLevelCreateView(PermissionRequiredMixin, CreateView):
    model = EducationLevel
    form_class = EducationLevelForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.add_educationlevel'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Education Level'
        context['subtitle'] = 'Add a new education level'
        context['cancel_url'] = reverse_lazy('hrm:education_level_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Education Level created successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:education_level_list')

class EducationLevelUpdateView(PermissionRequiredMixin, UpdateView):
    model = EducationLevel
    form_class = EducationLevelForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.change_educationlevel'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Education Level'
        context['subtitle'] = f'Edit {self.object.name}'
        context['cancel_url'] = reverse_lazy('hrm:education_level_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Education Level updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:education_level_list')

class EducationLevelDeleteView(GenericDeleteView):
    model = EducationLevel
    success_url = reverse_lazy('hrm:education_level_list')
    permission_required = 'Hrm.delete_educationlevel'

class EducationLevelExportView(BaseExportView):
    model = EducationLevel
    permission_required = 'Hrm.view_educationlevel'

class EducationLevelBulkDeleteView(BaseBulkDeleteConfirmView):
    model = EducationLevel
    success_url = reverse_lazy('hrm:education_level_list')
    permission_required = 'Hrm.delete_educationlevel'

# ==================== EDUCATION QUALIFICATION VIEWS ====================

class EducationQualificationListView(GenericFilterView):
    model = EducationQualification
    template_name = 'education/education_qualification_list.html'
    context_object_name = 'objects'
    paginate_by = 10
    filter_form_class = EducationQualificationFilterForm
    permission_required = 'Hrm.view_educationqualification'
    
    def apply_filters(self, queryset):
        filters = self.filter_form.cleaned_data
        if filters.get('search'):
            queryset = queryset.filter(
                Q(employee__first_name__icontains=filters['search']) |
                Q(employee__last_name__icontains=filters['search']) |
                Q(degree_title__icontains=filters['search']) |
                Q(institution_name__icontains=filters['search'])
            )
        if filters.get('education_level'):
            queryset = queryset.filter(education_level=filters['education_level'])
        if filters.get('employee'):
            queryset = queryset.filter(employee=filters['employee'])
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('hrm:education_qualification_create')
        context['can_create'] = self.request.user.has_perm('Hrm.add_educationqualification')
        context['can_view'] = self.request.user.has_perm('Hrm.view_educationqualification')
        context['can_update'] = self.request.user.has_perm('Hrm.change_educationqualification')
        context['can_delete'] = self.request.user.has_perm('Hrm.delete_educationqualification')
        return context

class EducationQualificationCreateView(PermissionRequiredMixin, CreateView):
    model = EducationQualification
    form_class = EducationQualificationForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.add_educationqualification'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Education Qualification'
        context['subtitle'] = 'Add education qualification'
        context['cancel_url'] = reverse_lazy('hrm:education_qualification_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Education Qualification created successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:education_qualification_list')

class EducationQualificationUpdateView(PermissionRequiredMixin, UpdateView):
    model = EducationQualification
    form_class = EducationQualificationForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.change_educationqualification'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Education Qualification'
        context['subtitle'] = f'Edit {self.object.degree_title}'
        context['cancel_url'] = reverse_lazy('hrm:education_qualification_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Education Qualification updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:education_qualification_list')

class EducationQualificationDeleteView(GenericDeleteView):
    model = EducationQualification
    success_url = reverse_lazy('hrm:education_qualification_list')
    permission_required = 'Hrm.delete_educationqualification'

class EducationQualificationExportView(BaseExportView):
    model = EducationQualification
    permission_required = 'Hrm.view_educationqualification'

class EducationQualificationBulkDeleteView(BaseBulkDeleteConfirmView):
    model = EducationQualification
    success_url = reverse_lazy('hrm:education_qualification_list')
    permission_required = 'Hrm.delete_educationqualification'

# ==================== JOB EXPERIENCE VIEWS ====================

class JobExperienceListView(GenericFilterView):
    model = JobExperience
    template_name = 'experience/job_experience_list.html'
    context_object_name = 'objects'
    paginate_by = 10
    filter_form_class = JobExperienceFilterForm
    permission_required = 'Hrm.view_jobexperience'
    
    def apply_filters(self, queryset):
        filters = self.filter_form.cleaned_data
        if filters.get('search'):
            queryset = queryset.filter(
                Q(employee__first_name__icontains=filters['search']) |
                Q(employee__last_name__icontains=filters['search']) |
                Q(company_name__icontains=filters['search']) |
                Q(job_title__icontains=filters['search'])
            )
        if filters.get('employee'):
            queryset = queryset.filter(employee=filters['employee'])
        if filters.get('employment_type'):
            queryset = queryset.filter(employment_type=filters['employment_type'])
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('hrm:job_experience_create')
        context['can_create'] = self.request.user.has_perm('Hrm.add_jobexperience')
        context['can_view'] = self.request.user.has_perm('Hrm.view_jobexperience')
        context['can_update'] = self.request.user.has_perm('Hrm.change_jobexperience')
        context['can_delete'] = self.request.user.has_perm('Hrm.delete_jobexperience')
        return context

class JobExperienceCreateView(PermissionRequiredMixin, CreateView):
    model = JobExperience
    form_class = JobExperienceForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.add_jobexperience'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Job Experience'
        context['subtitle'] = 'Add job experience record'
        context['cancel_url'] = reverse_lazy('hrm:job_experience_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Job Experience created successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:job_experience_list')

class JobExperienceUpdateView(PermissionRequiredMixin, UpdateView):
    model = JobExperience
    form_class = JobExperienceForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.change_jobexperience'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Job Experience'
        context['subtitle'] = f'Edit {self.object.job_title} at {self.object.company_name}'
        context['cancel_url'] = reverse_lazy('hrm:job_experience_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Job Experience updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:job_experience_list')

class JobExperienceDeleteView(GenericDeleteView):
    model = JobExperience
    success_url = reverse_lazy('hrm:job_experience_list')
    permission_required = 'Hrm.delete_jobexperience'

class JobExperienceExportView(BaseExportView):
    model = JobExperience
    permission_required = 'Hrm.view_jobexperience'

class JobExperienceBulkDeleteView(BaseBulkDeleteConfirmView):
    model = JobExperience
    success_url = reverse_lazy('hrm:job_experience_list')
    permission_required = 'Hrm.delete_jobexperience'

# ==================== DOCUMENT TYPE VIEWS ====================

class DocumentTypeListView(GenericFilterView):
    model = DocumentType
    template_name = 'document/document_type_list.html'
    context_object_name = 'objects'
    paginate_by = 10
    filter_form_class = DocumentTypeFilterForm
    permission_required = 'Hrm.view_documenttype'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('hrm:document_type_create')
        context['can_create'] = self.request.user.has_perm('Hrm.add_documenttype')
        context['can_view'] = self.request.user.has_perm('Hrm.view_documenttype')
        context['can_update'] = self.request.user.has_perm('Hrm.change_documenttype')
        context['can_delete'] = self.request.user.has_perm('Hrm.delete_documenttype')
        return context

class DocumentTypeCreateView(PermissionRequiredMixin, CreateView):
    model = DocumentType
    form_class = DocumentTypeForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.add_documenttype'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Document Type'
        context['subtitle'] = 'Add a new document type'
        context['cancel_url'] = reverse_lazy('hrm:document_type_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Document Type created successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:document_type_list')

class DocumentTypeUpdateView(PermissionRequiredMixin, UpdateView):
    model = DocumentType
    form_class = DocumentTypeForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.change_documenttype'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Document Type'
        context['subtitle'] = f'Edit {self.object.name}'
        context['cancel_url'] = reverse_lazy('hrm:document_type_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Document Type updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:document_type_list')

class DocumentTypeDeleteView(GenericDeleteView):
    model = DocumentType
    success_url = reverse_lazy('hrm:document_type_list')
    permission_required = 'Hrm.delete_documenttype'

class DocumentTypeExportView(BaseExportView):
    model = DocumentType
    permission_required = 'Hrm.view_documenttype'

class DocumentTypeBulkDeleteView(BaseBulkDeleteConfirmView):
    model = DocumentType
    success_url = reverse_lazy('hrm:document_type_list')
    permission_required = 'Hrm.delete_documenttype'

# ==================== EMPLOYEE DOCUMENT VIEWS ====================

class EmployeeDocumentListView(GenericFilterView):
    model = EmployeeDocument
    template_name = 'document/employee_document_list.html'
    context_object_name = 'objects'
    paginate_by = 10
    filter_form_class = EmployeeDocumentFilterForm
    permission_required = 'Hrm.view_employeedocument'
    
    def apply_filters(self, queryset):
        filters = self.filter_form.cleaned_data
        if filters.get('search'):
            queryset = queryset.filter(
                Q(employee__first_name__icontains=filters['search']) |
                Q(employee__last_name__icontains=filters['search']) |
                Q(document_name__icontains=filters['search']) |
                Q(document_number__icontains=filters['search'])
            )
        if filters.get('employee'):
            queryset = queryset.filter(employee=filters['employee'])
        if filters.get('document_type'):
            queryset = queryset.filter(document_type=filters['document_type'])
        if filters.get('status'):
            queryset = queryset.filter(status=filters['status'])
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('hrm:employee_document_create')
        context['can_create'] = self.request.user.has_perm('Hrm.add_employeedocument')
        context['can_view'] = self.request.user.has_perm('Hrm.view_employeedocument')
        context['can_update'] = self.request.user.has_perm('Hrm.change_employeedocument')
        context['can_delete'] = self.request.user.has_perm('Hrm.delete_employeedocument')
        return context

class EmployeeDocumentCreateView(PermissionRequiredMixin, CreateView):
    model = EmployeeDocument
    form_class = EmployeeDocumentForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.add_employeedocument'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Employee Document'
        context['subtitle'] = 'Upload employee document'
        context['cancel_url'] = reverse_lazy('hrm:employee_document_list')
        return context
    
    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, 'Employee Document created successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:employee_document_list')

class EmployeeDocumentUpdateView(PermissionRequiredMixin, UpdateView):
    model = EmployeeDocument
    form_class = EmployeeDocumentForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.change_employeedocument'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Employee Document'
        context['subtitle'] = f'Edit {self.object.document_name}'
        context['cancel_url'] = reverse_lazy('hrm:employee_document_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Employee Document updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:employee_document_list')

class EmployeeDocumentDeleteView(GenericDeleteView):
    model = EmployeeDocument
    success_url = reverse_lazy('hrm:employee_document_list')
    permission_required = 'Hrm.delete_employeedocument'

class EmployeeDocumentExportView(BaseExportView):
    model = EmployeeDocument
    permission_required = 'Hrm.view_employeedocument'

class EmployeeDocumentBulkDeleteView(BaseBulkDeleteConfirmView):
    model = EmployeeDocument
    success_url = reverse_lazy('hrm:employee_document_list')
    permission_required = 'Hrm.delete_employeedocument'

# ==================== FAMILY MEMBER VIEWS ====================

class FamilyMemberListView(GenericFilterView):
    model = FamilyMember
    template_name = 'family/family_member_list.html'
    context_object_name = 'objects'
    paginate_by = 10
    filter_form_class = FamilyMemberFilterForm
    permission_required = 'Hrm.view_familymember'
    
    def apply_filters(self, queryset):
        filters = self.filter_form.cleaned_data
        if filters.get('search'):
            queryset = queryset.filter(
                Q(employee__first_name__icontains=filters['search']) |
                Q(employee__last_name__icontains=filters['search']) |
                Q(name__icontains=filters['search'])
            )
        if filters.get('employee'):
            queryset = queryset.filter(employee=filters['employee'])
        if filters.get('relationship'):
            queryset = queryset.filter(relationship=filters['relationship'])
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('hrm:family_member_create')
        context['can_create'] = self.request.user.has_perm('Hrm.add_familymember')
        context['can_view'] = self.request.user.has_perm('Hrm.view_familymember')
        context['can_update'] = self.request.user.has_perm('Hrm.change_familymember')
        context['can_delete'] = self.request.user.has_perm('Hrm.delete_familymember')
        return context

class FamilyMemberCreateView(PermissionRequiredMixin, CreateView):
    model = FamilyMember
    form_class = FamilyMemberForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.add_familymember'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Family Member'
        context['subtitle'] = 'Add family member information'
        context['cancel_url'] = reverse_lazy('hrm:family_member_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Family Member created successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:family_member_list')

class FamilyMemberUpdateView(PermissionRequiredMixin, UpdateView):
    model = FamilyMember
    form_class = FamilyMemberForm
    template_name = 'common/premium-form.html'
    permission_required = 'Hrm.change_familymember'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Family Member'
        context['subtitle'] = f'Edit {self.object.name}'
        context['cancel_url'] = reverse_lazy('hrm:family_member_list')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Family Member updated successfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('hrm:family_member_list')

class FamilyMemberDeleteView(GenericDeleteView):
    model = FamilyMember
    success_url = reverse_lazy('hrm:family_member_list')
    permission_required = 'Hrm.delete_familymember'

class FamilyMemberExportView(BaseExportView):
    model = FamilyMember
    permission_required = 'Hrm.view_familymember'

class FamilyMemberBulkDeleteView(BaseBulkDeleteConfirmView):
    model = FamilyMember
    success_url = reverse_lazy('hrm:family_member_list')
    permission_required = 'Hrm.delete_familymember'
