# supermarketapi

Install:
```
git clone https://github.com/nautics889/supermarketapi.git
docker-compose build
```

SQLite3-DB with some fixtures is already in repository.

Use:
```
docker-compose up
```
to run a server.
Open http://127.0.0.1:8000/rest-auth/login/ and log in. Further open http://127.0.0.1:8000/purchase/ to make checkout. Cost counts by following prices: 

“A costs 50 cents,”

“three A cost $1.30,”

“B costs 30 cents, two B cost 45 cents,”

“$1.99 per kg of C,” and

“D costs $1.20, E costs $0.90, buy two D, get one E free.”
