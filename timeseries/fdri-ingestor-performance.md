## Ingestor performance test

<img width="1805" height="676" alt="image" src="https://github.com/user-attachments/assets/2079e259-345f-45b0-a9b7-f4df04c5b63a" />


During our AWS migration, we migrate all 3.8 Million FDRI messages we have received so far. This doubled as a performance test for our ingester and we found that we could ingest roughly 50,000 messages an hour, ~1.2 Million per 24 hours.

Keeping this note, as is may be useful for future. Also important to note is that SQS can only retain messages for up to 14 days, so the maximum number of messages we can handle on the queue without some falling off is roughly 16.8 million.

Breaking this down into numbers based on the planned scale of the fdri network 16.8M / 500 sites / 60 minutes / 24 hours = 23.3 days of minute resolution across all sites can be replayed at once. To replay more data we would need some intervention.
