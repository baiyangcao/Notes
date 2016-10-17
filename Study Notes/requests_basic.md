# requests快速入门

```
Requests 是唯一的一个非转基因的 Python HTTP 库，人类可以安全享用。

警告：非专业使用其他 HTTP 库会导致危险的副作用，包括：安全缺陷症、冗余代码症、重新发明轮子症、啃文档症、抑郁、头疼、甚至死亡。

Requests 允许你发送纯天然，植物饲养的 HTTP/1.1 请求，无需手工劳动。
```

## HTTP请求

requests模块针对不同的HTTP请求提供的相应的顶层方法，
包括：`get`, `post`, `put`, `delete`, `head`及`options`等

```python
>>> r = requests.get("http://httpbin.org/get")
>>> r = requests.post("http://httpbin.org/post")
>>> r = requests.put("http://httpbin.org/put")
>>> r = requests.delete("http://httpbin.org/delete")
>>> r = requests.head("http://httpbin.org/get")
>>> r = requests.options("http://httpbin.org/get")
```

这就是官方文档中所描述的`纯天然、无需手工劳动`的HTTP请求，
然后在这个基础上可以根据不同的需求添加不同的关键字参数。

### 传递URL参数 - `params`

关键字参数`params`用于传递URL参数，以一个字典对象来提供键值对参数

```python
>>> payload = {'key1': 'value1', 'key2': ['value2', 'value3'], 'key3': None}

>>> r = requests.get('http://httpbin.org/get', params=payload)
>>> print(r.url)
#http://httpbin.org/get?key1=value1&key2=value2&key2=value3
```

这里注意两点：

 - 字典里值为`None`的键不会被添加到URL中
 - 字典里值为数组的键会被拆分成多个同时添加到URL中，如上例中的key2

### Post数据 - `data`, `json`, `files`

一般在发起POST请求的时候会附加上一些要传送给服务器的数据，如表单，文件等。

 1. 对于表单形式的数据，只要简单的将一个字典传递给`data`参数

     ```python
     >>> payload = {'key1': 'value1', 'key2': 'value2'}
     >>> r = requests.post("http://httpbin.org/post", data=payload)
     # 通过抓包可以发现发起的HTTP请求中BODY部分就是已经编码的表单数据
     # key1=value1&key2=value2
     ```

    > 注： `data`参数也可以接受一个字符串参数直接发布出去。

 2. 有些服务接受JSON编码格式的数据，可以使用`json`参数

    ```python
    >>> r = requests.post("http://httpbin.org/post", json=payload)
    # 这是发送出去的HTTP请求中BODY部分就是JSON格式的字符串
    # {"key1": "value1", "key2": "value2"}
    ```

 3. 若是要上传文件数据，可以使用`files`参数

    ```python
    >>> files = {'file': open('report.xls', 'rb')}
    >>> r = requests.post("http://httpbin.org/post", files=files)
    ```
    
### 自定义请求头 - `headers`

通过`headers`参数提供的字典值自定义添加HTTP请求头信息，
如服务要求JSON数据格式，要求请求`Content-Type`为`application/json`

```python
headers = {'Content-Type':'application/json'}
r = requests.post(url, headers=headers, data=jsonstring)
```

> 注： 其实这个例子里的问题可以使用`json`参数来解决，
>     在使用`json`参数时会自动在请求头中添加`Content-Type: application/json`信息
>
>     requests.post(url, json=jsonstring)

### Cookies - `cookies`

要想要在发送请求时发送Cookies数据，可以使用`cookies`参数，
可以使用`requests.cookies.RequestCookieJar`来构建Cookies

```python
>>> jar = requests.cookies.RequestsCookieJar()
>>> jar.set('tasty_cookie', 'yum', site='httpbin.org', path='/cookies')
>>> jar.set('gross_cookie', 'blech', site='httpbin.org', path='/elsewhere')
>>> r = requests.get('http://httpbin.org/cookies', cookies=jar)
```

### 超时时间 - `timeout`

在请求时指定超时时间，若超过超时时间服务器没有响应，
则会抛出`requests.exceptions.Timeout`错误

## HTTP响应

请求方法返回的`Response`对象，可以通过响应码来确定响应状态，
并获取不同格式的响应内容（以下默认`r`为`Response`类型对象）

 - `r.status_code`属性可以用来获取响应码，如：200，万恶的404等
 - 响应内容可以获取文本、二进制、JSON等格式：
     + `r.text`返回unicode格式的字符串响应内容，
       其内容编码可以通过`r.encoding`属性来设置
     + `r.content`返回二进制格式的响应内容
     + `r.json`把响应内容当做JSON字符串来处理，解码后返回JSON对象
 - `r.cookes`可以获取响应中要设置的cookies 