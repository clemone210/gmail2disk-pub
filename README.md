## Documentation

### Overview

This code is a Python script that connects to the Gmail API and downloads the latest attachment(s) from specified labels.

### Required Libraries

The following libraries are required for this script:

- `os`
- `base64`
- `google.oauth2.credentials`
- `google.auth.transport.requests`
- `google_auth_oauthlib.flow`
- `googleapiclient.discovery`
- `googleapiclient.errors`

### Gmail API Client Setup

The first step in the script is to set up the Gmail API client using the user's credentials. If a `token.json` file exists in the same directory as the script, it is used to authenticate the user. Otherwise, the user is prompted to log in and authenticate the script using their Google account.
You will need to save the credentials.json file into the project root directory.

### Labels and Subfolder Name

The script defines the labels for which to download attachments and the subfolder in which to save them. By default, the subfolder is named "attachments", but this can be changed.
You can use the API to get all your Label-Id's: [here](https://developers.google.com/gmail/api/reference/rest/v1/users.labels/list?hl=de)

### Attachment Subfolder Creation and Cleaning

If the subfolder does not exist, the script creates it. If the subfolder already exists, the script deletes all files in the folder before downloading new attachments.

### Downloading Attachments

For each label specified, the script searches for the latest email with that label and downloads any attachments from that email to the subfolder. If no attachments are found in the email, the script continues to the next email.

### Output

After each attachment is downloaded, the script outputs a message indicating that the attachment was successfully downloaded and saved to the subfolder. If no messages are found with a particular label, the script outputs a message indicating that no messages were found with that label.
