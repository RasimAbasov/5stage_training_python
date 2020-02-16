import requests
from requests import get
from requests.auth import HTTPBasicAuth
import json

# создали в jira два бага TEST-4037 TEST-4057
url = 'https://testbase.atlassian.net/rest/api/3/issueLink/12210'

auth = HTTPBasicAuth("mail.for.testbase@yandex.ru", "cCehOzIeIcisnqaCzBKQ1E53")

headers = {
    "Accept": "application/json",
    "referrer": "https://yandex.ru/"
}

response = get(url=url, headers=headers, auth=auth)
assert response.status_code == 200, "Хреновый ответ"

# можно так отправить
# response = requests.request(
#                               "GET",
#                               url,
#                               headers=headers,
#                               auth=auth
#                            )
print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

# Check response headers
response_headers = response.headers
assert response_headers['Content-Type'] == 'application/json;charset=UTF-8', "Не совпадает заголовок Content-Type"
assert response_headers['Content-Encoding'] == 'gzip', "Не совпадает заголовок Content-Encoding"
assert response_headers['Connection'] == 'keep-alive', "Не совпадает заголовок Connection"
assert response_headers['Transfer-Encoding'] == 'chunked', "Не совпадает заголовок Transfer-Encoding"
assert response_headers['Cache-Control'] == 'no-cache, no-store, no-transform', "Не совпадает заголовок Cache-Control"
assert response_headers['Server'] == 'AtlassianProxy/1.15.8.1', "Не совпадает заголовок Server"

#  Вопрос: откуда пришел запрос с основного сайта или по реферальной ссылке или через прокси сервер.
#  несовсем понял, как это проверять, по заголовку "referrer": "https://yandex.ru/" ?

# Check requests headers
requests_headers = response.request.headers
assert requests_headers['Accept-Encoding'] == 'gzip, deflate', "Не совпадает заголовок Accept-Encoding"
assert requests_headers['Accept'] == 'application/json', "Не совпадает заголовок Accept"
assert requests_headers['Connection'] == 'keep-alive', "Не совпадает заголовок Connection"
print("User-Agent: ", requests_headers['User-Agent'])
print("referrer:", requests_headers['referrer'])
