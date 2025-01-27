import requests
import json
from datetime import *
 


def image_Times():

    # repository holding the Red Hat build of Keycloak’s container image history 
    repository_images = "https://catalog.redhat.com/api/containers/v1/repositories/registry/registry.access.redhat.com/repository/rhbk/keycloak-rhel9/images"

    # Here we are doing a GET request to the red hat Keycloak repo
    repo_Response = requests.get(repository_images)

    # Testing to make sure we are getting a successful call
    # As the status code we receive is 200, we know the server successfully processed the request  
    print(repo_Response.status_code)

    # this deseriealizes the JSON to a python obj so we can read it 
    text = json.loads(repo_Response.text)

    # data is the key which holds all of the image's info
    image_info = text.get('data', [])
    
    # list to store dates 
    dates = []

    # iterate over images to get repo info 
    for info in image_info:
        repository_data = info.get("repositories", {})
        # from "repositories" section, i will retrieve "published_date", if it exists 
        for instance in repository_data:
            if 'published_date' in instance:
                published_date = instance.get('published_date')
                #adding to a list
                dates.append(published_date)
                #print(published_date)
            else:
                print("error")
                break    
    return dates



# function to determine the release and version of the image 
def versions_Release(times, image_dict):
    # list to store versions and releases 
    version = []
    release = []

    repository_images = "https://catalog.redhat.com/api/containers/v1/repositories/registry/registry.access.redhat.com/repository/rhbk/keycloak-rhel9/images"

    # Here we are doing a GET request to the red hat Keycloak repo
    repo_Response = requests.get(repository_images)

    # this deseriealizes the JSON to a python obj so we can read it 
    text = json.loads(repo_Response.text)

    # data is the key which holds all of the image's info
    image_info = text.get('data', [])
    # Loop through each image
    for info in image_info:
        #we retrieve the 'parsed data' info
        image_data = info.get('parsed_data', {})
        #then we loop through the data in the parsed data dictionary to get to 'labels' where version is stored 
        for image in image_data:
            # we then retrieve the 'labels' info
            label_info = image.get('labels', [])

            if 'version' in label_info:
                vers = image.get('version')
                version.append(vers)
            else:
                print("Error")


    print(version)                

    

    
    






if __name__ == "__main__":

    # Here we have a dictionary used to store the info of each instance so we can determine the most recent image of each 
    image_Dict = {
        "contentStream": "",
        "publishedDate": ""
    }

    times = image_Times()
    res = versions_Release(times, image_Dict)


















    


