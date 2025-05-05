IMPORTANT

Make sure you have Python 3.7 or higher installed on your system. If you don’t have it, you can download it from python.org.

In order to use this program, you'll need to set up a project in Google Cloud Console and enable the necessary APIs. Follow these steps:

1. Create a Google Cloud Account
If you don’t already have one, create a Google Cloud account at https://cloud.google.com.

2. Create a New Project
Go to the Google Cloud Console.

In the top left, click the project drop-down, then click New Project.

Name your project and click Create.

3. Enable the YouTube Data API v3
In the Google Cloud Console, navigate to the API & Services > Library.

Search for YouTube Data API v3 and click on it.

Click Enable to activate the API for your project.

4. Create API Credentials
Go to API & Services > Credentials.

Click on Create Credentials and select API Key.

Copy the generated API key—you’ll need it for the project.

5. Set Up OAuth 2.0 
Go to Credentials.

Click Create Credentials > OAuth 2.0 Client IDs.

Configure the OAuth consent screen with your app’s information.

Download the client secret JSON file, rename it to client_secrets.json and drop it in root folder (.\Youtube Bulk Uploader).


