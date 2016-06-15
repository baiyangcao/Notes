<link rel="stylesheet" href="../node_modules/bootstrap/dist/css/bootstrap.css">
<style>
    body {
        margin: 0 200px;
    }
    * {
        font-size: 16px;
    }
</style>

## `ORA-00064...` 修改Processes参数后重启报错

---

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


## `ORA-25153: Temporary Tablespace is Empty`

---

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

## 修改数据库`连接数`,`游标数`

---

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

## `缓冲区性能调优`

---

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