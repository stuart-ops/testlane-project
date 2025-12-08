from django.db import models
from django.contrib.auth.models import User


class BrandTrackingCategory(models.Model):
    """Model to store question categories for brand tracking"""
    category_key = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Brand Tracking Category'
        verbose_name_plural = 'Brand Tracking Categories'
        ordering = ['order', 'display_name']
    
    def __str__(self):
        return self.display_name


class BrandTrackingQuestion(models.Model):
    """Model to store individual brand tracking scoring questions"""
    category = models.ForeignKey(BrandTrackingCategory, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Brand Tracking Question'
        verbose_name_plural = 'Brand Tracking Questions'
        ordering = ['category__order', 'order', 'id']
        unique_together = [['category', 'order']]
    
    def __str__(self):
        return f"{self.category.display_name} - Q{self.order}: {self.question_text[:50]}..."
    
    @property
    def global_question_number(self):
        """Calculate the global question number (1-10) based on category and order"""
        categories = BrandTrackingCategory.objects.all().order_by('order', 'display_name')
        question_number = 0
        
        for cat in categories:
            if cat.id == self.category.id:
                questions_in_category = self.category.questions.filter(
                    is_active=True, order__lt=self.order
                ).count()
                question_number += questions_in_category + 1
                break
            else:
                question_number += cat.questions.filter(is_active=True).count()
        
        return question_number


class BrandTrackingScore(models.Model):
    """Model to store brand tracking scoring results"""
    article_text = models.TextField()
    total_score = models.IntegerField(default=0)  # Out of 100 (10 questions × 10 max points)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    population_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('running', 'Running'), ('done', 'Done'), ('failed', 'Failed')],
        default='pending'
    )
    processed_questions = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Brand Tracking Score: {self.total_score}/100 - {self.created_at.strftime('%Y-%m-%d')}"
    
    @property
    def score_percentage(self):
        return round((self.total_score / 100) * 100, 1)
    
    def get_ordered_categories(self):
        """Get category scores in the admin-defined order with ordered questions"""
        admin_categories = BrandTrackingCategory.objects.all().order_by('order', 'display_name')
        category_order = [cat.category_key for cat in admin_categories]
        
        categories = self.category_scores.all()
        categories_dict = {cat.category_name: cat for cat in categories}
        
        return [categories_dict[cat_name] for cat_name in category_order if cat_name in categories_dict]


class BrandTrackingCategoryScore(models.Model):
    """Model to store category-wise scores"""
    brand_tracking_score = models.ForeignKey(BrandTrackingScore, on_delete=models.CASCADE, related_name='category_scores')
    category_name = models.CharField(max_length=50)
    category_display_name = models.CharField(max_length=100)
    score = models.IntegerField(default=0)  # Variable max based on questions per category
    
    def __str__(self):
        return f"{self.category_display_name}: {self.score}"
    
    @property
    def max_score(self):
        """Calculate max score based on number of questions in this category (each worth 10 points)"""
        return self.question_scores.count() * 10
    
    @property
    def score_percentage(self):
        max_score = self.max_score
        if max_score == 0:
            return 0
        return round((self.score / max_score) * 100, 1)


class BrandTrackingQuestionScore(models.Model):
    """Model to store individual question scores"""
    category_score = models.ForeignKey(BrandTrackingCategoryScore, on_delete=models.CASCADE, related_name='question_scores')
    question_text = models.TextField()
    question_number = models.IntegerField()  # 1-10
    score = models.IntegerField(blank=True, null=True)  # 1-10, can be null until completed
    semilattice_answer_id = models.CharField(max_length=255, blank=True, null=True)
    raw_response = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"Q{self.question_number}: {self.score}/10"
    
    class Meta:
        ordering = ['question_number']
