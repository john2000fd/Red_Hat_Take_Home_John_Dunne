import requests
import json
from datetime import *
from collections import defaultdict 
 



# function to determine the published_date of each image
def image_Times(text):

    
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
def release(text):
    # list to store release info
    release = []

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
def versions(text):
    # list to store versions 
    version = []

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






def vcs_Ref(text):
    
    # list to store the vcs-ref values 
    vcs = []

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
def fresh_Grade(text):
    # list to store the grade values
    grades = []

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

    print()    
    return grades




# function to determine what our most recent image in each content stream is 

def find_Newest(times, res_vers, res_release, vcs_ref, fresh_grade):

    # first we are going to create our dictionary by merging the 5 lists
    # we are going to use zip(), loop, defaultdict() 
    solution = defaultdict(list)
    # then we are going to loop over the 5 lists simultaneously to create our new dictionary
    for a, b, c, d, e in zip(times, res_vers, res_release,vcs_ref, fresh_grade):
        solution[b].append((a,c,d,e))

    # converting to a set then back to a list to remove duplicates in dictionary due to architecture e.g ppc64le, amd64 
    for main in solution:
        solution[main] = list(set(solution[main]))
    

    # here we are getting the most recent time for each key 22, 26.0, 24
    most_recent = {}  #use an empty dictionary
    for main, entries in solution.items():
        # want to sort entries by time, which is the first element of the tuple 
        sorted_entries = sorted(entries, key=lambda x: datetime.fromisoformat(x[0]), reverse=True)
        most_recent[main] = sorted_entries[0]  # pick the most recent entry for the newest time for each version

    return most_recent



# final function to print our final answer
def printing(input_list):
    # create a new list for answer
    answer = []
    # loop over our inputted dictionary using the key value pair x,y
    for x, y in input_list.items():
        dict = {
            "contentStream": x,   # x is our key, y are our values
            "vcsRef": y[2],
            "publishedDate": y[0],
            "freshnessGrade": y[3]
        }
        # insted of just converting one, make sure to loop over the dictionary values to get all 3
        answer.append(dict)
    # convert Python to JSON, indent 4 for pretty printing   
    json_answer= json.dumps(answer, indent = 4) 
    print(json_answer)





# main function of the program
if __name__ == "__main__":  

    #API repository holding the Red Hat build of Keycloak’s container image history 
    repository_images = "https://catalog.redhat.com/api/containers/v1/repositories/registry/registry.access.redhat.com/repository/rhbk/keycloak-rhel9/images"

    #Here we are doing a GET request to the red hat Keycloak repo
    repo_Response = requests.get(repository_images)

    # Testing to make sure we are getting a successful call
    # As the status code we receive is 200, we know the server successfully processed the request and returned 200
    print(repo_Response.status_code)

    # this deseriealizes the JSON to a python obj so we can read it, and feed it to our functions for evaluation
    # we pass this to our evaluation functions to isolate information we need such as version and release
    text = json.loads(repo_Response.text)

    # Getting published_date of each image
    times = image_Times(text)
    # function to determine the version of each image 
    res_vers = versions(text)
    # function to determine the release of each image 
    res_release = release(text)
    # function to determine the vcs_Ref of each image
    vcs_ref = vcs_Ref(text)
    # function to determine the freshness_grade of each image
    fresh_grade = fresh_Grade(text)
    
    # function to determine our newest image in each content stream is 
    comb_time_rel_vers = find_Newest(times, res_vers, res_release, vcs_ref, fresh_grade)

    # function to print our final answer
    printing(comb_time_rel_vers)


    


