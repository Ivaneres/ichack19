# Karaoke app

## Python dependency installation

```
pip install -r requirements.txt
```

## Backend

To run

```
python backend.py
```

Send a request
```
curl -i -H "Content-Type: application/json" -X POST -d '{"lyrics":"hey now youre a rockstar"}' localhost:33507
```