# NVidia Trition Server + FastAPI + CSV Client

This is an implementation using NVidia Trition server to serve both the models (phi-2 and gemma) for inference and FastAPi server to aggregate requests and send back responses to the client. 

The sequence to deploy and run is:

1. modelserver
2. server
3. client

README docs inside each folder will guide you through the process! Cheers. 

Note: Due to lack of GPU this code hasn't been tested and may have some small bugs. This is true to the best of my knowledge. 
