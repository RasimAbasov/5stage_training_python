import re
from requests import post, get
from zeep import Client

url_rest = 'http://users.bugred.ru/tasks/rest/{}'
parameters_register = {'email': 'rasimabasov@gmail.com',
                       'name': 'rasimabasov',
                       'password': '1234567890'
                       }

# client = Client('http://users.bugred.ru/tasks/soap/WrapperSoapServer.php?wsdl')
# doRegisterRequest = client.service.doRegister(data)


# Rest
response_rest_get_user = get(url=url_rest.format("getuser"), params={"email": "rasimabasov@gmail.com"})
assert response_rest_get_user.status_code == 200, "Хреновый ответ"
reg = re.findall('"name":"rasimabasov"', response_rest_get_user.text)
print(reg)
if reg != ['"name":"rasimabasov"']:
    # создаем пользака через doregister
    response_register = post(url=url_rest.format("doregister"), data=parameters_register)
    assert response_register.status_code == 200, "Хреновый ответ"
    print(response_register.text)
    response_rest_get_user = get(url=url_rest.format("getuser"), params={"email": "rasimabasov@gmail.com"})
    print(response_rest_get_user.text)
if reg == ['"name":"rasimabasov"']:
    # удаляем пользака
    response_delete = post(url=url_rest.format("deleteuser"), data={"email": "rasimabasov@gmail.com"})
    assert response_delete.status_code == 200, "Хреновый ответ"
    print(response_delete.text)
    response_rest_get_user = get(url=url_rest.format("getuser"), params={"email": "rasimabasov@gmail.com"})
    reg = re.findall('"name":"rasimabasov"', response_rest_get_user.text)
    assert reg != ['"name":"rasimabasov"'], "Пользак не удалился"
# создаем пользака через doregister
response_register = post(url=url_rest.format("doregister"), data=parameters_register)
assert response_register.status_code == 200, "Хреновый ответ"
print(response_register.text)
response_rest_get_user = get(url=url_rest.format("getuser"), params={"email": "rasimabasov@gmail.com"})
print(response_rest_get_user.text)

# Это пример cUrl
# curl -i -X POST -H "Content-Type: application/json" -d "{\"email\": \"rasimabasov@gmail.com\", \"name\": \"rasimabasov\", \"password\": \"1234567890\"}" http://users.bugred.ru/tasks/rest/doregister