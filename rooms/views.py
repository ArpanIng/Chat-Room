from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddRoomModelForm
from .models import Topic, Room, Message


def homepage_view(request):

    if request.GET.get("q") == None:  # No query '?q=' parameter
        q = ""
    else:
        q = request.GET.get("q")

    # user can search room by topic name, room name and room description
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(description__icontains=q),
    )
    # filters room messages according to topics
    room_messages = Message.objects.filter(room__topic__name__icontains=q)

    context = {
        "rooms": rooms,
        "topics": Topic.objects.all()[:4],  # limit topic in homepage
        "rooms_count": rooms.count(),
        "room_messages": room_messages,
    }

    return render(request, "rooms/homepage.html", context)


@login_required
def room_create_view(request):

    room_operation = "create"
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        # user can create topic
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),  # name -> form.name
            description=request.POST.get("description"),
        )
        return redirect("rooms:homepage")
    else:
        form = AddRoomModelForm()

    context = {
        "form": form,
        "room_operation": room_operation,
        "topics": topics,
    }

    return render(request, "rooms/room_form.html", context)


def room_detail_view(request, pk):

    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST":
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get("body"),
        )
        room.participants.add(request.user)
        return redirect("rooms:room_detail", room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }

    return render(request, "rooms/room_detail.html", context)


@login_required
def room_update_view(request, pk):

    room = get_object_or_404(Room, id=pk)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("Not ALLOWED!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic  # user can either update or create new topic
        room.name = request.POST.get("name")
        room.description = request.POST.get("description")
        room.save()
        return redirect("rooms:room_detail", room.id)
    else:
        form = AddRoomModelForm(instance=room)

    context = {
        "room": room,
        "form": form,
        "topics": topics,
    }

    return render(request, "rooms/room_form.html", context)


@login_required
def room_delete_view(request, pk):

    room_operation = "room_delete"
    room = get_object_or_404(Room, id=pk)

    if request.user != room.host:
        return HttpResponse("Not ALLOWED!")

    if request.method == "POST":
        room.delete()
        return redirect("rooms:homepage")

    context = {
        "room": room,
        "room_operation": room_operation,
    }

    return render(request, "rooms/delete_confirm.html", context)


@login_required
def message_delete_view(request, pk):

    message = get_object_or_404(Message, id=pk)

    if request.user != message.user:
        return HttpResponse("Not ALLOWED!")

    if request.method == "POST":
        message.delete()
        return redirect("rooms:homepage")

    context = {
        "message": message,
    }

    return render(request, "rooms/delete_confirm.html", context)


def topics_view(request):

    if request.GET.get("q") == None:  # No query '?q=' parameter
        q = ""
    else:
        q = request.GET.get("q")

    topics = Topic.objects.filter(name__icontains=q)

    context = {
        "topics": topics,
    }
    return render(request, "topics.html", context)


def activities_view(request):

    room_messages = Message.objects.all()

    context = {
        "room_messages": room_messages,
    }
    return render(request, "activities.html", context)
