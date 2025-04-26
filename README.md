# more_itertoos_bug_report

https://github.com/more-itertools/more-itertools/issues/980

I'm trying to use `more_itertools.ichunked` function to read data from Cassandra in chunks.
When I was using `more_itertools==10.2.0` everything was okay. 
But when I had upgraded to `more_itertools==10.3.0` or newer 
the iterator of iterators that ichunked returned new and new sub-iterators with same and same contents.

It looks like a strange bug in new `ichunked` implementation...

Here's an example of what I'm doing (`Python 3.12`, `more_itertools==10.7.0`)

To reproduce the bug run the following:

```bash
cd more_itertools_bug_report

docker compose up -d

# wait about a minute while Cassandra is starting...

uv run main.py
```