from django.db import models

class Task(models.Model):
    task_id=models.AutoField(primary_key=True)
    task_title=models.CharField(max_length=50,null=False)
    task_discription=models.TextField(null=True)
    task_status = models.BooleanField(default=False)
    task_created_date = models.DateTimeField(auto_now_add=True)
    task_due_date=models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


