## RedHat6设置Oracle 11g R2开机启动

1. oracle用户登录，修改dbstart, dbshut文件：
   文件中的`ORACLE_HOME_LISTNER=$1`行改为`ORACLE_HOME_LISTNER=$ORACLE_HOME`

2. 切换root用户，修改oratab文件：
   文件格式为`<ORACLE_SID>:<ORACLE_HOME>:<N/Y>`，最后一栏表示是否开机启动，改为`Y`

3. 创建oracle服务：

   - `$ vim /etc/rc.d/init.d/oracle`，添加如下内容：
     
    ```
    # !/bin/bash
    # whoami
    # root
    # chkconfig: 345 51 49 
    # description: starts the oracle dabase deamons
    #
    #ORACLE_HOME=/opt/oracle
    ORACLE_OWNER=oracle

    ORACLE_DESC="Oracle 11g"

    ORACLE_LOCK=/var/lock/subsys/oracle11g

    case "$1" in

    'start')

    echo -n \"Starting ${ORACLE_DESC}:\"

    runuser - $ORACLE_OWNER -c '$ORACLE_HOME/bin/lsnrctl start'

    runuser - $ORACLE_OWNER -c '$ORACLE_HOME/bin/dbstart'

    runuser - $ORACLE_OWNER -c '$ORACLE_HOME/bin/emctl start dbconsole'

    touch ${ORACLE_LOCK}
    echo
    ;;

    'stop')

    echo -n "shutting down ${ORACLE_DESC}: "

    runuser - $ORACLE_OWNER -c '$ORACLE_HOME/bin/lsnrctl stop'

    runuser - $ORACLE_OWNER -c '$ORACLE_HOME/bin/dbshut'

    rm -f ${ORACLE_LOCK}
    echo
    ;;

    'restart')

    echo -n "restarting ${ORACLE_DESC}:"
    $0 stop
    $0 start
    echo
    ;;
    *)

    echo "usage: $0 { start | stop | restart }"

    exit 1
    esac

    exit 0
    ```

   - 添加执行权限：`$ chmod a+x /etc/rc.d/init.d/oracle`

   - `$ chkconfig oracle on`

> 参考链接：  
> <http://blog.itpub.net/29029866/viewspace-1702241/>  
> <http://www.cnblogs.com/mchina/archive/2012/11/27/2782993.html>

## RedHat6开机挂载分区

执行命令`df -h`查看当前分区挂载情况，有挂载在`/media`目录下的应该就是没有挂载的分区，
如下这种：

```
/dev/sda2             816G   13G  763G   2% /media/df7b2329-261b-41fb-bd3f-d46c90eb7a89
```

想要挂载分区的话直接执行命令`mount /dev/sda2 <mount-point>`挂载即可，
但是要想开机自动挂载的话，就需要修改`/etc/fstab`文件，
首先要获取到分区的UUID值

```
$ blkid /dev/sda2
df7b2329-261b-41fb-bd3f-d46c90eb7a89
```

其实可以看出来这个UUID就是之前`/media`目录下的挂载点目录名称，
然后在`/etc/fstab`文件中添加一行即可：

```
UUID=df7b2329-261b-41fb-bd3f-d46c90eb7a89  /mnt  ext4   defaults  1 1
```

其中UUID为之前查出来的分区UUID值，`/mnt`为需要挂载的目录名

> 参考链接：  
> <http://www.cnblogs.com/xia/archive/2011/01/30/1947706.html>  
> <http://www.cnblogs.com/chenmh/p/5097530.html>