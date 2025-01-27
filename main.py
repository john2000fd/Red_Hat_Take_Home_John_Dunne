import requests
import json

# repository holding the Red Hat build of Keycloak’s container image history 
repository = "https://catalog.redhat.com/api/containers/v1/repositories/registry/registry.access.redhat.com/repository/rhbk/keycloak-rhel9/images"

# Here we are doing a GET request to the red hat Keycloak repo
repo_Response = requests.get(repository)

# Testing to make sure we are getting a successful call
# As the status code we receive is 200, we know the server successfully processed the request  
print(repo_Response.status_code)


repo_info = requests.get(repository)
var = json.loads(repo_info.text)
print(var)


    


