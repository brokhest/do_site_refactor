import requests
import json
import re


class LoginClient(object):

    @staticmethod
    def login(username, password):
        url = "http://127.0.0.1:8000/login/"
        data = {
            "user": {
                "username": username,
                "password": password
            }
        }
        headers = {'Content-Type': "application/json", "Accept": "*/*"}
        res = requests.post(url, data=json.dumps(data), headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
            return data["token"]
        return 0

    @staticmethod
    def register(username, password):
        url = "http://127.0.0.1:8000/login/register/"
        data = {
            "user": {
                "username": username,
                "password": password
            }
        }
        headers = {'Content-Type': "application/json", "Accept": "*/*"}
        res = requests.post(url, data=json.dumps(data), headers=headers)
        if res.status_code == 201:
            data = json.loads(res.text)
            return data["user"]["token"]
        return 0


class TodoClient(object):


    @staticmethod
    def get_tasks(token):
        url = "http://127.0.0.1:8000/todo/task_list/"
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        res = requests.get(url, headers=headers)
        data = json.loads(res.text)
        return data

    @staticmethod
    def add_task(token, name, desc):
        url = "http://127.0.0.1:8000/todo/task_list/"
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        data = {
                "title": name,
                "desc": desc,
            }
        res = requests.post(url, data=json.dumps(data), headers=headers)
        if res.status_code == 201:
            return 1
        return 0

    @staticmethod
    def change_task(token, name, desc, comp, cat, pk):
        url = "http://127.0.0.1:8000/todo/task_list/" + str(pk)
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        data = {
                "title": name,
                "desc": desc,
                "completion": comp,
                "category": cat
            }
        res = requests.put(url, data=json.dumps(data), headers=headers)
        if res.status_code == 200:
            return 1
        return 0

    @staticmethod
    def delete_task(token, pk):
        url = "http://127.0.0.1:8000/todo/task_list/" + str(pk)
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        res = requests.delete(url, headers=headers)
        if res.status_code == 200:
            return 1
        return 0

    @staticmethod
    def get_categories(token):
        url = "http://127.0.0.1:8000/todo/category/"
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        res = requests.get(url, headers=headers)
        data = json.loads(res.text)
        return data

    @staticmethod
    def add_category(token, name):
        url = "http://127.0.0.1:8000/todo/category/"
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        data ={
            "name": name
        }
        res = requests.post(url, data=json.dumps(data), headers=headers)
        if res.status_code == 201:
            return 1
        return 0

    @staticmethod
    def change_category(token, new_name, name):
        url = "http://127.0.0.1:8000/todo/category/" + name
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        data ={
            "name": new_name
        }
        res = requests.put(url, data=json.dumps(data), headers=headers)
        if res.status_code == 200:
            return 1
        return 0

    @staticmethod
    def delete_category(token, name):
        url = "http://127.0.0.1:8000/todo/category/" + name
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        res = requests.delete(url, headers=headers)
        if res.status_code == 200:
            return 1
        return 0

    @staticmethod
    def get_category(token, name):
        url = "http://127.0.0.1:8000/todo/task_list/by_category/" + name
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        res = requests.get(url, headers=headers)
        data = json.loads(res.text)
        return data


class FileClient(object):

    @staticmethod
    def get_files(token):
        url = "http://127.0.0.1:8000/files"
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        res = requests.get(url, headers=headers)
        data = json.loads(res.text)
        return data

    @staticmethod
    def add_file(token, filename, public):
        url = "http://127.0.0.1:8000/files/"
        headers = {"Accept": "*/*", "Authorization": "Token " + token}
        public = "True" if public else "False"
        data = {
            "public": public
        }
        f = open(filename, "rb")
        files = {
            "file": f
        }
        res = requests.post(url, files=files, data=data, headers=headers)
        f.close()
        if res.status_code == 201:
            return 1
        return 0

    @staticmethod
    def change_file(token, name, permission, perm_to, keyword, public, pk):
        url = "http://127.0.0.1:8000/files/" + str(pk)
        headers = {"Accept": "*/*", "Authorization": "Token " + token}
        permission = "True" if permission else "False"
        perm_to = "True" if perm_to else "False"
        public = "True" if public else "False"
        data = {
            "name": name,
            "permission": permission,
            "permissioned_to": perm_to,
            "public": public,
            "keyword": keyword
        }
        res = requests.put(url, data=data, headers=headers)
        if res.status_code == 200:
            return 1
        return 0

    @staticmethod
    def delete_file(token, pk):
        url = "http://127.0.0.1:8000/files/" + str(pk)
        headers = {"Accept": "*/*", "Authorization": "Token " + token}
        res = requests.delete(url, headers=headers)
        if res.status_code == 200:
            return 1
        return 0

    @staticmethod
    def download_file(token, pk):
        url = "http://127.0.0.1:8000/files/download/" + str(pk)
        headers = {"Accept": "*/*", "Authorization": "Token " + token}
        res = requests.get(url, headers=headers)
        fname = re.findall('filename=(.+)', res.headers.get("content-disposition"))
        if len(fname) == 1:
            with open(fname[0], "w") as f:
                print(res.text, file=f)


class ForumClient(object):
    @staticmethod
    def get(token):
        url = "http://127.0.0.1:8000/forum"
        headers = {"Accept": "*/*", "Authorization": "Token " + token}
        res = requests.get(url, headers=headers)
        data = json.loads(res.text)
        return data

    @staticmethod
    def my_messages(token):
        url = "http://127.0.0.1:8000/forum/my_messages/"
        headers = {"Accept": "*/*", "Authorization": "Token " + token}
        res = requests.get(url, headers=headers)
        data = json.loads(res.text)
        return data

    @staticmethod
    def add_message(token, text):
        url = "http://127.0.0.1:8000/forum/my_messages/"
        headers = {'Content-Type': "application/json", "Accept": "*/*", "Authorization": "Token " + token}
        data = {
            "text":text
        }
        res = requests.post(url, data=json.dumps(data), headers=headers)
        if res.status_code == 201:
            return 1
        return 0

    @staticmethod
    def delete_message(token, pk):
        url = "http://127.0.0.1:8000/forum/my_messages/" + str(pk)
        headers = {"Accept": "*/*", "Authorization": "Token " + token}
        res = requests.delete(url, headers=headers)
        if res.status_code == 200:
            return 1
        return 0
