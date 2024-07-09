import boto3
from botocore.exceptions import ClientError

def send_email(subject, body):
    # Create a new SES resource and specify a region.
    ses_client = boto3.client('ses', region_name='us-east-1')  # Change to your AWS SES region

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    NOTIFICATION_EMAIL,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=EMAIL_ADDRESS,
        )
    except ClientError as e:
        print(f"Failed to send email. Error: {e.response['Error']['Message']}")
    else:
        print("Email sent! Message ID:", response['MessageId'])