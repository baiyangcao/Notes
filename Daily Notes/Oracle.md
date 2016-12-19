<!--<link rel="stylesheet" href="../node_modules/bootstrap/dist/css/bootstrap.css">-->

---

## `ORA-00064...` 修改Processes参数后重启报错

今天大黄蜂同学修改Oracle数据库的Processes参数后重启报这个错误

```sql
alter system set processes=300 scope=spfile;
```

```
ORA-00064: object is too large to allocate on this O/S
```

原因是因为修改了Processes参数过大，超出了系统能分配的最大值而报错，
虽然可以通过修改系统内核参数来解决，但是小生不懂，故只能选择把参数值调制正常范围(20-200)  

 - 首先要把数据库启动，因为直接启动使用spfile，报错，所以只能用pfile启动了：

     + 先来生成pfile，链接到数据库`sqlplus / as sysdba`，然后执行`create pfile from spfile`，
       即可根据spfile生成pfile，生成的pfile位于目录`$ORACLE_HOME/dbs/init[SID].ora`，
       一般是`initorcl.ora`，然后退出`exit`

     + 修改pfile的Processes参数值，打开`$ORACLE_HOME/dbs/initorcl.ora`文件，修改`processes=200`

     + 然后使用pfile启动数据库，链接数据库`sqlplus / as sysdba`，然后执行`startup pfile=$ORACLE_HOME/dbs/initorcl.ora`
       便可以启动数据库了

 - 然后，由于当前是用pfile启动的数据库，无法修改spfile参数，所以就直接用pfile生成spfile`create spfile from pfile`

 - 最会，重启数据库就是默认的使用spfile启动了`shutdownimmediate`，`startup`

---

## `ORA-25153: Temporary Tablespace is Empty`

故障定位

```sql
SQL> select * from v$tempfile;
no rows selected
```

看来是临时文件丢失的原因，似乎是因为**备份还原的时候导致的临时文件丢失，10g好像是有这样的一个bug**，添加一个临时文件即可

```sql
SQL> alter tablespace temp add tempfile '/u01/oracle/oradata/elvis/temp01.dbf';
Tablespace altered.
```

---

## 修改数据库`连接数`,`游标数`

Oracle中的`processes`参数表示`最大连接数`，`open_cursors`参数表示`游标数`，
如下可以查看系统中的最大连接数和游标数

```sql
SQL> show parameter processes;
50

SQL> show parameter open_cursors;
1000
```

可以使用如下命令修改`processes`和`open_cursors`参数值

```sql
SQL> alter system set processes=200 scope=spfile;

SQL> alter system set open_cursors=2000 scope=spfile;
```

> **注：** `processes`的可取值可以到pfile样例文件(一般在$ORACLE_HOME/db/init.ora)
> 中查看
> 
> ```
> processes = 50    #SMALL
> processes = 100   #MEDIIUM
> processes = 200   #LARGE
> ```
>
> 这里可以看出`processes`参数最大值可以取`200`，
> 最好不要超过这个值，否则就可能出现[`ORA-00064...` 修改Processes参数后重启报错]()的情况

<!-- -->

> ```sql
> -- 查看当前数据库连接数
> SQL> select * from v$session;
> 
> -- 查看当前数据库打开的游标
> SQL> select * from v$open_cursors;
> ```

---

## `缓冲区性能调优`

oracle 10g 修改SGA,PGA大小

 - 概念  
   `SGA指系统全局区域(System Global Area)`,是用于存储数据库信息的内存区，该信息为数据库进程所共享。
   `PGA指进程全局区域(Process Global Area)`,包含单个服务器进程或单个后台进程的数据和控制信息，与几个进程共享的SGA 正相反,PGA 是只被一个进程使用的区域，PGA 在创建进程时分配,在终止进程时回收。 Oracle 10g提供了PGA内存的自动管理。参数pga_aggregate_target可以指定PGA内存的最大值。当参数 pga_aggregate_target大于0时，Oracle将自动管理pga内存，并且各进程的所占PGA之和，不大于 pga_aggregate_target所指定的值。

 - 配置  
   oracle推荐OLTP(on-line Transaction Processing)系统oracle占系统总内存的80%,然后再分配80%给SGA,20%给PGA。也就是

```
SGA=system_total_memory*80%*80%
PGA=system_total_memory*80%*20%
```

 - 操作  
   用SYS用户以SYSDBA身份登录系统

