import csv
import sqlalchemy
from sqlalchemy import create_engine, text


# # set up database
engine = create_engine(
    "postgresql://slniyhprhdecdt:4c47420a0456d96c614a9136f5aa850f90a5f76370da0abe0d294ad755eace47@ec2-18-215-111-67.compute-1.amazonaws.com:5432/d2k26gq36rcfe0", echo=True)
# creating user table
# Users = text("""
# CREATE TABLE IF NOT EXISTS Users (
#     Id SERIAL NOT NULL,
#     User_Name TEXT NOT NULL unique,
#     Email TEXT NOT NULL,
#     password TEXT NOT NULL,
#     PRIMARY KEY (Id)
#     );
#         """)
engine.execute(Users)
Books = text("""
CREATE TABLE IF NOT EXISTS Books (
    Id SERIAL NOT NULL,
    name TEXT NOT NULL,
    price SERIAL NOT NULL,
    shoe_size SERIAL NOT NULL,
    description TEXT NOT NULL,
    categories TEXT NOT NULL,
    available Boolean NOT NULL,
    PRIMARY KEY (Id)
    );
        """)
engine.execute(Books)
# creating review table
# Reviews = text("""
# CREATE TABLE IF NOT EXISTS Reviews (
#     Id SERIAL NOT NULL,
#     User_Id TEXT references Users(User_Name),
#     Book_Isbn TEXT references Books(Isbn),
#     review TEXT NOT NULL,
#     rating TEXT NOT NULL,
#     PRIMARY KEY(Id)
#     );
#         """)
# engine.execute(Reviews)
# #  creating Book table


def BookFun():
    with open('shop.csv', 'r') as book:
        book_csv_reader = csv.reader(book, delimiter=',')

        for row in book_csv_reader:
            # print(row)
            # Isbn = row[0]
            # Title = row[1]
            # Book_Author = row[2]
            # Published_year = row[3]
            engine.execute(text(
                f"""
                insert into Books (Isbn,Title,Author,Year) values (:isbn,:title,:author,:year);
                """), {"isbn": row[0], "title": row[1], "author": row[2], "year": row[3]}
            )


BookFun()
