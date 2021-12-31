from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Note(models.Model):
    title = models.CharField(max_length=300, default='')
    content = models.TextField(default='')

    # store note position
    left = models.CharField(max_length=7, default='35vw')
    top = models.CharField(max_length=7, default='37h')

    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title


    def get_title_id(self):
        return f'title_{self.id}'


    def get_content_id(self):
        return f'content_{self.id}'


    def get_footer_id(self):
        return f'footer_{self.id}'


    def when_published(self):
        now = timezone.now()
        since = now - self.creation_date
        days = since.days
        seconds = since.seconds

        if days == 0:
            if seconds >= 3600:
                return f"{int(seconds/3600)} hours ago"
            else:
                return f"{int(seconds / 60)} minutes ago"
        else:
            return f"{days} days ago"


    def get_edits(self):
        return self.edit_set.all()


    def get_last_edit(self):
        edits = self.get_edits()

        if edits:
            last_edit = edits[0]
            for edit in edits:
                if edit.creation_date > last_edit.creation_date:
                    last_edit = edit
            return last_edit


class Edit(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)

    def when_published(self):
        now = timezone.now()
        since = now - self.creation_date
        days = since.days
        seconds = since.seconds

        if days == 0:
            if seconds >= 3600:
                return f"{int(seconds/3600)} hours ago"
            else:
                return f"{int(seconds / 60)} minutes ago"
        else:
            return f"{days} days ago"