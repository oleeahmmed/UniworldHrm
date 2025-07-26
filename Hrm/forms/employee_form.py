from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from ..models import (
    Employee, Department, Designation, Shift, EducationLevel, 
    EducationQualification, JobExperience, DocumentType, 
    EmployeeDocument, FamilyMember
)
from config.forms import CustomTextarea, BaseFilterForm
import random
import string
from django.db.models import Max
from decimal import Decimal

# Define common CSS classes based on form-loop.html
COMMON_INPUT_CLASSES = "peer w-full px-3 py-2 rounded-md border-2 border-[hsl(var(--border))] bg-transparent premium-input text-[hsl(var(--foreground))] transition-all duration-200 focus:outline-none focus:border-[hsl(var(--primary))] focus:ring-1 focus:ring-[hsl(var(--primary))] focus:bg-[hsl(var(--accent))] placeholder-transparent"
FILE_INPUT_CLASSES = COMMON_INPUT_CLASSES + " file:bg-[hsl(var(--secondary))] file:text-[hsl(var(--secondary-foreground))] file:border-0 file:px-4 file:py-2 file:mr-4 file:rounded-md file:cursor-pointer file:hover:bg-[hsl(var(--accent))] file:transition-all"
CHECKBOX_INPUT_CLASSES = "sr-only peer" # For single checkbox/toggle
RADIO_INPUT_CLASSES = "appearance-none w-5 h-5 rounded-full border-2 border-[hsl(var(--border))] checked:border-[hsl(var(--primary))] relative cursor-pointer transition-all duration-200 after:content-[''] after:absolute after:opacity-0 after:w-2.5 after:h-2.5 after:bg-[hsl(var(--primary))] after:rounded-full after:top-1/2 after:left-1/2 after:-translate-x-1/2 after:-translate-y-1/2 checked:after:opacity-100"
CHECKBOX_MULTIPLE_INPUT_CLASSES = "appearance-none w-6 h-6 rounded-md border-2 border-[hsl(var(--border))] checked:bg-[hsl(var(--primary))] checked:border-[hsl(var(--primary))] relative cursor-pointer transition-all duration-200 after:content-[''] after:absolute after:opacity-0 after:w-1 after:h-2 after:border-r-2 after:border-b-2 after:border-[hsl(var(--primary-foreground))] after:rotate-45 after:top-1/2 after:left-1/2 after:-translate-y-[60%] after:-translate-x-1/2 checked:after:opacity-100 mr-3"


