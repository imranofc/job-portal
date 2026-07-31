from django.db import models

class Profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=50, choices=[('job_seeker', 'Job Seeker'), ('employer', 'Employer')], default='job_seeker')

    def __str__(self):
        return self.user.username

class JobType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

APPLY_TYPES = [
    ('resume', 'Resume'),
    ('link', 'Link'),
]

class Job(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    posted_date = models.DateTimeField(auto_now_add=True)
    apply_type = models.CharField(max_length=10, choices=APPLY_TYPES, default='resume')
    apply_link = models.CharField(max_length=500, null=True)
    def __str__(self):
        return self.title