from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random


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
            if int(seconds / 3600) == 1:
                return f"{int(seconds / 3600)} hour ago"
            elif seconds >= 3600:
                return f"{int(seconds / 3600)} hours ago"
            elif int(seconds / 60) == 1:
                return f"{int(seconds / 60)} minute ago"
            else:
                return f"{int(seconds / 60)} minutes ago"
        elif days == 1:
            return f"{days} day ago"
        else:
            return f"{days} days ago"


    def get_edits(self):
        return self.edit_set.all()


    def get_last_edit(self):
        edits = self.get_edits()

        #if edits:
        #    return edits.order_by('-creation_date')[0]

        #edits = self.get_edits()

        if edits:
            last_edit = edits[0]
            for edit in edits:
                if edit.creation_date > last_edit.creation_date:
                    last_edit = edit
            return last_edit


    def get_save_alert_id(self):
        return f'save_alert_{self.id}'


    def html_users_edits(self):
        d = {}
        edits = self.get_edits()
        if edits:
            for edit in edits:
                if edit.author not in d:
                    d[edit.author] = 1
                else:
                    d[edit.author] += 1
        return [f'{author} : {d[author]} upd' for author in d]


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
            if int(seconds/3600) == 1:
                return f"{int(seconds / 3600)} hour ago"
            elif seconds >= 3600:
                return f"{int(seconds/3600)} hours ago"
            elif int(seconds / 60) == 1:
                return f"{int(seconds / 60)} minute ago"
            else:
                return f"{int(seconds / 60)} minutes ago"
        elif days == 1:
            return f"{days} day ago"
        else:
            return f"{days} days ago"

    def get_position(self):
        edits = self.note.get_edits().order_by('-creation_date')

        if edits:
            i = 0
            for edit in edits:
                if edit.id == self.id:

                    row = i // 4
                    col = i % 4

                    xran = 5*random.random()
                    yran = 1 * random.random()

                    return f'left:{3 + col*23 + xran}%; ' \
                           f'top:{5 + row*2 + i*4 + yran}rem;'
                i += 1



