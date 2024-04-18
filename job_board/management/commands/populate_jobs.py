from django.core.management.base import BaseCommand
from job_board.models import Job


class Command(BaseCommand):
    help = 'Populate demo data for jobs'

    def handle(self, *args, **options):
        jobs_data = [
            {
                'company': 'DoctusTech',
                'title': 'Software Engineer',
                'description': 'Develop software applications',
                'location': 'New York',
                'experience': 3,
                'applicants': []
            },
            {
                'company': 'Dell',
                'title': 'Data Scientist',
                'description': 'Analyze data and build predictive models',
                'location': 'San Francisco',
                'experience': 5,
                'applicants': []
            },
            {
                'company': 'Quark',
                'title': 'UI/UX Designer',
                'description': 'Design user interfaces for web and mobile apps',
                'location': 'London',
                'experience': 2,
                'applicants': []

            },
        ]

        for job_data in jobs_data:
            Job.objects.create(**job_data)

        self.stdout.write(self.style.SUCCESS('Demo data created successfully'))
