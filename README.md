# mailInventoryImport
This simple python tool downloads .csv inventory stocktakes from a Mail server and imports to [WebIMS](https://github.com/zammitjohn/WebIMS). It exploits Inventory ```import``` API to import inventory data. This tool must be executed per category import job.

## Instructions
1. Install all required libraries and launch mailInventoryImport.py
2. Enter mail server settings, fetch frequency (in seconds) and mail server folder name.
3. Define subject filter. Any incoming mail with subject containing the entered string will be processed. 
4. Enter API host 'https://*hostname*/WebIMS'.
5. Obtain sessionId via Users ```login``` API and enter session key. 
6. Obtain categoryId via Inventory Categories ```read``` API and enter inventory category ID.
7. Import job will be executed for any incoming mail with .csv attachments as per defined subject filter.