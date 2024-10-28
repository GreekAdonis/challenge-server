# ♨️ Trusst.ai Interview Challenge ♨️

This project uses the serverless framework for deployment. To deploy, [set up your AWS credentials](https://www.serverless.com/framework/docs/providers/aws/guide/credentials) and then ```serverless deploy``` should do the trick.

The server requires the following environment variables to be set:
1. **llm_api_url**: The "completions" endpoint URL
2. **llm_api_model**: The model name to use for inference
3. **llm_api_token**: The auth token for connecting to the url (include "Bearer: " if your server requires it)
4. **chunk_size**: The number of lines to use as a chunk for the sliding window
