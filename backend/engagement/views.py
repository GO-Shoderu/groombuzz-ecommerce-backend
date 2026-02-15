from rest_framework import viewsets, permissions
from .models import Review, Message
from .serializers import ReviewSerializer, MessageSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("booking", "business", "client").all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related("sender", "recipient", "business").all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
