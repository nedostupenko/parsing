import json
import  requests

# GitHub REST API
gh_user = 'nedostupenko'
url = f'https://api.github.com/users/{gh_user}/repos'

response = requests.get(url)
j_data = response.json()

# Saving in file
try:
    with open("gh_user_repos.json", 'w') as gh_user_repos:
        json.dump(j_data, gh_user_repos, indent=4)
except IOError:
    print("Произошла ошибка ввода-вывода!")

# Print results
print(f"У пользователя <{gh_user}> на портале {url[0:22]} находятся <{len(j_data)}> репозитория.")
print('Названия репозиториев:')
for no, el in enumerate(j_data, 1):
    print(no, el['name'])