<link rel="stylesheet" href="../node_modules/bootstrap/dist/css/bootstrap.css">
<style>
    body {
        margin: 0 200px;
    }
    * {
        font-size: 16px;
    }
</style>

## `SQL Server`中`LEN`函数不包含尾随字符串

---

`SQL Server`中的`LEN`函数用于计算字符串中所含的字符数，
但是不包含尾随的空格数

```sql
LEN('1234') -- 4
LEN('1234   ') -- 4
```