class EmployeeForm(forms.ModelForm):
    """Enhanced Employee form with comprehensive fields"""
    
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'marriage_date': forms.DateInput(attrs={'type': 'date'}),
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'confirmation_date': forms.DateInput(attrs={'type': 'date'}),
            'probation_end_date': forms.DateInput(attrs={'type': 'date'}),
            'contract_start_date': forms.DateInput(attrs={'type': 'date'}),
            'contract_end_date': forms.DateInput(attrs={'type': 'date'}),
            'termination_date': forms.DateInput(attrs={'type': 'date'}),
            # Mailing address can still be a textarea if it's manually entered
            'mailing_address': forms.Textarea(attrs={'rows': 3}), 
            'languages_spoken': forms.Textarea(attrs={'rows': 2}),
            'skills': forms.Textarea(attrs={'rows': 2}),
            'hobbies': forms.Textarea(attrs={'rows': 2}),
            'medical_conditions': forms.Textarea(attrs={'rows': 2}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'termination_reason': forms.Textarea(attrs={'rows': 3}),
        }

    fieldsets = [
        {
            'title': 'Basic Information',
            'description': 'Employee identification and basic details',
            'icon': 'user',
            'fields': ['employee_id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'national_id', 'phone', 'marital_status', 'nationality', 'religion', 'blood_group', 'department', 'designation', 'default_shift', 'joining_date', 'probation_end_date', 'expected_work_hours', 'overtime_grace_minutes', 'gross_salary', 'basic_salary', 'currency'],
        },
        # {
        #     'title': 'Identity Documents',
        #     'description': 'Official identification documents',
        #     'icon': 'credit-card',
        #     'fields': ['passport_number', 'driving_license', 'tax_id', 'social_security_number', 'card_no'],
        # },
        {
            'title': 'Personal Information',
            'description': 'Personal and family details',
            'icon': 'info',
            'fields': ['father_name', 'mother_name', 'spouse_name', 'place_of_birth',  'marriage_date', 'height', 'weight'],
        },
        {
            'title': 'Contact Information',
            'description': 'Communication details',
            'icon': 'phone',
            'fields': ['personal_email', 'mobile', 'home_phone', 'work_phone'],
        },
        # {
        #     'title': 'Emergency Contacts',
        #     'description': 'Emergency contact information',
        #     'icon': 'alert-triangle',
        #     'fields': ['emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship', 'emergency_contact_address', 'emergency_contact_2_name', 'emergency_contact_2_phone', 'emergency_contact_2_relationship'],
        # },
        {
            'title': 'Present Address',
            'description': 'Current residential address details (Bangladesh)',
            'icon': 'home',
            'fields': [
                'present_village_house', 'present_road_block', 'present_post_office',
                'present_police_station', 'present_district', 'present_division', 'present_postal_code_bd'
            ],
        },
        {
            'title': 'Permanent Address',
            'description': 'Permanent residential address details (Bangladesh)',
            'icon': 'home',
            'fields': [
                'permanent_village_house', 'permanent_road_block', 'permanent_post_office',
                'permanent_police_station', 'permanent_district', 'permanent_division', 'permanent_postal_code_bd'
            ],
        },
        # {
        #     'title': 'Mailing Address',
        #     'description': 'Address for official correspondence',
        #     'icon': 'mail',
        #     'fields': ['mailing_address'],
        # },
        {
            'title': 'Employment Details',
            'description': 'Job and employment information',
            'icon': 'briefcase',
            'fields': ['confirmation_date', 'contract_start_date', 'contract_end_date', 'employment_status', 'employment_type', 'employee_grade', 'employee_level', 'reporting_manager', 'work_location', 'termination_date', 'termination_reason'],
        },
        {
            'title': 'Salary & Banking',
            'description': 'Compensation and banking details',
            'icon': 'dollar-sign',
            'fields': ['bank_name', 'bank_branch', 'bank_account_number', 'bank_routing_number', 'bank_swift_code'],
        },
        # {
        #     'title': 'Additional Information',
        #     'description': 'Skills, languages, and other details',
        #     'icon': 'plus-circle',
        #     'fields': ['languages_spoken', 'skills', 'hobbies', 'medical_conditions', 'allergies'],
        # },
        # {
        #     'title': 'Profile & Status',
        #     'description': 'Profile picture and status',
        #     'icon': 'image',
        #     'fields': ['is_active', 'profile_picture', 'signature'],
        # },
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Auto-generate employee_id for new instances
        if not self.instance.pk:
            self.initial['employee_id'] = self.generate_unique_employee_id()
        
        # Apply styling to all fields
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.EmailInput, forms.URLInput, forms.TimeInput)):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, (forms.DateInput, forms.DateTimeInput)):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.CheckboxInput):
                # Check if it's a multiple choice checkbox or a single checkbox
                if isinstance(field.widget, forms.CheckboxSelectMultiple):
                    field.widget.attrs.update({'class': CHECKBOX_MULTIPLE_INPUT_CLASSES})
                else:
                    field.widget.attrs.update({'class': CHECKBOX_INPUT_CLASSES})
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': RADIO_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': FILE_INPUT_CLASSES})
            elif isinstance(field.widget, forms.ColorInput):
                # Color input has slightly different styling in form-loop.html
                field.widget.attrs.update({'class': "peer w-full h-10 px-1 py-1 rounded-md border-2 border-[hsl(var(--border))] bg-transparent text-[hsl(var(--foreground))] transition-all duration-200 focus:outline-none focus:border-[hsl(var(--primary))] focus:ring-1 focus:ring-[hsl(var(--primary))] cursor-pointer"})
            elif isinstance(field.widget, forms.RangeInput):
                # Range input has unique styling in form-loop.html
                field.widget.attrs.update({'class': "w-full h-2 bg-[hsl(var(--secondary))] rounded-full appearance-none cursor-pointer focus:outline-none [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-5 [&::-webkit-slider-thumb]:h-5 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-[hsl(var(--primary))] [&::-webkit-slider-thumb]:cursor-pointer [&::-webkit-slider-thumb]:transition-all [&::-webkit-slider-thumb]:duration-200 [&::-webkit-slider-thumb]:hover:scale-110"})


    def generate_unique_employee_id(self):
        """Generate unique employee ID"""
        prefix = "EMP"
        try:
            last_employee = Employee.objects.filter(
                employee_id__startswith=prefix
            ).aggregate(Max('employee_id'))['employee_id__max']
            
            if last_employee:
                try:
                    last_num = int(last_employee[len(prefix):])
                    new_num = last_num + 1
                    return f"{prefix}{new_num:04d}"
                except ValueError:
                    pass
        except Exception:
            pass
        
        # Fallback
        random_part = ''.join(random.choices(string.digits, k=4))
        return f"{prefix}{random_part}"

