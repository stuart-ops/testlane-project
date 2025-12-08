from django.core.management.base import BaseCommand
from brand_tracking.models import BrandTrackingCategory, BrandTrackingQuestion
from brand_tracking.constants import BRAND_TRACKING_QUESTIONS


class Command(BaseCommand):
    help = 'Seeds the brand tracking questions from constants into the database'

    def handle(self, *args, **options):
        self.stdout.write('Seeding brand tracking questions...')
        
        # Clear existing data if needed (optional - comment out to preserve)
        # BrandTrackingQuestion.objects.all().delete()
        # BrandTrackingCategory.objects.all().delete()
        
        for category_key, category_data in BRAND_TRACKING_QUESTIONS.items():
            # Create or get category
            category, created = BrandTrackingCategory.objects.get_or_create(
                category_key=category_key,
                defaults={
                    'display_name': category_data['display_name'],
                    'order': category_data['order'],
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.display_name}'))
            else:
                # Update order and display name if changed
                category.display_name = category_data['display_name']
                category.order = category_data['order']
                category.save()
                self.stdout.write(f'Updated category: {category.display_name}')
            
            # Create questions for this category
            for order, question_text in enumerate(category_data['questions'], start=1):
                question, created = BrandTrackingQuestion.objects.get_or_create(
                    category=category,
                    order=order,
                    defaults={
                        'question_text': question_text,
                        'is_active': True,
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  Created Q{order}: {question_text[:60]}...'))
                else:
                    # Update question text if changed
                    if question.question_text != question_text:
                        question.question_text = question_text
                        question.save()
                        self.stdout.write(f'  Updated Q{order}: {question_text[:60]}...')
                    else:
                        self.stdout.write(f'  Q{order} already exists')
        
        # Display summary
        total_categories = BrandTrackingCategory.objects.count()
        total_questions = BrandTrackingQuestion.objects.filter(is_active=True).count()
        
        self.stdout.write(self.style.SUCCESS(f'\nSeeding complete!'))
        self.stdout.write(f'Total categories: {total_categories}')
        self.stdout.write(f'Total active questions: {total_questions}')
