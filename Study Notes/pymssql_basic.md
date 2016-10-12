# Python连接SQL Server数据库 - pymssql使用基础

### 连接数据库

pymssql连接数据库的方式和使用sqlite的方式基本相同：

 - 使用`connect`创建连接对象
 - `connect.cursor`创建游标对象，SQL语句的执行基本都在游标上进行
 - `cursor.executeXXX`方法执行SQL语句，`cursor.fetchXXX`获取查询结果等
 - 调用`close`方法关闭游标`cursor`和数据库连接

```
import pymssql

# server    数据库服务器名称或IP
# user      用户名
# password  密码
# database  数据库名称
conn = pymssql.connect(server, user, password, database)

cursor = conn.cursor()

# 新建、插入操作
cursor.execute("""
IF OBJECT_ID('persons', 'U') IS NOT NULL
    DROP TABLE persons
CREATE TABLE persons (
    id INT NOT NULL,
    name VARCHAR(100),
    salesrep VARCHAR(100),
    PRIMARY KEY(id)
)
""")
cursor.executemany(
    "INSERT INTO persons VALUES (%d, %s, %s)",
    [(1, 'John Smith', 'John Doe'),
     (2, 'Jane Doe', 'Joe Dog'),
     (3, 'Mike T.', 'Sarah H.')])
# 如果没有指定autocommit属性为True的话就需要调用commit()方法
conn.commit()

# 查询操作
cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
row = cursor.fetchone()
while row:
    print("ID=%d, Name=%s" % (row[0], row[1]))
    row = cursor.fetchone()

# 也可以使用for循环来迭代查询结果
# for row in cursor:
#     print("ID=%d, Name=%s" % (row[0], row[1]))

# 关闭连接
conn.close()
```

> **注意**: 例子中查询操作的参数使用的`%s`而不是`'%s'`，**若参数值是字符串**，在执行语句时会自动添加单引号

### 游标使用注意事项

一个连接一次只能有一个游标的查询处于活跃状态，如下：

```
c1 = conn.cursor()
c1.execute('SELECT * FROM persons')

c2 = conn.cursor()
c2.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')

print( "all persons" )
print( c1.fetchall() )  # 显示出的是c2游标查询出来的结果

print( "John Doe" )
print( c2.fetchall() )  # 不会有任何结果
```

为了避免上述的问题可以使用以下两种方式：

 - 创建多个连接来保证多个查询可以并行执行在不同连接的游标上
 - 使用`fetchall`方法获取到游标查询结果之后再执行下一个查询， 如下：

```
c1.execute('SELECT ...')
c1_list = c1.fetchall()

c2.execute('SELECT ...')
c2_list = c2.fetchall()
```

### 游标返回行为字典变量

上述例子中游标获取的查询结果的每一行为元组类型，
可以通过在创建游标时指定`as_dict`参数来使游标返回字典变量，
字典中的键为数据表的列名

```
conn = pymssql.connect(server, user, password, database)
cursor = conn.cursor(as_dict=True)

cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
for row in cursor:
    print("ID=%d, Name=%s" % (row['id'], row['name']))

conn.close()
```

### 使用`with`语句（上下文管理器）

可以通过使用`with`语句来省去显示的调用`close`方法关闭连接和游标

```
with pymssql.connect(server, user, password, database) as conn:
    with conn.cursor(as_dict=True) as cursor:
        cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
        for row in cursor:
            print("ID=%d, Name=%s" % (row['id'], row['name']))
```

### 调用存储过程

**pymssql 2.0.0**以上的版本可以通过`cursor.callproc`方法来调用存储过程

```
with pymssql.connect(server, user, password, database) as conn:
    with conn.cursor(as_dict=True) as cursor:
        # 创建存储过程
        cursor.execute("""
        CREATE PROCEDURE FindPerson
            @name VARCHAR(100)
        AS BEGIN
            SELECT * FROM persons WHERE name = @name
        END
        """)

        # 调用存储过程
        cursor.callproc('FindPerson', ('Jane Doe',))
        for row in cursor:
            print("ID=%d, Name=%s" % (row['id'], row['name']))
```

> 参考连接： <http://pymssql.org/en/stable/pymssql_examples.html>