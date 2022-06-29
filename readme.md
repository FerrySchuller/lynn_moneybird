### CLI to https://developer.moneybird.com
### Gemaakt door https://lynn-vastgoed.nl

Exampes:

API GET request
```
$ python app.py api GET users.json
```

Tijdschrijven:
```
python app tijd <omschrijving> <user_id> <project_id> <contact_id> <started_at> <ended_at>
python app.py tijd "stucen" "Ferry Schuller" Opdracht1 Jan "2022-06-29 12:03:46 GMT-2" "2022-06-29 12:03:46 GMT-2"
```

Requirement:

```
$ cat .env 
schaduw_mb_bearer = <key>
schaduw_mb_administration = <administration_number>

mb_bearer = <key>
mb_administration = <administration_number>
```

