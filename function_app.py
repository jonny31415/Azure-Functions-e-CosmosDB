import azure.functions as func
from dotenv import load_dotenv
import logging
import os

app = func.FunctionApp()

# Function to post data to storage
@app.route(route="fnPostDataStorage", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
def fnPostDataStorage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Posting data to storage')

    # Get environment variables
    load_dotenv()
    storage_account_name = os.environ['STORAGE_ACCOUNT_NAME']
    storage_account_key = os.environ['STORAGE_ACCOUNT_KEY']

    # Get uploaded file and check for consistency
    data = req.get_json()

    print(data)

    # Check if file-type is correct in header
    if 'file-type' not in data:
        return func.HttpResponse(
            "Please include the 'file-type' in the header",
            status_code=400
        )
    
    file_type = data['file-type']
    if file_type not in ['.png', '.jpg', '.jpeg', '.mp4']:
        return func.HttpResponse(
            "Please include a valid 'file-type' in the header",
            status_code=400
        )
    
    # Check if file is included in the request
    if 'file' not in data:
        return func.HttpResponse(
            "Please include the file in the request",
            status_code=400
        )
    
    # Save file to storage account blob
    file = data['file']
    container_name = file_type

    print(container_name)

    # Create a blob service client
    blob_service_client = app.get_blob_service_client(storage_account_name, storage_account_key)

    # Create a blob container if it does not exist
    blob_service_client.create_container(container_name, fail_on_exist=False)

    # Upload file to blob
    blob_client = blob_service_client.get_blob_client(container_name, file.filename)
    blob_client.upload_blob(file)

    return func.HttpResponse(
        "File uploaded successfully",
        status_code=200
    )
