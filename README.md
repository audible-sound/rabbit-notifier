# Rabbit Notifier

A Simple Incident Reporting System using RabbitMQ

## Services


| Service         | Role                                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| `web-service`   | FastAPI app on port 3000. Accepts a receiver and message body, then publishes to the `incident_report` queue. |
| `rabbitmq`      | Message broker. Default user is `pbc` / `password`.                                                           |
| `email-service` | Consumes from `incident_report` and sends a "Site Incident Alert" email.                                      |


## Run

Requires Docker.

```bash
docker compose up --build
```

The API is at `http://localhost:3000`.

## Publish a message

```bash
curl -X POST http://localhost:3000/publish-message \
  -H "Content-Type: application/json" \
  -d '{"receiver": "you@example.com", "data": "Something went wrong on the site."}'
```



## Email settings

SMTP is configured in `email-service/main.py`. Update `smtp_host`, `smtp_port`, `username`, and `password` for the mail service you want to use.