class EmployeeFilterForm(BaseFilterForm):
    """Filter form for Employee list"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by ID, name, email...', 'class': COMMON_INPUT_CLASSES})
    )
    
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label="All Departments",
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )
    
    designation = forms.ModelChoiceField(
        queryset=Designation.objects.all(),
        required=False,
        empty_label="All Designations",
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )
    
    employment_status = forms.ChoiceField(
        choices=(('', 'All Status'),) + Employee.EMPLOYMENT_STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )
    
    is_active = forms.ChoiceField(
        choices=[('', 'All'), ('true', 'Active'), ('false', 'Inactive')],
        required=False,
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )


class EducationLevelForm(forms.ModelForm):
    """Form for Education Level"""
    
    class Meta:
        model = EducationLevel
        fields = '__all__'

    # Removed fieldsets
    # fieldsets = [
    #     {
    #         'title': 'Basic Information',
    #         'description': 'Education level details',
    #         'icon': 'book',
    #         'fields': ['name', 'code', 'level', 'description'],
    #     },
    # ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput)):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})

class EducationLevelFilterForm(BaseFilterForm):
    """Filter form for Education Level list"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by name or code...', 'class': COMMON_INPUT_CLASSES})
    )

class EducationQualificationForm(forms.ModelForm):
    """Form for Education Qualification (Simplified)"""
    
    class Meta:
        model = EducationQualification
        fields = ['employee', 'education_level', 'institution_name', 'degree_title', 'graduation_date']
        widgets = {
            'graduation_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Removed fieldsets
    # fieldsets = [
    #     {
    #         'title': 'Education Details',
    #         'description': 'Key education qualification details',
    #         'icon': 'book',
    #         'fields': ['employee', 'education_level', 'institution_name', 'degree_title', 'graduation_date'],
    #     },
    # ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput)):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': FILE_INPUT_CLASSES})

class EducationQualificationFilterForm(BaseFilterForm):
    """Filter form for Education Qualifications"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by employee, degree, institution...', 'class': COMMON_INPUT_CLASSES})
    )
    
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        required=False,
        empty_label="All Employees",
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )
    
    education_level = forms.ModelChoiceField(
        queryset=EducationLevel.objects.all(),
        required=False,
        empty_label="All Education Levels",
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )

class JobExperienceForm(forms.ModelForm):
    """Form for Job Experience (Simplified)"""
    
    class Meta:
        model = JobExperience
        fields = ['employee', 'company_name', 'job_title', 'start_date', 'end_date', 'employment_type'] # Added employment_type back
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Removed fieldsets
    # fieldsets = [
    #     {
    #         'title': 'Job Experience Details',
    #         'description': 'Key details of previous job experience',
    #         'icon': 'briefcase',
    #         'fields': ['employee', 'company_name', 'job_title', 'start_date', 'end_date', 'employment_type'], # Added employment_type back
    #     },
    # ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.EmailInput)):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.CheckboxInput):
                if isinstance(field.widget, forms.CheckboxSelectMultiple):
                    field.widget.attrs.update({'class': CHECKBOX_MULTIPLE_INPUT_CLASSES})
                else:
                    field.widget.attrs.update({'class': CHECKBOX_INPUT_CLASSES})
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': RADIO_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': FILE_INPUT_CLASSES})

class JobExperienceFilterForm(BaseFilterForm):
    """Filter form for Job Experience"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by employee, company, job title...', 'class': COMMON_INPUT_CLASSES})
    )
    
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        required=False,
        empty_label="All Employees",
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )
    # Re-added employment_type to filter form now that it's nullable in the model
    employment_type = forms.ChoiceField(
        required=False,
        choices=(('', 'All Types'),) + JobExperience.EMPLOYMENT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )

class DocumentTypeForm(forms.ModelForm):
    """Form for Document Type (Simplified)"""
    
    class Meta:
        model = DocumentType
        fields = ['name', 'code', 'description'] # Simplified fields

    # Removed fieldsets
    # fieldsets = [
    #     {
    #         'title': 'Basic Information',
    #         'description': 'Document type details',
    #         'icon': 'file',
    #         'fields': ['name', 'code', 'description'], # Simplified fields
    #     },
    # ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput)):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.CheckboxInput):
                if isinstance(field.widget, forms.CheckboxSelectMultiple):
                    field.widget.attrs.update({'class': CHECKBOX_MULTIPLE_INPUT_CLASSES})
                else:
                    field.widget.attrs.update({'class': CHECKBOX_INPUT_CLASSES})
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': RADIO_INPUT_CLASSES})


