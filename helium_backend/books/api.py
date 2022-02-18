from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from olclient.openlibrary import OpenLibrary
import pandas as pd
import requests
import time

from helium_backend.books.models import Book, Author


class DatabaseLoad(APIView):

    def post(self, request):
        file_path = '/Users/charlesclark/Documents/development/helium/Helium_Books_Database.csv'

        df = pd.read_csv(file_path, index_col=False)

        book_data = df[["Title", "Author"]]
        for index, row in book_data.iterrows():
            book_title = row['Title']
            book_author = row['Author']
            author, author_created = Author.objects.get_or_create(
                full_name=book_author
            )

            book, book_created = Book.objects.get_or_create(
                title=book_title,
                author=author
            )
        data = {"status": "complete"}
        return Response(status=status.HTTP_200_OK, data=data)

class DatabaseUpdate(APIView):

    def post(self, request):
        ol_client = OpenLibrary()
        api_base_url = "https://openlibrary.org/search.json?"
        books = Book.objects.all().values('id', 'title', 'author__full_name').order_by('title')
        count = 0
        for item in books[:2]:
            formatted_author = item.get('author__full_name').replace(" ", "+")
            formatted_title = item.get('title').replace(" ", "+")
            try:
                if count % 90 == 0 and count != 0:
                    time.sleep(300)
                response = requests.get(f"{api_base_url}author={formatted_author}&title={formatted_title}").json()
                count += 1
                book = Book.objects.filter(pk=item.get('id')).first()
                book_ol_id = response.get('docs')[0].get('key').split("/")[-1]
                ol_book = ol_client.Work.get(book_ol_id)
                # Can get description, notes, author ID and subjects from the library
                # can use this to update the author as well
                # still need to get the isbn information from the API though

            except:
                print('unable to get books')
        # ol_client = OpenLibrary()
        # book = ol_client.Work.get('OL19763711W')
        # other_version = ol_client.
        data = {"status": "complete"}
        return Response(status=status.HTTP_200_OK, data=data)