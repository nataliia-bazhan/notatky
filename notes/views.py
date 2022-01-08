from django.shortcuts import render
from .models import Edit, Note
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# get all notes
def all_notes(request):
    context = {'notes': Note.objects.all(),
               'user': request.user,
               'only_user': False,}
    return render(request, "all_notes.html", context)


# get only user notes
@login_required
def user_notes(request):
    context = {'notes': Note.objects.all(),
               'user': request.user,
               'only_user': True}
    return render(request, "all_notes.html", context)


@login_required
def create_note(request):
    if is_ajax(request) and request.method == "POST":

        note = Note(author=User.objects.get(username=request.user))
        note.save()

        # return the note.id to JS
        response = {
            'id': note.id
        }

        return JsonResponse(response)


@login_required
def update_note(request):
    if is_ajax(request) and request.method == "POST":

        # collect data
        id = request.POST['id']
        title, content = request.POST['title'], request.POST['content']
        left, top = request.POST['left'], request.POST['top']

        # update note
        note = Note.objects.get(id=id)

        if note.title == title and note.content == content:
            return JsonResponse({'saved': False, 'message': f'note {id} wasn\'t changed'})
        else:
            note.title, note.content = title, content
            note.left, note.top = left, top
            note.save()

        # create edit instance
        edit = Edit(author=User.objects.get(username=request.user),
                    title=title,
                    content=content,
                    note=note)
        edit.save()

        return JsonResponse({'saved': True, 'message': f'note {id} successfully updated'})


@login_required
def delete_note(request):
    if is_ajax(request) and request.method == "POST":

        id = request.POST['id']
        note = Note.objects.get(id=id)
        note.delete()

        return JsonResponse({'message': f'note {id} successfully deleted'})


@login_required
def details_note(request, pk):
    note = Note.objects.get(id=pk)
    edits = note.get_edits()
    context = {
        "edits": edits,
        "note": note
    }
    return render(request, "details_note.html", context)


