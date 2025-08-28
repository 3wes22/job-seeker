from django.contrib import admin
from .models import Company, Job
# from .models import Company, Job, JobCategory, JobSkill, JobCategoryJob, JobSkillJob


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'size', 'location', 'is_verified', 'created_at')
    list_filter = ('industry', 'size', 'is_verified', 'created_at')
    search_fields = ('name', 'description', 'location')
    ordering = ('-created_at',)


# @admin.register(JobCategory)
# class JobCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'parent', 'created_at')
#     list_filter = ('parent', 'created_at')
#     search_fields = ('name', 'description')
#     ordering = ('name',)


# @admin.register(JobSkill)
# class JobSkillAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_at')
#     search_fields = ('name',)
#     ordering = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'employer_id', 'job_type', 'experience_level', 'location', 'created_at')
    list_filter = ('job_type', 'experience_level', 'is_remote', 'created_at')
    search_fields = ('title', 'description', 'requirements')
    ordering = ('-created_at',)


# @admin.register(JobCategoryJob)
# class JobCategoryJobAdmin(admin.ModelAdmin):
#     list_display = ('job', 'category')
#     list_filter = ('category',)
#     search_fields = ('job__title', 'category__name')


# @admin.register(JobSkillJob)
# class JobSkillJobAdmin(admin.ModelAdmin):
#     list_display = ('job', 'skill', 'is_required')
#     list_filter = ('is_required', 'skill')
#     search_fields = ('job__title', 'skill__name') 