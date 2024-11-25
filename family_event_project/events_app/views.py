from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Event
from .serializers import EventSerializer

class CreateEventView(APIView):
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditEventView(APIView):
    def put(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteEventView(APIView):
    def delete(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": "Event does not exist"}, status=status.HTTP_404_NOT_FOUND)
        event.delete()
        return Response({"deleted":"true"} , status=status.HTTP_204_NO_CONTENT)

class JoinEventView(APIView):
    def post(self, request):
        # Логика присоединения к событию
        return Response({"message": "Joined event"}, status=status.HTTP_200_OK)

class UnjoinEventView(APIView):
    def post(self, request):
        # Логика отсоединения от события
        return Response({"message": "Unjoined event"}, status=status.HTTP_200_OK)

class ListEventsView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
