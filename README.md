# Cloud Computing Project: Scalable Distributed Object Storage with Consitent Hashing
### Load balancer for Object Storage that provides REST API to Create/Delete Buckets and Create/Update/Delete Files.
Implementation of the characterstics of [Amazon Dynamo Paper](https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf) like Consistent Hashing, Sloppy Quorum and Hinted Handoff as REST based Object storage service. 
#### Requirements:
- Python 3
- [Cloud Storage Repository](https://github.com/vishnuys/cloudstorage)
- List of Storage Nodes and their addresses available in the system

#### Installation:
1) Create a virtualenv `LoadBalancer` and activate it. If you do not have virtualenv installed, install it. (Installation: [Windows](https://thinkdiff.net/python/how-to-install-python-virtualenv-in-windows/), [Linux & MAC OS](https://medium.com/@garimajdamani/https-medium-com-garimajdamani-installing-virtualenv-on-ubuntu-16-04-108c366e4430))
2) Clone the Load Balancer repo into the desired directory.
3) In the project home folder, Install the necessary packages using the command `pip install -r requirements` .
4) Create `config.py` in `clouder` folder.
5) Add the following code to `config.py`
    ```python
    NODE_LIST = [<List of the Storage Nodes>]
    NODE_ADDRESS = {<Each node in NODE_LIST as key and its corresponding address as its value>}
    REPLICATION_FACTOR = <Minimum number of replications needed for each read/write>
    ```
6) Execute the following command to apply migrations: `python manage.py migrate`.
7) To run the server on local IP assigned with default port, execute the command `python manage.py runserver 0.0.0.0:8000`. 

#### Usage:
This REST API doesn't have any authentication. To access this API, send a **POST** request using any request managers like Postman to specified address given below.

- **Create Bucket:** 
        - *URL*: `/create/bucket/`
        - *Request Body*: 'name' = <Bucket name>
        - *Result*:  `{status: <Success/Failure>, node: <Node at which the bucket was created>}`
- **Delete Bucket:** 
        - *URL*: `/delete/bucket/`
        - *Request Body*: 'name' = <Bucket name>
        - *Result*:  `{status: <Success/Failure>, node: <Node at which the bucket was deleted>}`
- **Create File:** 
        - *URL*: `/create/file/`
        - *Request Body*: 'name' = <File name>, 'bucket' = <Bucket name>, 'file' = <File to be Stored>
        - *Result*:  `{status: <Success/Failure>, node: <Node at which the file was created>, vector_clocks: {<Vector Clock of each node after file creation>}}`
- **Update File:** 
        - *URL*: `/update/file/`
        - *Request Body*: 'name' = <File name>, 'bucket' = <Bucket name>, 'file' = <File to be Updated>
        - *Result*:  `{status: <Success/Failure>, node: <Node at which the file was updated>, vector_clocks: {<Vector Clock of each node after file updation>}}`
- **Delete File:** 
        - *URL*: `/delete/file/`
        - *Request Body*: 'name' = <File name>, 'bucket' = <Bucket name>
        - *Result*:  `{status: <Success/Failure>, node: <Node at which the file was deleted>}`

You can learn more about APIs and how to use them [here](https://schoolofdata.org/2013/11/18/web-apis-for-non-programmers/).
