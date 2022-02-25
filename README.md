# Project 1: book review website
it's a site that let users search for books, see reviews, add reviews and use it's api 


# import.py 
This file read about 5000 different book from books.csv file and import them in Postgresql


# application.py
This file includes all web application's logic btw handling user requests, calling Goodreads API and dealing with engine.

There are routes that let users:

1- register with validating user inputs.

2- login also with validation and remembering users by storing their sessions.

3- logout.

4- search for their favorite book with handling possible search queries and matching errors.

5- see information about selected book.

6- see added reviews submitted by other users.

7- see book rate and it's average review from Goodreads.

8 write our own review for each page only once.

9- use site api via (/api/isbn) will provide info for book isbn, title, author, publication year and reviews.
