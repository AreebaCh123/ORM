# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from django.db.models import Count
from .models import Student, Course
from .models import Course as CourseModel  # for explain()
from .serializers import CourseSerializer

class ORMOperationsView(APIView):
    def get(self, request):
        output = {}

        # CREATE
        student1 = Student.objects.create(name="Areeba")
        course1 = Course.objects.create(title="Python Course")
        course1.students.add(student1)
        output["create"] = {"student": student1.name, "course": course1.title}

        # GET
        try:
            course = Course.objects.get(id=course1.id)
            output["get"] = course.title
        except Course.DoesNotExist:
            output["get"] = "Course not found"

        # GET_OR_CREATE
        student2, created = Student.objects.get_or_create(name="Ali")
        output["get_or_create"] = {"student": student2.name, "created": created}

        # UPDATE_OR_CREATE
        course2, created = Course.objects.update_or_create(
            id=course1.id,
            defaults={"title": "Updated Python Course"}
        )
        output["update_or_create"] = {"course": course2.title, "created": created}

        # BULK_CREATE
        new_courses = Course.objects.bulk_create([
            Course(title="Django"),
            Course(title="DRF")
        ])
        output["bulk_create"] = [c.title for c in new_courses]

        # BULK_UPDATE
        for c in new_courses:
            c.title += " Advanced"
        Course.objects.bulk_update(new_courses, ['title'])
        output["bulk_update"] = [c.title for c in new_courses]

        # COUNT
        output["count"] = Course.objects.count()

        # IN_BULK
        ids = Course.objects.values_list('id', flat=True)
        in_bulk_courses = Course.objects.in_bulk(ids)
        output["in_bulk"] = {str(k): v.title for k, v in in_bulk_courses.items()}

        # ITERATOR
        output["iterator"] = [c.title for c in Course.objects.iterator()]

        # LATEST / EARLIEST
        try:
            output["latest"] = Course.objects.latest('id').title
            output["earliest"] = Course.objects.earliest('id').title
        except Course.DoesNotExist:
            output["latest"] = output["earliest"] = "No courses"

        # FIRST / LAST
        first = Course.objects.first()
        last = Course.objects.last()
        output["first"] = first.title if first else None
        output["last"] = last.title if last else None

        # AGGREGATE
        # output["aggregate"] = Course.objects.aggregate(total_courses=Count('id'))

        # EXISTS
        output["exists"] = Course.objects.exists()

        # UPDATE
        updated_count = Course.objects.filter(title__icontains="Python").update(title="Updated Title")
        output["update"] = f"{updated_count} course(s) updated"

        # DELETE
        deleted_count, _ = Course.objects.filter(title__icontains="DRF").delete()
        output["delete"] = f"{deleted_count} course(s) deleted"

        # EXPLAIN
        output["explain"] = CourseModel.objects.filter(title__icontains="Python").explain()

        # FILTER - Get all courses with "Advanced" in the title
        filtered_courses = Course.objects.filter(title__icontains="Advanced")
        output["filter"] = [course.title for course in filtered_courses]

        # EXCLUDE - Get all courses that do NOT contain "Advanced" in the title
        excluded_courses = Course.objects.exclude(title__icontains="Advanced")
        output["exclude"] = [course.title for course in excluded_courses]

        from django.db.models import Count

        # ANNOTATE - Count number of students per course
        courses_with_student_count = Course.objects.annotate(student_count=Count('students'))
        output["annotate"] = [
            {"course": course.title, "student_count": course.student_count}
            for course in courses_with_student_count
        ]

        # ORDER_BY - Sort all courses by title alphabetically
        ordered_courses = Course.objects.order_by('title')
        output["order_by"] = [course.title for course in ordered_courses]


        # REVERSE - First order by title A–Z, then reverse to Z–A
        reversed_courses = Course.objects.order_by('title').reverse()
        output["reverse"] = [course.title for course in reversed_courses]

        # DISTINCT - Get unique course titles
        distinct_titles = Course.objects.values_list('title', flat=True).distinct()
        output["distinct"] = list(distinct_titles)

        # VALUES - Get course IDs and titles as dictionaries
        course_values = Course.objects.values('id', 'title')
        output["values"] = list(course_values)

        # VALUES_LIST - Get only course titles as a flat list
        course_titles = Course.objects.values_list('title', flat=True)
        output["values_list"] = list(course_titles)

        # NONE - Return an empty queryset
        empty_qs = Course.objects.none()
        output["none"] = list(empty_qs)  # Will be an empty list

        # ALL - Get all course objects
        all_courses = Course.objects.all()
        output["all"] = [course.title for course in all_courses]

        # UNION - Combine two querysets and remove duplicates
        qs1 = Course.objects.filter(title__icontains='Python').values_list('title', flat=True)
        qs2 = Course.objects.filter(title__icontains='Django').values_list('title', flat=True)
        union_qs = qs1.union(qs2)
        output["union"] = list(union_qs)

        # INTERSECTION - Common results between two querysets
        qs1 = Course.objects.filter(title__icontains='Advanced').values_list('title', flat=True)
        qs2 = Course.objects.filter(title__icontains='Django').values_list('title', flat=True)
        intersection_qs = qs1.intersection(qs2)
        output["intersection"] = list(intersection_qs)

        # DIFFERENCE - Items in qs1 but not in qs2
        qs1 = Course.objects.filter(title__icontains='Python').values_list('title', flat=True)
        qs2 = Course.objects.filter(title__icontains='Django').values_list('title', flat=True)
        difference_qs = qs1.difference(qs2)
        output["difference"] = list(difference_qs)

                # DEFER - Delay loading of 'title' field
        deferred_courses = Course.objects.defer('title')
        output["defer"] = [course.id for course in deferred_courses]  # title not fetched yet

        # ONLY - Load only the 'title' field
        only_courses = Course.objects.only('title')
        output["only"] = [course.title for course in only_courses]

                # USING - Use a different database
        used_courses = Course.objects.using('default').all()
        output["using"] = [course.title for course in used_courses]

                # RAW - Run a raw SQL query
        raw_courses = Course.objects.raw('SELECT * FROM app_course')
        output["raw"] = [course.title for course in raw_courses]


        from django.db.models import Count, Avg, Max, Min, Sum, StdDev, Variance

        output["aggregate_avg"] = Student.objects.aggregate(avg_id=Avg('id'))
        output["aggregate_count"] = Student.objects.aggregate(total=Count('id'))
        output["aggregate_max"] = Student.objects.aggregate(max_id=Max('id'))
        output["aggregate_min"] = Student.objects.aggregate(min_id=Min('id'))
        output["aggregate_sum"] = Student.objects.aggregate(sum_id=Sum('id'))
        output["aggregate_stddev"] = Student.objects.aggregate(std_dev=StdDev('id'))
        output["aggregate_variance"] = Student.objects.aggregate(variance=Variance('id'))









        return Response(output)
    
