from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Author, Book#, Product
from django.db.models import Count

class OrmTestView(APIView):

    def get(self, request):
        output = {}

        # CREATE
        author = Author.objects.create(name="Author CBV")
        book = Book.objects.create(title="Book CBV", author=author)
        output["create"] = {"author": author.name, "book": book.title}

        # GET
        try:
            book = Book.objects.get(id=book.id)
            output["get"] = book.title
        except Book.DoesNotExist:
            output["get"] = "Book not found"

        # GET_OR_CREATE
        author2, created = Author.objects.get_or_create(name="Author CBV2")
        output["get_or_create"] = {"author": author2.name, "created": created}

        # UPDATE_OR_CREATE
        book2, created = Book.objects.update_or_create(
            id=book.id,
            defaults={"title": "Book Updated CBV"}
        )
        output["update_or_create"] = {"book": book2.title, "created": created}

        # BULK_CREATE
        books = Book.objects.bulk_create([
            Book(title="Bulk 1", author=author2),
            Book(title="Bulk 2", author=author2),
        ])
        output["bulk_create"] = [b.title for b in books]

        # BULK_UPDATE
        for b in books:
            b.title += "++"
        Book.objects.bulk_update(books, ['title'])
        output["bulk_update"] = [b.title for b in books]

        # COUNT
        output["count"] = Book.objects.count()

        # IN_BULK
        ids = Book.objects.values_list('id', flat=True)
        output["in_bulk"] = {str(k): v.title for k, v in Book.objects.in_bulk(ids).items()}

        # ITERATOR
        output["iterator"] = [b.title for b in Book.objects.iterator()]

        # LATEST / EARLIEST
        try:
            output["latest"] = Book.objects.latest('id').title
            output["earliest"] = Book.objects.earliest('id').title
        except Book.DoesNotExist:
            output["latest"] = output["earliest"] = "No books"

        # FIRST / LAST
        output["first"] = Book.objects.first().title 
        output["last"] = Book.objects.last().title 
        # AGGREGATE
        output["aggregate"] = Book.objects.aggregate(total_books=Count('id'))

        # EXISTS
        output["exists"] = Book.objects.exists()

        # UPDATE
        Book.objects.filter(author=author2).update(title="Updated by CBV")
        output["update"] = "Updated titles for author2"

        # DELETE
        Book.objects.filter(title__icontains="Bulk").delete()
        output["delete"] = "Deleted bulk books"

        # # AS_MANAGER
        # # Already implemented in Product model
        # active_products = Product.active_objects.all()
        # output["as_manager"] = [p.name for p in active_products]

        # EXPLAIN
        output["explain"] = Book.objects.filter(author=author).explain()

        return Response(output)
