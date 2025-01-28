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
        
    return grades





def find_Newest(times, res_vers, res_release, vcs_ref, fresh_grade):

    # first we are going to create our dictionary by merging the 5 lists
    # we are going to use zip(), loop, defaultdict() 
    solution = defaultdict(list)
    # then we are going to loop over the 5 lists simultaneously to create our new dictionary
    for a, b, c, d, e in zip(times, res_vers, res_release,vcs_ref, fresh_grade):
        solution[b].append((a,c,d,e))

    # converting to a set to remove duplicates in dictionary due to architecture e.g ppc64le, amd64 
    for main in solution:
        solution[main] = list(set(solution[main]))

    print("The merged key value dictionary is : " + str(dict(solution)))
    

    # here we are getting the most recent time for each key
    most_recent = {} 
    for main, entries in solution.items():
        # want to sort entries by time, which is the first element of the tuple 
        sorted_entries = sorted(entries, key=lambda x: datetime.fromisoformat(x[0]), reverse=True)
        most_recent[main] = sorted_entries[0]  # pick the most recent entry for the newest time for each version
    
    print("The most recent time entry for each key is:", most_recent)

    return most_recent

# final function to print our final answer
def printing(input_list):
    # create a new list for answer
    answer = []

    # convert Python to JSON  
    json_object = json.dumps(input_list, indent = 4) 
    print(json_object)



if __name__ == "__main__":  

    times = image_Times()
    res_vers = versions()
    res_release = release()
    vcs_ref = vcs_Ref()
    fresh_grade = fresh_Grade()
    
    comb_time_rel_vers = find_Newest(times, res_vers, res_release, vcs_ref, fresh_grade)

    printing(comb_time_rel_vers)


    


