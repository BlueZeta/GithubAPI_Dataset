import requests
import json
import csv
import time

counter = 0
print("How many repositories do you want?")
n = int(input())

masterList = []

headers = {'Authorization':'token AUTH-TOKEN'}

# First Url
repositories = requests.get("https://api.github.com/repositories", headers = headers)
# Next Url
next_url = repositories.links['next']['url']

tic = time.perf_counter()

while(counter < n):

    # 0 - 45
    total = len(repositories.json())-1
    
    for i in range(total):

        # check if we exceeded our limit
        if(counter >= n):
            break

        # reset our data list
        data = []

        # grab data
        id = repositories.json()[i]['id']
        repo_name = repositories.json()[i]['name']
        owner = repositories.json()[i]['owner']['login']
        repo_url = repositories.json()[i]['html_url']
        is_fork = repositories.json()[i]['fork']

        api_repo_url = repositories.json()[i]['url']
        request_repo_url = requests.get(api_repo_url, headers = headers)
        if request_repo_url.status_code == 200:
            size = request_repo_url.json()['size']
            if(request_repo_url.json()['language'] == None):
                language = "None"
            else:
                language = request_repo_url.json()['language']
            stars = request_repo_url.json()['stargazers_count']
            watchers = request_repo_url.json()['subscribers_count']
            forks = request_repo_url.json()['forks_count']
            issues = request_repo_url.json()['open_issues_count']
            if(request_repo_url.json()['license'] == None):
                legal_license = "None"
            else:
                legal_license = request_repo_url.json()['license']['name']
            created_date = request_repo_url.json()['created_at']
            updated_at = request_repo_url.json()['updated_at']

        # Add to master list
        data = [id, repo_name, owner, repo_url, is_fork, size, language, stars, watchers, forks, issues, legal_license, created_date, updated_at]
        masterList.append(data)

        # Update number of enteries collected
        counter += 1

    # Waits until API limit resets
    api_limit = requests.get("https://api.github.com/rate_limit", headers = headers)
    limit = api_limit.json()['resources']['core']['remaining']
    if(limit < 2):
        while(limit < 2):
            time.sleep(60)
            api_limit = requests.get("https://api.github.com/rate_limit", headers = headers)
            limit = api_limit.json()['resources']['core']['remaining']

    print(counter)

    # Head to next page
    repositories = requests.get(next_url, headers = headers)
    next_url = repositories.links['next']['url']

# Get Time
toc = time.perf_counter()
print(f"Get Requests finished in {toc - tic:0.4f} seconds")

# CSV File 
with open("GithubDataset.csv", 'a', encoding='utf-8', newline = '') as csvfile:

    writer =csv.writer(csvfile)
    Labels = ["ID", "Repo Name", "Owner", "Repo URL", "Is Forked", "Size", "Language", "Stars", "Watchers", "Forks", "Issues", "License", "Date Created", "Date Updated"]
    writer.writerow(Labels)

    for i in masterList:
        writer.writerow(i)

# Beta - Downloads count implementation
# downloads_url = repositories.json()[i]['downloads_url']
# request_downloads_url = requests.get(downloads_url)
# if request_downloads_url.status_code == 200:
#     print(request_downloads_url)
    # download_count = request_downloads_url.json()[count]["download_count"]

# Beta - Contributor Count Implementation
# countributor_url = repositories.json()[i]['contributors_url']
# request_countributor_count = requests.get(countributor_url)
# cont_next_url = request_countributor_count.links['next']['url']
# if request_countributor_count.status_code == 200:
#     get_total = len(request_countributor_count.json()) - 1
#     go_next = requests.get(cont_next_url)

# Next page
# https://api.github.com/repositories?since=id

# Future Ideas
# Finish implementing downloads count
# Finish implementing contributor count
# Works with csv

# Other Useful Code

# formats string for printing to console nicely
# json_formatted_str = json.dumps(repo_json.json(), indent=2)

# needs to start at 1
# file = open("repo_count.txt", "w")
# file.write(test.json()[1]['id'])
# for y in range(1, total):
#     file.write(user_repos.json()[y]['name']+'\n')
# file.close()

