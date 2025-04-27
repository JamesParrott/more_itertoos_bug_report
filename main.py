# # pip3 install cassandra-driver==3.29.2 more_itertools==10.3.0

from typing import Any, Self
from dataclasses import dataclass

import more_itertools  # for ichunked()
# from cassandra.cluster import Cluster
# from cassandra.auth import PlainTextAuthProvider

@dataclass
class Row:
    id: int
    value: str

    @classmethod
    def from_int(cls, i: int) -> Self:
        return cls(i, f"value_{i}")


class PaginatedIterator:
    
    def __init__(
        self,
        pages: list[list[Row]],
    ):
        self._pages_iter = iter(pages)
        self._current_rows = next(self._pages_iter)
        self.num_pages = len(pages)
        self.pages_so_far = 1

    def __iter__(self):

        self._rows_iter = iter(self._current_rows)
        return self

    def next(self):
        try:
            return next(self._rows_iter)
        except StopIteration as e:
            if self.pages_so_far >= self.num_pages:
                raise e

        self.fetch_next_page()



        return next(self._rows_iter)

    __next__ = next

    def fetch_next_page(self):
        self._current_rows = next(self._pages_iter) 
        self._rows_iter = iter(self._current_rows)
        self.pages_so_far += 1



rows = (Row.from_int(i+1) for i in range(15))


if __name__ == "__main__":
    
    rows = (Row.from_int(i+1) for i in range(15))
    paginated_iterator = PaginatedIterator([[next(rows), next(rows), next(rows)] for _ in range(5)])
    for row in paginated_iterator:
        print(row)

    rows = (Row.from_int(i+1) for i in range(15))
    paginated_iterator = PaginatedIterator([[next(rows), next(rows), next(rows)] for _ in range(5)])

    for (j, chunk) in enumerate(more_itertools.ichunked(paginated_iterator, 5)):
        if j > 7:
            break
        print(f'{j}) {list(chunk)}')


def main_cass():
    # 1) Connect to Cassandra with PlainTextAuthProvider
    auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')  #
    cluster = Cluster(["localhost"], auth_provider=auth_provider)  #
    session = cluster.connect()  #

    # Create a keyspace named 'default' for our table
    session.execute("CREATE KEYSPACE IF NOT EXISTS default "
                    "WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1}")

    # 2) Create first table in default keyspace
    session.execute("""
        CREATE TABLE IF NOT EXISTS default.table1 (
            id    int PRIMARY KEY,
            value text
        )
    """)  #

    N = 15

    # 3) Insert 100 rows into table1
    for i in range(1, N+1):
        session.execute(
            "INSERT INTO default.table1 (id, value) VALUES (%s, %s)",
            (i, f"value_{i}")
        )  #

    # 5) Read rows and chunk into sub-iterators of 20 items
    rows = session.execute("SELECT id, value FROM default.table1")  #
    # @dataclass
    # class Row:
    #     id: int
    #     value: str

    # rows = [Row(i+1, f'Val: {i+1}') for i in range(100)]
    # for row in rows:
    #     print(f'{row=!r}, {type(row)} {dir(row)=}')

    # print(vars(rows))

    # chunked_iters = more_itertools.ichunked(rows, N // 5)  #


    # #  Let's read the from the table: I assume that there will be 5 chunks with size 20 each
    # for i, chunk in enumerate(chunked_iters):
    #     print(f"chunk_idx: {i}")
    #     # But here are generated new and new and new and new chunks wuth same and same and same contents!!!!!!
    #     params = [(row.id, row.value) for row in chunk]
    #     print(params)

    #     if i > 10*N:
    #         raise Exception("What the hell is going on, there should be only 5 chunks!!!")

    # Cleanup
    # session.shutdown()
    # cluster.shutdown()