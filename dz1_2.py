import random
import re
from requests import post, get
from zeep import Client

url_rest = 'http://users.bugred.ru/tasks/rest/{}'
url_soap = 'http://users.bugred.ru/tasks/soap/WrapperSoapServer.php'
parameters_register = {'email': 'rasimabasov@gmail.com',
                       'name': 'rasimabasov',
                       'password': '1234567890'
                       }

# client = Client('http://users.bugred.ru/tasks/soap/WrapperSoapServer.php?wsdl')
# doRegisterRequest = client.service.doRegister(data)


# Rest

def test_doregister_rest():
    response_rest_get_user = get(url=url_rest.format("getuser"), params={"email": "rasimabasov@gmail.com"})
    assert response_rest_get_user.status_code == 200, "Хреновый ответ"
    reg = re.findall('"name":"rasimabasov"', response_rest_get_user.text)
    print(reg)
    if reg != ['"name":"rasimabasov"']:
        # создаем пользака через doregister
        response_register = post(url=url_rest.format("doregister"), data=parameters_register)
        assert response_register.status_code == 200, "Хреновый ответ"
        print(response_register.json())
        response_rest_get_user = get(url=url_rest.format("getuser"), params={"email": "rasimabasov@gmail.com"})
        print(response_rest_get_user.json())
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
    print(response_register.json())
    response_rest_get_user = get(url=url_rest.format("getuser"), params={"email": "rasimabasov@gmail.com"})
    print(response_rest_get_user.json())

# Это пример cUrl
# curl -i -X POST -H "Content-Type: application/json" -d "{\"email\": \"rasimabasov@gmail.com\", \"name\": \"rasimabasov\", \"password\": \"1234567890\"}" http://users.bugred.ru/tasks/rest/doregister


# SOAP
def test_doregister_soap():
    # headers = {'content-type': 'text/xml'}
    rand = random.randint(100, 500)
    xml = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wrap="http://foo.bar/wrappersoapserver">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <wrap:doRegister>
                         <email>soap_{rand}@mail.ru</email>
                         <name>soap_{rand}</name>
                         <password>soap_{rand}</password>
                      </wrap:doRegister>
                   </soapenv:Body>
                </soapenv:Envelope>"""
    response = post(url=url_soap, data=xml)
    print(response.content)
    response_rest_get_user = get(url=url_rest.format("getuser"), params={"email": f"soap_{rand}@mail.ru"})
    print(response_rest_get_user.json())


test_doregister_soap()
# test_doregister_rest()
