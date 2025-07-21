from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer
from rest_framework import viewsets

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # Custom action to return only adult students
    @action(detail=False, methods=['get'])
    def adults(self, request):
        adult_students = Student.objects.adults()
        serializer = StudentSerializer(adult_students, many=True)
        return Response(serializer.data)
