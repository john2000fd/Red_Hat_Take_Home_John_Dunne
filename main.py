import requests
import json
from datetime import *
from collections import defaultdict 
 

# function to determine the published_date of each image
def image_Times():

    # API repository holding the Red Hat build of Keycloak’s container image history 
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
    print(dates)
    print("")
    print("")
    return dates



# function to determine the release of each image 
def release():
    # list to store release info
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
        
        # we then retrieve the 'labels' info              
        label_info = image_data.get('labels', [])

        # loop through the list of labels 
        for label in label_info:
            if label['name'] == 'release':     # set each version as a seperate entry in the list
                vers = label['value']
                release.append(vers)
            else:
                continue


    print(release)
    print("")
    print("")     
    return release




# function to determine the version of each image 
def versions():
    # list to store versions 
    version = []

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
        
        # we then retrieve the 'labels' info              
        label_info = image_data.get('labels', [])

        # loop through the list of labels 
        for label in label_info:
            if label['name'] == 'version':    # set each version as a seperate entry in the list
                vers = label['value']
                version.append(vers)
            else:
                continue


    print(version)        
    print("")
    print("")        
    return version


def vcs_Ref():
    vcs = []

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
        
        # we then retrieve the 'labels' info              
        label_info = image_data.get('labels', [])

        # loop through the list of labels 
        for label in label_info:
            if label['name'] == 'vcs-ref':    # set each version as a seperate entry in the list
                vers = label['value']
                vcs.append(vers)
            else:
                continue
    print(vcs)        
    print("")
    print("")        
    return vcs            



# function to retrieve freshness_grade of each image
def fresh_Grade():
    grades = []

    repository_images = "https://catalog.redhat.com/api/containers/v1/repositories/registry/registry.access.redhat.com/repository/rhbk/keycloak-rhel9/images"

    # Here we are doing a GET request to the red hat Keycloak repo
    repo_Response = requests.get(repository_images)

    # this deseriealizes the JSON to a python obj so we can read it 
    text = json.loads(repo_Response.text)

    # data is the key which holds all of the image's info
    image_info = text.get('data', [])
    # Loop through each image
    for info in image_info:
        fresh = info.get('freshness_grades', {})   #get freshness grade 
        for grade in fresh:
            if 'grade' in grade:    #if grade exists, we get the value and store it in a list 'grades'
                published_date = grade.get('grade')
                #adding to a list
                grades.append(published_date)
            else:
                print("error")
                break    
    print(grades)        
    print("")
    print("")        
    return grades





def find_Newest(times, res_vers, res_release, vcs_ref, fresh_grade):

    # first we are going to create our dictionary by merging the three lists: times, res_release, res_vers
    # we are going to use zip(), loop, defaultdict() 
    solution = defaultdict(list)
    # then we are going to loop over the 5 lists simultaneously to create our new dictionary
    for a, b, c, d, e in zip(times, res_vers, res_release,vcs_ref, fresh_grade):
        solution[a].append((b,c,d,e))

    #print("The merged key value dictionary is : " + str(dict(solution)))

    # converting to a set to remove duplicates in dictioanery due to architecture e.g ppc64le, amd64 
    for main in solution:
        solution[main] = list(set(solution[main]))

    print("The merged key value dictionary is : " + str(dict(solution)))




if __name__ == "__main__":

    # Here we have a dictionary used to store the info of each instance so we can determine the most recent image of each 
    image_Dict = {
        "contentStream": "",
        "publishedDate": ""
    }

    times = image_Times()
    res_vers = versions()
    res_release = release()
    vcs_ref = vcs_Ref()
    fresh_grade = fresh_Grade()
    
    comb_time_rel_vers = find_Newest(times, res_vers, res_release, vcs_ref, fresh_grade)


    


