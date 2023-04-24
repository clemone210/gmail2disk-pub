import os
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up the Gmail API client
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.readonly'])

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/gmail.readonly'])
        creds = flow.run_local_server(port=0)
    
    # Save the credentials to a file
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('gmail', 'v1', credentials=creds)

# Define the labels and subfolder name
labels = ['Label_Label_XXXXXXXXXXXXXXXXXX', 'Label_XXXXXXXXXXXXXXXXXX']
subfolder = 'attachments' #<-you can change this

# Create the attachments subfolder if it doesn't exist
if not os.path.exists(subfolder):
    os.mkdir(subfolder)

# Clean the attachments subfolder
for filename in os.listdir(subfolder):
    file_path = os.path.join(subfolder, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(f'An error occurred while deleting file: {file_path} - {e}')

# Loop through each label and download the latest file
for label in labels:
    try:
        # Get the ID of the latest email with the specified label
        response = service.users().messages().list(userId='me', labelIds=[label], maxResults=1).execute()
        message_id = response['messages'][0]['id']
    except HttpError as error:
        print(f'An error occurred: {error}')
        message_id = None

    if message_id:
        # Get the full message details
        try:
            message = service.users().messages().get(userId='me', id=message_id).execute()
            
        except HttpError as error:
            print(f'An error occurred: {error}')
            message = None

        if message:
            # Find the attachment and download it
            for part in message['payload']['parts']:
                if part.get('filename'):
                    if part['filename']:
                        if 'data' in part:
                            data = part['data']
                        else:
                            att_id = part['body']['attachmentId']
                            att = service.users().messages().attachments().get(userId='me', messageId=message_id,id=att_id).execute()
                            data = att['data']

                        # Save the attachment to the subfolder
                        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                        #timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        file_name = f"{part['filename']}"
                        path = os.path.join(os.path.dirname(__file__), subfolder, file_name)
                        with open(path, 'wb') as f:
                            f.write(file_data)
                        
                        print(f'Successfully downloaded and saved attachment: {file_name}')

else:
    print(f'No messages found with label "{label}"')
