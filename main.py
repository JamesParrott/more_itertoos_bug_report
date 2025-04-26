# # pip3 install cassandra-driver==3.29.2 more_itertools==10.3.0
from dataclasses import dataclass
import more_itertools  # for ichunked()
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

if __name__ == "__main__":
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