class DocumentTypeFilterForm(BaseFilterForm):
    """Filter form for Document Type list (Simplified)"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by name or code...', 'class': COMMON_INPUT_CLASSES})
    )

class EmployeeDocumentForm(forms.ModelForm):
    """Form for Employee Document (Simplified)"""
    
    class Meta:
        model = EmployeeDocument
        fields = ['employee', 'document_type', 'document_name', 'document_file', 'status'] # Simplified fields
        widgets = {
            # Removed issue_date, expiry_date, approval_date as they are no longer in the model
            'description': forms.Textarea(attrs={'rows': 3}), # Kept for potential future use or if needed elsewhere
            'notes': forms.Textarea(attrs={'rows': 2}), # Kept for potential future use or if needed elsewhere
            'rejection_reason': forms.Textarea(attrs={'rows': 2}), # Kept for potential future use or if needed elsewhere
        }

    # Removed fieldsets
    # fieldsets = [
    #     {
    #         'title': 'Document Information',
    #         'description': 'Basic document details',
    #         'icon': 'file',
    #         'fields': ['employee', 'document_type', 'document_name'], # Simplified fields
    #     },
    #     {
    #         'title': 'File & Status',
    #         'description': 'Upload document and current status',
    #         'icon': 'upload',
    #         'fields': ['document_file', 'status'], # Simplified fields
    #     },
    #     # Removed Dates & Status, Approval Information fieldsets
    # ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput)):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, (forms.DateInput, forms.DateTimeInput)):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.CheckboxInput):
                if isinstance(field.widget, forms.CheckboxSelectMultiple):
                    field.widget.attrs.update({'class': CHECKBOX_MULTIPLE_INPUT_CLASSES})
                else:
                    field.widget.attrs.update({'class': CHECKBOX_INPUT_CLASSES})
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': RADIO_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': FILE_INPUT_CLASSES})

class EmployeeDocumentFilterForm(BaseFilterForm):
    """Filter form for Employee Documents (Simplified)"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by employee, document name...', 'class': COMMON_INPUT_CLASSES})
    )
    
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        required=False,
        empty_label="All Employees",
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )
    
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        required=False,
        empty_label="All Document Types",
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=(('', 'All Status'),) + EmployeeDocument.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )

class FamilyMemberForm(forms.ModelForm):
    """Form for Family Member"""
    
    class Meta:
        model = FamilyMember
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    # Removed fieldsets
    # fieldsets = [
    #     {
    #         'title': 'Basic Information',
    #         'description': 'Family member details',
    #         'icon': 'user',
    #         'fields': ['employee', 'name', 'relationship', 'date_of_birth', 'gender'],
    #     },
    #     {
    #         'title': 'Contact Information',
    #         'description': 'Contact details',
    #         'icon': 'phone',
    #         'fields': ['phone', 'email', 'address'],
    #     },
    #     {
    #         'title': 'Professional Information',
    #         'description': 'Work and employment details',
    #         'icon': 'briefcase',
    #         'fields': ['occupation', 'employer'],
    #     },
    #     {
    #         'title': 'Relationship Status',
    #         'description': 'Dependency and contact preferences',
    #         'icon': 'heart',
    #         'fields': ['is_dependent', 'is_emergency_contact', 'is_nominee'],
    #     },
    #     {
    #         'title': 'Documents',
    #         'description': 'Photo and identification documents',
    #         'icon': 'image',
    #         'fields': ['photo', 'id_document'],
    #     },
    # ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.CheckboxInput):
                if isinstance(field.widget, forms.CheckboxSelectMultiple):
                    field.widget.attrs.update({'class': CHECKBOX_MULTIPLE_INPUT_CLASSES})
                else:
                    field.widget.attrs.update({'class': CHECKBOX_INPUT_CLASSES})
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({'class': RADIO_INPUT_CLASSES})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': COMMON_INPUT_CLASSES})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': FILE_INPUT_CLASSES})

class FamilyMemberFilterForm(BaseFilterForm):
    """Filter form for Family Members"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by employee or family member name...', 'class': COMMON_INPUT_CLASSES})
    )
    
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        required=False,
        empty_label="All Employees",
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )
    
    relationship = forms.ChoiceField(
        required=False,
        choices=(('', 'All Relationships'),) + FamilyMember.RELATIONSHIP_CHOICES,
        widget=forms.Select(attrs={'class': COMMON_INPUT_CLASSES})
    )
