"""
Uploads pdf document to EchoSign and returns its transientDocumentId
Sends agreement using transient to single signer.

"""
import requests
import json
from random import *

thisToken = '3AAABLblqZ****** ACCESS TOKEN OR INTEGRATION KEY HERE ******LfnS1rzdwxL' # your access token or integration key
fpath = './some_file_to_upload.pdf' # path to file
tname = 'my_document_name.pdf' # transient doc name with extension
myShard = 'na4' # the "shard" your account is on
senderEmail = 'sender_email@example.com' # email address of sender or token owner
recipt_email = 'recipient_email@example.com' # email address of recipient
rand_number = randint(1, 100)

def upl_trans(api_token, file_path, docName, ashard, sender):
    url = f"https://secure.{ashard}.adobesign.com/api/rest/v6/transientDocuments"
    payload={'File-Name': docName}
    files=[
        ('File',('empty.pdf',open(file_path,'rb'),'application/pdf'))
        ]
    headers = {
            'x-api-user': f'email:{sender}',
            'Authorization': f'Bearer {api_token}',
            'User-Agent': f'MyApplicationName_to_help_with_troubleshooting_{rand_number}' # Please include a user agent string
        }
    return requests.request("POST", url, headers=headers, data=payload, files=files).json().get('transientDocumentId')

def send_last_trans_to_one_signer(api_token, shard, trans_id, ag_name, sender, rcpt_email):
    url = f"https://secure.{shard}.adobesign.com/api/rest/v6/agreements"
    payload = json.dumps({
        "fileInfos": [
                {
                "transientDocumentId": trans_id
                }
            ],
        "name": ag_name,
        "participantSetsInfo": [
            {
                "memberInfos": [
                        {
                            "email": rcpt_email
                        }
                    ],
                "order": 1,
                "role": "SIGNER"
            }
        ],
        "message": "Plese sign this from us.",
        "signatureType": "ESIGN",
        "externalId": {
                        "id": rand_number
        },
        "state": "IN_PROCESS"
    })
    headers = {
                'x-api-user': f'email:{sender}',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_token}',
                'User-Agent': f'MyApplicationName_to_help_with_troubleshooting_{rand_number}' # Please include a user agent string
            }
    response = requests.request("POST", url, headers=headers, data=payload).json().get('id')
    return response


uploadtransID = upl_trans(thisToken, fpath, tname, myShard, senderEmail)

print(f'Got transient upload with ID:\n\n {uploadtransID}\n\n Now sending Agreement to {recipt_email}\n\n')

new_ag_id = send_last_trans_to_one_signer(thisToken, myShard, uploadtransID, f"New agreement Test {rand_number}", senderEmail, recipt_email)

print(f'Agreement \n\n"New agreement Test {rand_number}"\n\nwith ID: \n\n    {new_ag_id}\n\n    was sent to {recipt_email}. \n\nPlease have {recipt_email} check their inBox!\n\n')

