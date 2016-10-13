<link rel="stylesheet" href="../node_modules/bootstrap/dist/css/bootstrap.css">

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