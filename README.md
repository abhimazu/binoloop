# Evaluation of Essays by LLMs

This repo contains implementations of a model server (LLM based) using either 'microsoft/phi-2' or 'google/gemma-7b' to evaluate and generate criticism for Essay that were previously generated by other LLMs using writing styles of few candidates appearing for English tests.

All the individual folders have READMEs that willl guide you through the deployment. The usual deployment order is:
1. **server**
2. **client**.

There are three branches in this repository:

1. **main** - Contains a FastAPI server hosting the LLM, that can handle concurrent requests from a client, to evaluate essays by parsing them from a csv dataset. (Tested)
2. **[cicd_github_actions](https://github.com/abhimazu/binoloop/tree/cicd_github_actions)** - Contains a CI/CD GitHub actions implementation for automated testing and Docker registry upload of the server image from the main branch. (Few Bugs)
3. **[trition_server](https://github.com/abhimazu/binoloop/tree/trition_server)** - Contains a Trition server based implementation that can accomodate both models with optimized dynamic batching which is capable of serving lots of users and concurrent requests. (Untested - Lack of resources)

Report back any improvements that you can suggest! Cheers!
