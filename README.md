# mailInventoryImport
This simple python tool downloads .csv inventory stocktakes from a Mail server and imports to [WebIMS](https://github.com/zammitjohn/WebIMS). It exploits Inventory ```import``` API to import inventory data. This tool must be executed per category import job.

## Instructions
1. Install all required libraries and launch [main.py](main.py)
2. Enter sync settings, fetch frequency (in seconds) and mail server folder name.
3. Define subject filter. Any incoming mail with subject containing the entered string will be processed. 
4. Enter API host 'https://*hostname*/WebIMS'.
5. Obtain sessionId via Users ```login``` API and enter session key. 
6. Obtain categoryId via Inventory Categories ```read``` API and enter inventory category ID.
7. Import job will be executed for any incoming mail with .csv attachments as per defined subject filter.
8. Enter mailbox settings. Supported configurations include IMAP and Microsoft Outlook (recommended, see instructions below).

### Microsoft Outlook Configuration
To allow authentication you first need to register your application at Azure App Registrations.

1. Login at [Azure Portal](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade) (App Registrations)
2. Create an app. Set a name.
3. In Supported account types choose "Accounts in any organizational directory and personal Microsoft accounts (e.g. Skype, Xbox, Outlook.com)".
4. Set the redirect uri (Web) to: https://login.microsoftonline.com/common/oauth2/nativeclient and click register. This needs to be inserted into the "Redirect URI" text box as simply checking the check box next to this link seems to be insufficent. This is the default redirect uri used by this library, but you can use any other if you want.
5. Write down the Application (client) ID. You will need this value.
6. Under "Certificates & secrets", generate a new client secret. Set the expiration preferably to never. Write down the value of the client secret created now. It will be hidden later on.
7. Under API Permissions, add delegated permissions for the following Microsoft Graph scopes (Mail.ReadWrite, offline_access, User.Read).
8. Then you need to login for the first time to get the access token that will grant access to the user resources.