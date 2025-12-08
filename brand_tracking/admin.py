from django.contrib import admin
from .models import (
    BrandTrackingScore, BrandTrackingCategoryScore, BrandTrackingQuestionScore,
    BrandTrackingCategory, BrandTrackingQuestion
)


class SuperuserOnlyAdminMixin:
    """Mixin to restrict admin access to superusers only"""
    
    def has_module_permission(self, request):
        return request.user.is_superuser
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


class BrandTrackingQuestionInline(admin.TabularInline):
    model = BrandTrackingQuestion
    extra = 1
    fields = ['question_text', 'order', 'is_active']
    ordering = ['order']


@admin.register(BrandTrackingCategory)
class BrandTrackingCategoryAdmin(SuperuserOnlyAdminMixin, admin.ModelAdmin):
    list_display = ['display_name', 'category_key', 'order', 'question_count', 'updated_at']
    list_editable = ['order']
    search_fields = ['display_name', 'category_key']
    ordering = ['order', 'display_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [BrandTrackingQuestionInline]
    
    def question_count(self, obj):
        return obj.questions.filter(is_active=True).count()
    question_count.short_description = 'Active Questions'


@admin.register(BrandTrackingQuestion)
class BrandTrackingQuestionAdmin(SuperuserOnlyAdminMixin, admin.ModelAdmin):
    list_display = ['global_question_number', 'category', 'order', 'question_preview', 'is_active', 'updated_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question_text', 'category__display_name']
    list_editable = ['order', 'is_active']
    ordering = ['category__order', 'order']
    readonly_fields = ['created_at', 'updated_at', 'global_question_number']
    
    fieldsets = (
        (None, {
            'fields': ('category', 'question_text', 'order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('global_question_number', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        return obj.question_text[:80] + "..." if len(obj.question_text) > 80 else obj.question_text
    question_preview.short_description = 'Question Preview'


@admin.register(BrandTrackingScore)
class BrandTrackingScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'total_score', 'score_percentage', 'created_by', 'created_at']
    list_filter = ['created_at', 'created_by']
    search_fields = ['article_text', 'created_by__username']
    readonly_fields = ['created_at']
    
    def score_percentage(self, obj):
        return f"{obj.score_percentage}%"
    score_percentage.short_description = 'Score %'


@admin.register(BrandTrackingCategoryScore)
class BrandTrackingCategoryScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_display_name', 'score', 'score_percentage', 'brand_tracking_score']
    list_filter = ['category_name', 'brand_tracking_score__created_at']
    search_fields = ['category_display_name', 'brand_tracking_score__article_text']
    
    def score_percentage(self, obj):
        return f"{obj.score_percentage}%"
    score_percentage.short_description = 'Score %'


@admin.register(BrandTrackingQuestionScore)
class BrandTrackingQuestionScoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_number', 'score', 'category_score', 'question_text_short']
    list_filter = ['score', 'category_score__category_name']
    search_fields = ['question_text']
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'