```sql
SQL> alter system set sga_max_size=2000m scope=spfile;
SQL> alter system set sga_target=2000m scope=spfile;
SQL> alter system set pga_aggregate_target=500m scope=spfile;
```

   然后重新启动数据库
   最后查看一下是否生效

```sql
show parameter sga_max_size;
show parameter sga_target;
show parameter pga_aggregate_target;
```

---

## `ORA-12514:TNS:监听程序当前无法识别连接描述符中请求的服务_监听程序不支持服务`

今天大黄蜂同学重启虚拟机之后再链接数据库就报了这个错，先查看了一下监听的状态

```
C:> lsnrctl status
... ...
服务摘要..
服务 "CLRExtProc" 包含 1 个实例。
  实例 "CLRExtProc", 状态 UNKNOWN, 包含此服务的 1 个处理程序...
命令执行成功
```

监听中的服务并没有数据库实例`orcl`，检查了一下`listener.ora`文件，配置并没有问题，
怀疑是数据库启动时出了问题，导致监听并没有找到数据库服务，
为了连上数据库，在`listener.ora`文件中强制添加`orcl`的监听

```
SID_LIST_LISTENER =
  (SID_LIST =
    (SID_DESC =
      (SID_NAME = CLRExtProc)
      (ORACLE_HOME = D:\app\Administrator\product\11.2.0\dbhome_1)
      (PROGRAM = extproc)
      (ENVS = "EXTPROC_DLLS=ONLY:D:\app\Administrator\product\11.2.0\dbhome_1\bin\oraclr11.dll")
    )
    # 以下是添加部分
    (SID_DESC =
      (GLOBAL_DBNAME = ORCL)
      (ORACLE_HOME = D:\app\Administrator\product\11.2.0\dbhome_1)  
      (SID_NAME = ORCL)
    )
  )
```

然后重启监听，让监听可以识别`orcl`服务

```
C:> lsnrctl stop
... ...

C:> lsnrctl start
... ...
服务 "ORCL" 包含 1 个实例。
  实例 "ORCL", 状态 UNKNOWN, 包含此服务的 1 个处理程序...
命令执行成功
```

然后连接Oracle数据库，尝试重启数据库

```sql
C:> sqlplus sys/sys@127.0.0.1/orcl as sysdba
... ...

SQL> shutdown immediate;
ORA-01034 - Oracle not available
ORA-27101 - shared memory realm does not exist
```

网上大部分说是`ORACL_HOME`或`ORACLE_SID`问题，可惜并不适用，
后找到一篇说查看日志，日志路径位于`ORACLE_HOME\database\ORADIM.LOG`，
日志中找到数据库启动时的报错信息如下：

```
Tue Jun 21 15:10:17 2016
D:\app\Administrator\product\11.2.0\dbhome_1\bin\oradim.exe -startup -sid orcl -usrpwd *  -log oradim.log -nocheck 0 
Tue Jun 21 15:10:33 2016
ORA-00847: MEMORY_TARGET/MEMORY_MAX_TARGET and LOCK_SGA cannot be set together
```

继续查询报错信息`ORA-00847`，看起来是数据库系统参数设置的问题，先把`pfile`导出看一下

```
SQL> create pfile from spfile;
```

创建了之后宝宝傻眼了，不在`ORACLE_HOME/dbs`里啊！
后来经查才知原来Windows下`pfile`的默认生成路径和linux下不一样，位于`$ORACLE_BASE\admin\db_name\pfile`
然后打开`pfile`注释掉`MEMORY_TARGET`参数的设置

```
...
# memory_target=898629632
...
```

然后从`pfile`启动数据库，根据`pfile`生成`spfile`

```sql
SQL> startup pfile='D:\app\Administrator\admin\orcl\pfile\init.ora.115201614250';

SQL> create spfile from pfile='D:\app\Administrator\admin\orcl\pfile\init.ora.115201614250';
```

然后便可以重启数据库了，最后将`listener.ora`还原，重启服务器，再查看监听状态就可以看到`orcl`服务正常了

```
C:> lsnrctl status

... ...
服务摘要..
服务 "CLRExtProc" 包含 1 个实例。
  实例 "CLRExtProc", 状态 UNKNOWN, 包含此服务的 1 个处理程序...
服务 "ORCL" 包含 1 个实例。
  实例 "orcl", 状态 READY, 包含此服务的 1 个处理程序...
服务 "orclXDB" 包含 1 个实例。
  实例 "orcl", 状态 READY, 包含此服务的 1 个处理程序...
命令执行成功
```


