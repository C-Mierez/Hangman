from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        return redirect(
            '/game/%s'
            %room_name
        )
    return render(request, 'index.html', {})

# @login_required
def room(request, room_name):
    if not request.user.is_authenticated:
        #create anonymous user
        request.session.save()
    return render(request, 'hangedman.html', {
        'room_name': room_name
    })