from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'], url_path='all-students')
    def all_students(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def filter_age(self, request):
        students = Student.objects.filter(age=14)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def exclude_age(self, request):
        students = Student.objects.exclude(age=18)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def order_by_age(self, request):
        students = Student.objects.order_by('age')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def order_by_age_desc(self, request):
        students = Student.objects.order_by('-age')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def first_student(self, request):
        student = Student.objects.first()
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def last_student(self, request):
        student = Student.objects.last()
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def values_demo(self, request):
        data = list(Student.objects.values('name', 'age'))
        return Response(data)

    @action(detail=False, methods=['get'])
    def count_students(self, request):
        total = Student.objects.count()
        return Response({"count": total})

    @action(detail=False, methods=['get'])
    def exists_age_20(self, request):
        exists = Student.objects.filter(age=20).exists()
        return Response({"exists": exists})

    @action(detail=False, methods=['get'])
    def distinct_ages(self, request):
        data = list(Student.objects.values('age').distinct())
        return Response(data)

    @action(detail=False, methods=['get'])
    def filtered_ordered(self, request):
        students = Student.objects.filter(age__gte=18).order_by('name')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
