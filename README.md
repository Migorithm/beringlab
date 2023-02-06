# Bering lab Tech 

## Requirements I understand
Suppose there is a task with high time complexity served by Django framework. To improve performance with regard to concurrency, design event driven architecture and assign the time consuming task to a separate process.

### Requirement in detail
- Any persistent solution is OK
- Any queue or event broker is OK.
- docstring, comment, readme will be pluses
- exception handlings on worker, queue and etcetera will be pluses
- consideration for horizontal scalability


### Set up
- Installation of docker
- create external volume
```sh
docker volume create sqlite-db
docker compose up --build
```

### Test
Head over to localhost:8000/docs, have a fun!

