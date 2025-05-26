from django.core.management.base import BaseCommand
from core.models import Plan


class Command(BaseCommand):
    help = 'Create initial subscription plans'

    def handle(self, *args, **options):
        plans_data = [
            {
                'name': 'basic',
                'price': 9.99,
                'features': {
                    'users': 1,
                    'storage_gb': 10,
                    'support': 'email',
                    'features': ['Basic Dashboard', 'Email Support']
                }
            },
            {
                'name': 'pro',
                'price': 29.99,
                'features': {
                    'users': 10,
                    'storage_gb': 100,
                    'support': 'priority',
                    'features': ['Advanced Dashboard', 'Priority Support',
                                 'API Access']
                }
            },
            {
                'name': 'enterprise',
                'price': 99.99,
                'features': {
                    'users': 'unlimited',
                    'storage_gb': 1000,
                    'support': '24/7',
                    'features': ['Custom Dashboard', '24/7 Support',
                                 'Full API Access', 'Custom Integrations']
                }
            }
        ]

        for plan_data in plans_data:
            plan, created = Plan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created plan: {plan.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Plan already exists: {plan.name}')
                )