> 参考链接：  
> 1. [连接本地Oracle 11g时 ORA-12514:TNS:监听程序当前无法识别连接描述符中请求的服务](http://www.cnblogs.com/lz-wolf/archive/2012/11/15/2771266.html)  
> 2. [解决连接Oracle 11g报ORA-01034和ORA-27101的错误](http://www.linuxidc.com/Linux/2012-05/59790.htm)  
> 3. [pfile和spfile全攻略](http://wenku.baidu.com/link?url=dZK2zvpnXAgoaQRxexRFOHWyZTRlFWks0oef08VrNqFBDJsQ35ycJ2ZrqsJF5SSpYjgGHim4JEP908sa54AWCKRfubP-WPsC_2_by4STqyW)  
> 4. [oracle错误实践之一：ora-00847](http://blog.sina.com.cn/s/blog_7e662b4a0100vbpg.html)

---

## `ORA-25153`: Temporary Tablespace is Empty

今天在Oracle数据库上进行查询时报错：

```
`ORA-25153`: Temporary Tablespace is Empty
```

### 原因排查：

 1. 用户临时表空间是否指定：
   
```
SQL> select username,temporary_tablespace from dba_users where username='<username>';
```
   
   查询到结果为`TEMP`表空间

  2. 查询表空间是否为ONLINE：

```
SQL> select tablespace_name, file_name from dba_temp_files;
```

    查询结果为ONLINE

  3. 查询是否指定表空间数据文件：

```
SQL> select tablespace_name, file_name from dba_temp_files;
```

    没有查询到结果，说明没有指定的表空间文件

### 解决办法：

为表空间添加对应的数据文件，首先查找当前数据库中数据文件的存放位置：

```
SQL> select name from v$datafile;
```

随意找一个就可以，一般数据文件都会放在同一个目录下，然后为`TEMP`临时表空间添加数据文件：

```
SQL> alter tablespace TEMP add datafile '<dir>/temp.dbf';
```

---

##  数据库连接DBLink

 1. 创建数据库连接

```
CREATE [PUBLIC] DATABASE LINK {link name}
CONNECT TO {username} IDENTIFIED BY {password}
USING {connection string/tns name} 
```

其中`USING`关键词后面可以是数据库服务器上配置的`TNS name`服务命名，
或者是在`tnsname.ora`中配置的服务命名对应的连接字符串，如：
`(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.0.78)(PORT = 1521)) ) (CONNECT_DATA = (SERVICE_NAME = orcl) ) )`

 2. 删除数据库连接：

```
DROP PUBLIC DATABASE LINK {link name}
```

 3. global_names
 
 如果数据库参数global_names设置为true，则必须数据库连接的名称{link name}
 必须与远程数据库GLOBAL_NAME相同。  
   
 global_names参数可以通过`show parameter global_names`得到，
 而远程服务器的GLOBAL_NAME可以通过执行SQL语句
 `SELECT * FROM GLOBAL_NAME`获得。  
  
 当global_names设置为false时，不可以在本地调用远程服务器中不存在
 的函数，不仅仅是自定义函数，`UTL_RAW.CAST_TO_RAW`函数也不可以

---

## 编译存储过程报错`PLS-00201: identifier 'XXXX.XXX' must be declared`

创建存储过程的编译过程中报错：

```
PLS-00201: identifier 'XXXX.XXX' must be declared
```

这是由于在存储过程中调用了其他用户的对象，但是当前用户权限不足所导致，
只要为用户添加的`ADMIN`权限即可，虽然有些权限已经通过角色授予，
但是并不能满足操作其他用户的权限，所以需要重新授予权限。  
  
如下，授予当前用户执行存储过程的权限：

```
GRANT EXECUTE ANY PROCEDURE TO XXXX WITH ADMIN OPTION;
```

其中XXXX为当前用户名，**注意：一定要带上`WITH ADMIN OPTION`选项`

---

## 更新少量数据也异常的慢（锁处理）

更新少量数据时也异常缓慢，怀疑是对象被锁，执行语句查询当前数据库上锁的对象：

```

SELECT l.session_id sid, s.serial#, l.locked_mode, l.oracle_username,
  l.os_user_name, s.machine, s.terminal, o.OBJECT_Name, s.logon_time
FROM v$locked_object l, all_objects o, v$session s
WHERE l.OBJECT_ID = o.OBJECT_ID
  AND l.session_id = s.sid
  ORDER BY sid, s.serial#;
```

然后关闭对应的进程即可：

```
ALTER SYSTEM KILL SESSION 'sid,serial#';
```

---

## Oracle查询表结构

通过Oracle中的用户表来查询相关信息，`user_tab_cols`, 
`user_col_comments`, `user_constraints`, `user_cons_columns`  
  
 - `user_tab_cols` 用来获取用户表的列信息
 - `user_col_comments` 用来获取对应用户表列的注释
 - `user_constraints` 用来获取用户表的约束条件
 - `user_cons_columns` 获取约束中用户可访问的列

如查询用户所有表的列及相关注释

```
SELECT a.TABLE_NAME AS 表名, a.COLUMN_NAME AS 列名, a.DATA_TYPE AS 数据类型,
  a.DATA_LENGTH AS 长度, a.NULLABLE AS 可空, b.COMMENTS AS 注释
FROM user_tab_columns a
  LEFT JOIN user_col_comments b
    ON a.TABLE_NAME = b.TABLE_NAME
      AND a.COLUMN_NAME = b.COLUMN_NAME
ORDER BY a.TABLE_NAME, a.COLUMN_ID
```

---

## ORACLE赋予用户权限

基本语法：

```
-- 赋予用户、角色权限
GRANT {PRIVS, ...} TO {USER/ROLE};

-- 收回用户、角色权限
REVOKE {PRIVS, ...} FROM {USER/ROLE};
```

其中权限如基本的`CREATE SESSION`, `SELECT ANY TABLE`,
`INSERT ANY TABLE`等。  
  
若是要赋予用户对另一个用户的操作权限，可以加上`ON`语法，如：

```
-- 为SYCHY用户赋予SYBDC用户下FOO表的选择、插入、删除权限
GRANT SELECT, INSERT, UPDATE ON SYBDC.FOO TO SYCHY;
```

或者要赋予用户对另一个用户的指定列的更新操作，可以使用`UPDATE({COLUMN_NAME})`语法，如：

```
-- 为SYCHY用户赋予SYBDC用户下TEST表的更新TESTCOLUMN列的权限
GRANT UPDATE(TESTCOLUMN) ON SYBDC.TEST TO SYCHY;
```

---

## 设置定时任务job

创建定时任务job，使用`DBMS_JOB.SUBMIT`存储过程创建，同时返回一个`jobid`参数

```
PROCEDURE Submit(job OUT binary_ineger, What IN varchar2, next_date IN date, 
  interval IN varchar2, no_parse IN boolean:=FALSE)
```

 - `job` 为返回参数，表示定时任务在数据库中的唯一标识
 - `What` 表示在任务执行时将要被执行的PL/SQL代码块
 - `next_date` 表示执行任务的时间
 - `interval` 表示定时执行任务的时间间隔
 - `no_parse` 表示执行语法分析的时间，FALSE表示立即执行语法分析，TRUE表示在第一次执行时进行语法分析

```
DECLARE
  jobid NUMBER;
BEGIN
  DBMS_JOB.SUBMIT(jobid, 'DATAEXPORT;', TO_DATE('2016-11-27', 'yyyy-MM-dd'), 'TRUNC(SYSDATE+1)');
END;
```

表示在2016-11-27凌晨0点执行存储过程DATAEXPORT，并且以后每天执行一次。
  
另外，可以是`DBMS_JOB.REMOVE`方法删除job，使用`DBMS_JOB.RUN`手动执行job，
这两个存储过程都需要一个`job`参数，为创建job时所产生的唯一标识。  
  
如果要查看当前系统中存在的job，可以使用如下表:

```
SELECT * FROM dba_jobs;
SELECT * FROM all_jobs;
SELECT * FROM user_jobs;
-- 查看正在执行的job
SELECT * FROM dba_jobs_running;
```

---

## ORA-24247 网络访问被访问控制列表(ACL)拒绝

使用`utl_http.request(url)`函数发起HTTP请求报错，原因是没有设置ACL，
进行如下设置：

```
BEGIN
  -- 创建ACL
  DBMS_NETWORK_ACL_ADMIN.create_acl(acl => 'httprequestpermission.xml',
                                    description => 'Normal Access',
                                    -- 要授权的角色
                                    principal => 'CONNECT',
                                    is_grant => TRUE,
                                    -- PRIVILEGE需要大写
                                    PRIVILEGE => 'connect',
                                    start_date => NULL,
                                    end_date => NULL);
  -- 一定要提交                                 
  COMMIT;
  dbms_network_acl_admin.assign_acl(acl => 'httprequestpermission.xml',
                                    host => '192.168.5.*',
                                    lower_port => 80,
                                    upper_port => NULL);
  COMMIT;  
  DBMS_NETWORK_ACL_ADMIN.add_privilege(acl => 'httprequestpermission.xml',
                                       -- 要赋予访问权限的用户或角色
                                       principal => 'SYBDCSXK',
                                       is_grant => TRUE,
                                       privilege => 'connect',
                                       start_date => NULL,
                                       end_date => NULL);
  COMMIT;
END;
```

---

## `ORA-04062`: timestamp of procedure "" has been changed

原因： 尝试执行已经过期的远程存储过程；

解决办法： 重新编译调用存储过程；

例：本地存储过程A调用远程存储过程B，首次编译A的时候并不会报错，
然后编译B，之后再次编译A的时候就会报错，原因是A中保存的B编译的时间戳与当前B的编译时间不符，
所以只要重新编译A存储过程即可。

---

## `ORA-02064`：不支持分布式操作

原因：调用的远程存储过程中使用了COMMIT，ROLLBACK等操作；

解决办法：使用Oracle自治事务来解决，如下：

```
-- 在BEGIN...END之前添加这句话即可
PRAGMA AUTONOMOUS_TRANSACTION;
BEGIN
END;
```

---

## 发起Http Post请求

```
DECLARE
  data VARCHAR2(8000);
  req UTL_HTTP.REQ;
  resp UTL_HTTP.RESP;
  bresult BLOB;
BEGIN
    req := UTL_HTTP.BEGIN_REQUEST(url => url, method => 'POST');
    UTL_HTTP.SET_HEADER(r => req, name => 'Content-Type', value => 'application/x-www-form-urlencoded');
    UTL_HTTP.SET_HEADER(r => req, name => 'Content-Length', value => LENGTHB(data));
    UTL_HTTP.WRITE_RAW(r => req, data => UTL_RAW.CAST_TO_RAW(CONVERT(data, 'UTF8')));
    resp := UTL_HTTP.GET_RESPONSE(req);
    UTL_HTTP.READ_RAW(resp, bresult);
    result := UTL_RAW.CAST_TO_VARCHAR2(bresult);
    UTL_HTTP.END_RESPONSE(resp);
  EXCEPTION
    WHEN UTL_HTTP.END_OF_BODY THEN
      UTL_HTTP.END_RESPONSE(resp);
  END;
```

这里有些需要注意的问题：

 - 使用`WRITE_RAW/READ_RAW`方法设置和读取数据，而不是`WRITE_TEXT/READ_TEXT`方法，
   因为后者会把字符串转换成服务器的字符集，而我们一般的请求Request的编码为UTF-8

 - 声明的变量类型应该是`VARCHAR2`而不是`NVARCHAR2`，否则在后台webservice中获取到的英文字符会自动补上`\0`，
   如`data`变量值为`BZF=A`到了后台中获取的为`\0B\0Z\0F=\0A`，
   这是因为`NVARCHAR2`中的字符都是以中文字符的形式保存，而对于英文字符则会自动补`\0`，
   这也就是为什么在`NVARCHAR2(10)`中可以保存十个中文字符或十个英文字符了。

---

## `ORU-10027:` buffer overflow, limit of 2000 bytes

使用`DBMS_OUTPUT.PUT_LINE`输出日志信息时报错：

```
ORA-20000: ORU-10027: buffer overflow, limit of 2000 bytes
ORA-06512: at "SYS.DBMS_OUTPUT", line 35
...
```

这是因为要输出到控制台的大小超出了缓存大小，所以需要设置一下缓存大小，
使用如下语句：

```
-- 设置缓存大小为40000
DBMS_OUTPUT.ENABLE(buffer_size => 40000);

-- 不设置缓存大小
DBMS_OUTPUT.ENABLE(buffer_size => null);
```