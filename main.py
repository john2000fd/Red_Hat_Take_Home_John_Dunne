import requests
import json

# repository holding the Red Hat build of Keycloak’s container images 
repository = "https://catalog.redhat.com/software/containers/rhbk/keycloak-rhel9/64f0add883a29ec473d40906"

# Here we are doing a GET request to the red hat Keycloak repo
repo_Response = requests.get(repository)

# Tsting to make sure we are getting a successful call
# As the status code we receive is 200, we know the server successfully processed the request  
print(repo_Response.status_code)


