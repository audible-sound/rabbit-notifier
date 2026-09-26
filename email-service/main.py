import pika
import smtplib, json, time
from email.mime.text import MIMEText
import traceback

def send_mail(message):
    message_dict = json.loads(message)
    subject = "Site Incident Alert"
    receiver = message_dict["receiver"]
    body = message_dict["data"]

    # I'm using a temporary email service
    # Change the values of the variables below according to the service you're using
    smtp_host = "smtp.ethereal.email"
    smtp_port = 587
    username = "estelle.nikolaus9@ethereal.email"
    password = "26Crt1pGyPpjw91aRr" 
    
    mail = MIMEText(body, "plain")
    mail["Subject"] = subject
    mail["From"] = username
    mail["To"] = receiver
    
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(username, password)
        print("Sending mail....")
        server.sendmail(username, receiver, mail.as_string())

def main():
    try:
        credentials = pika.PlainCredentials(
            username="pbc", password="password")
        parameters = pika.ConnectionParameters(
            host="rabbitmq", port=5672, credentials=credentials
        )
        print("Connecting to rabbitmq...")
        connection = pika.BlockingConnection(parameters=parameters)
        channel = connection.channel()
        print("Connected Successfully!")
        channel.queue_declare(queue="incident_report", durable=True)
        def on_message_callback(ch, method, _, body):
            try:
                send_mail(body)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                 print(f"Error sending email: {type(e)}")
                 traceback.print_exc()
                 ch.basic_nack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue="incident_report", on_message_callback=on_message_callback)
        channel.start_consuming()
    except Exception as e:
        print(f"Failed to send email: {type(e)}")
        traceback.print_exc()
    
if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"Failed to execute email service: {type(e)}")
            traceback.print_exc()
            time.sleep(0.5)
