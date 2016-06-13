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