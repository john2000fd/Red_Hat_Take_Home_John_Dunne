import requests
import json
from datetime import *
 


def find_Most_Recent_Images():

    # Here we have a dictionary used to store the info of each instance 
    image_Dict = {
        "contentStream": "",
        "vcsRef" : "",
        "publishedDate": "",
        "freshnessGrade": ""
    }

    # repository holding the Red Hat build of Keycloak’s container image history, with the included fields we want 
    repository_images = "https://catalog.redhat.com/api/containers/v1/repositories/registry/registry.access.redhat.com/repository/rhbk/keycloak-rhel9/images"

    # Here we are doing a GET request to the red hat Keycloak repo
    repo_Response = requests.get(repository_images)

    # Testing to make sure we are getting a successful call
    # As the status code we receive is 200, we know the server successfully processed the request  
    print(repo_Response.status_code)

    # this deseriealizes the JSON to a python obj so we can read it 
    text = json.loads(repo_Response.text)

    # 'data' is the key which holds all of the image's info
    image_info = text.get('data', [])
    
    # iterate over images to get repo info 
    for info in image_info:
        repository_data = info.get("repositories", {})
        print(repository_data)
        # from "repositories" section, i will retrieve "published_date", if it exists 
        for instance in repository_data:
            if 'published_date' in repository_data:
                published_date = instance.get('published_date')
                print(published_date)
            else:
                print("error")
                break    





if __name__ == "__main__":
    find_Most_Recent_Images()


















    


