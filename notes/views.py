from django.shortcuts import render
from .models import Edit, Note
from django.http import JsonResponse
from django.contrib.auth.models import User

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# get all notes
def all_notes(request):
    context = {'notes': Note.objects.all(),
               'user': request.user,
               'only_user': False}
    return render(request, "all_notes.html", context)


# get only user notes
def user_notes(request):
    context = {'notes': Note.objects.all(),
               'user': request.user,
               'only_user': True}
    return render(request, "all_notes.html", context)


def create_note(request):
    if is_ajax(request) and request.method == "POST":

        note = Note(author=User.objects.get(username=request.user))
        note.save()
        response = {
            'id': note.id
        }

        return JsonResponse(response)


def update_note(request):
    if is_ajax(request) and request.method == "POST":

        # collect data
        id = request.POST['id']
        title, content = request.POST['title'], request.POST['content']
        left, top = request.POST['left'], request.POST['top']

        # update note
        note = Note.objects.get(id=id)
        note.title, note.content = title, content
        note.left, note.top = left, top
        note.save()

        # create edit instance
        edit = Edit(author=User.objects.get(username=request.user),
                    title=title,
                    content=content,
                    note=note)
        edit.save()

        return JsonResponse({'message': f'note {id} successfully updated'})


def delete_note(request):
    if is_ajax(request) and request.method == "POST":

        id = request.POST['id']
        note = Note.objects.get(id=id)
        note.delete()

        return JsonResponse({'message': f'note {id} successfully deleted'})


def details_note(request, pk):
    note = Note.objects.get(id=pk)
    edits = note.get_edits()
    context = {
        "edits": edits,
        "note": note
    }
    return render(request, "details_note.html", context)


