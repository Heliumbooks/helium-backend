from os import stat
from py import process
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# from olclient.openlibrary import OpenLibrary
# import pandas as pd
import requests
import time
from datetime import datetime
import pytz

from helium_backend.books.models import Book, Author, Subject, IsbnNumber


def process_book_updates(books):
    api_base_url = "https://openlibrary.org/search.json?"
    count = 0
    for item in books:
        print(item.get('title'))
        formatted_author = item.get('author__full_name').replace(" ", "+")
        formatted_title = item.get('title').replace(" ", "+")
        try:
            if count % 90 == 0 and count != 0:
                time.sleep(300)
            response = requests.get(f"{api_base_url}author={formatted_author}&title={formatted_title}").json()
            count += 1
            if response.get('numFound') > 0:
                book = Book.objects.filter(pk=item.get('id')).first()
                book_ol_id = response.get('docs')[0].get('key').split("/")[-1]
                book.book_ol_id = book_ol_id
                pages = response.get('docs')[0].get('number_of_pages_median')
                if pages:
                    book.pages = pages
                # Need to convert this to an acutal date
                published_dates = response.get('docs')[0].get('publish_date')
                for item in published_dates:
                    if len(item) == 4:
                        publish_date = datetime(int(item), 1, 1, 0, 0, 0, 0, tzinfo=pytz.UTC)
                        book.published_date = publish_date
                        break

                if response.get('docs')[0].get('isbn'):
                    for x in response.get('docs')[0].get('isbn'):
                        isbn, isbn_created = IsbnNumber.objects.get_or_create(
                            book=book,
                            isbn=x
                        )
                if response.get('docs')[0].get('subject'):
                    for i in response.get('docs')[0].get('subject'):
                        subject = Subject.objects.filter(title=i).first()
                        if subject:
                            subject.books_in_subject += 1
                            subject.save()
                            book.subjects.add(subject)
                        else:
                            subject = Subject.objects.create(
                                title=i,
                                books_in_subject=1
                            )
                            book.subjects.add(subject)
                book.processed_from_open_lib = True
                book.save()
                print(f"Successfully processed {book.title}")
                continue
            else:
                print('book not in database')
        except Exception as e:
            print('unable to get books')
            print(e)


# class DatabaseLoad(APIView):

#     def post(self, request):
#         file_path = '/Users/charlesclark/Documents/development/helium/Helium_Books_Database.csv'

#         df = pd.read_csv(file_path, index_col=False)

#         book_data = df[["Title", "Author"]]
#         for index, row in book_data.iterrows():
#             book_title = row['Title']
#             book_author = row['Author']
#             author, author_created = Author.objects.get_or_create(
#                 full_name=book_author
#             )

#             book, book_created = Book.objects.get_or_create(
#                 title=book_title,
#                 author=author
#             )
#         data = {"status": "complete"}
#         return Response(status=status.HTTP_200_OK, data=data)

class DatabaseUpdate(APIView):

    def post(self, request):
        api_base_url = "https://openlibrary.org/search.json?"
        books = Book.objects.filter(processed_from_open_lib=False).values('id', 'title', 'author__full_name').order_by('title')
        process_book_updates(books)

        data = {"status": "Function has started successfully"}
        return Response(status=status.HTTP_200_OK, data=data)

# class UpdateBookInfo(APIView):

#     def post(self, request):
#         client = OpenLibrary()
#         books = Book.objects.all().values('id', 'title', 'book_ol_id', 'author__id').order_by('title')
#         for item in books[:20]:
#             try:
#                 book = Book.objects.get(pk=item.get('id'))
#                 work = client.Work.get(f"{item.get('book_ol_id')}")
#                 book.synopsis = work.description 
#                 if work.authors:
#                     for author in work.authors:
#                         author_ol_id = author.get('author').get('key').split("/")[-1]
#                         ol_author = client.Author.get(author_ol_id)
#                         if ol_author.bio:
#                             author = Author.objects.get(pk=item.get('author__id'))
#                             author.information = ol_author.bio
#                             author.save()
#                 book.save()
#             except Exception as e:
#                 print(e)
        
#         data = {"status": "complete"}
#         return Response(status=status.HTTP_200_OK, data=data)