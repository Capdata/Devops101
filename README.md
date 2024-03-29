# Devops101
(Repo for Devops 101 for DBAs training)

# PREREQS
- 1 github public repo per student (provision for 6 students) with original script, v1.0, MASTER branch only
- 1 EC2 Ubuntu 20.04 / student with each :
  - 1 40Gb GP3 volume mounted on /var/lib/docker
  - 1 40Gb GP3 volume for ZFS storage pool
  - ZFS tools and storage pool of 40Gb
  - lxd setup using ZFS
  - 3 x Ubuntu 20.04 LXD vanilla containers, stopped [ub1, ub2, ub3]
  - student user account with sudo privileges
  - Docker setup
  - Git client
  - Directory : /home/student
  - Internet access 
  - Python3 & pip3

# LAB 1 : GIT 
- Configure git :
<pre>
$ su - student
$ cd ~/FORMATION/DEVOPS101/GIT
$ git config --global user.name "students-capdata" # <-- put your name in here
$ git config --global user.email "students@capdata-osmozium.com" # <-- put your email in here
$ git config --list
user.name=students-capdata
user.email=students@capdata-osmozium.com
</pre>
- Clone repository :
A user token will be given to you during the training. It will be referred as TOKEN in the docs... Your student number will be referred as [1-6], eg devops_student[1-6], devops_student2, etc... 
<pre>
$ git clone https://students-capdata:TOKEN@github.com/Capdata/devops_student[1-6].git
Cloning into 'devops_student[1-6]'...
remote: Enumerating objects: 30, done.
remote: Counting objects: 100% (30/30), done.
remote: Compressing objects: 100% (25/25), done.
remote: Total 30 (delta 4), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (30/30), 8.43 KiB | 1.05 MiB/s, done.
</pre>
- Navigate the local files:
<pre>
$ tree devops_student[1-6]/
devops_student[1-6]/
├── README.md
└── student[1-6]
    ├── README.md
    ├── dockerfiles
    │   ├── README.md
    │   └── my.cnf
    ├── my
    │   ├── cs.xml
    │   ├── myGetVersion.py
    │   └── myconnect.py
    ├── my_healthcheck.py
    └── sql
        ├── 1_sakila-schema.sql
        ├── 2_sakila-data.sql
        └── README.md

</pre>
<ol>
  <li>my_healthcheck.py : is the main program</li>
  <li>my/cs.xml : is the connection string configuration file</li>
  <li>my/myGetVersion.py : just a simple SQL code definition for getting version in MySQL, host of myGetVersion class</li>
  <li>my/myconnect.py: where the MySQL connection happens, host of alldbmyconnection class, requires MySQLdb PIP package</li>
</ol>
 
- Create a new branch called MYSQL_1, and in the context of this new branch, modify the my.cs.xml file to reflect the correct connection string parameters (given by the trainer)    
<pre>
$ cd ~/FORMATION/DEVOPS101/GIT/devops_student[1-6]

$ git branch -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main

$ git branch MYSQL_1

$ git branch -a
  MYSQL_1
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main

$ git checkout MYSQL_1
Switched to branch 'MYSQL_1'

$ git branch -a
* MYSQL_1
  main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main

$ vi student[1-6]/my/cs.xml    
(...)
</pre>

- add new directory and files, and commit to the local repo:

<pre>
$ git add --all

$ git status
On branch MYSQL_1
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   student[1-6]/my/cs.xml

$ git commit -m "changing connection string parameters..."
[MYSQL_1 277aec0] changing connection string parameters...
 1 file changed, 5 insertions(+), 5 deletions(-)

$ git status
On branch MYSQL_1
nothing to commit, working tree clean
</pre>

- Check if local repo is up to date and push local branch to remote repo:
<pre>
$ git pull origin main
From https://github.com/Capdata/devops_student[1-6]
 * branch            main       -> FETCH_HEAD
Already up to date.

$ git push origin MYSQL_1 
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 623 bytes | 623.00 KiB/s, done.
Total 5 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
remote:
remote: Create a pull request for 'MYSQL_1' on GitHub by visiting:
remote:      https://github.com/Capdata/devops_student[1-6]/pull/new/MYSQL_1
remote:
To https://github.com/Capdata/devops_student[1-6].git
 * [new branch]      MYSQL_1 -> MYSQL_1
</pre>

- Disconnects from the host
<pre>exit</pre>

# LAB 2 : DOCKER
- Connect to the host as student user and check that the current GIT branch under ~/FORMATION/DEVOPS101/GIT/devops_student[1-6] is MYSQL_1:
<pre>
$ su - student
$ cd ~/FORMATION/DEVOPS101/GIT/devops_student[1-6]
$ git checkout MYSQL_1
Switched to branch 'MYSQL_1'
$ git branch -a
* MYSQL_1
  main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main
</pre>

- Under student[1-6]/dockerfiles, create a new Dockerfile to build a custom MySQL image using the following parameters and details in the training manual:
<ol>
  <li>Version : 8-debian</li>
  <li>additionnal packages to install : vim</li>
  <li>Create Data Directory : /mysqldata</li>
  <li>Mount Docker Volume /mysqldata</li> 
  <li>Mount student[1-6]/sql local git directory to the docker entry point</li>
  <li>Copy student[1-6]/etc/my.cnf local git file into the container's /etc/mysql</li>
</ol>
... and use also the information as per the student[1-6]/my/cs.xml to expose TCP port, set username, password and database environment variables. 
<pre>
$ cd student[1-6]/dockerfiles
$ vi Dockerfile
(...)
FROM mysql:8-debian
RUN apt-get update && apt-get install -y vim && apt-get install -y wget
RUN mkdir /mysqldata
VOLUME /mysqldata
COPY my.cnf /etc/mysql/conf.d/my.cnf
ADD sql/ /docker-entrypoint-initdb.d
ENV MYSQL_ROOT_PASSWORD=*****
ENV MYSQL_DATABASE=*****
EXPOSE ****/tcp
CMD ["mysqld"]
</pre>
- Build the image
<pre>
$ sudo docker build -t student[1-6]/mysqlserver .
[+] Building 21.5s (10/10) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                        
 => transferring dockerfile: 305B                                                                                                                                           
 => [internal] load .dockerignore                                                                                                                                           
 => => transferring context: 2B                                                                                                                                             
 => [internal] load metadata for docker.io/library/mysql:8-debian                                                                                                           
 => [1/5] FROM docker.io/library/mysql:8-debian@sha256:49f4fcb0087318aa1c222c7e8ceacbb541cdc457c6307d45e6ee4313f4902e33                                                     
 => resolve docker.io/library/mysql:8-debian@sha256:49f4fcb0087318aa1c222c7e8ceacbb541cdc457c6307d45e6ee4313f4902e33 
(...)

$ sudo docker image ls
REPOSITORY             TAG       IMAGE ID       CREATED         SIZE
student[1-6]/mysqlserver   latest    01e39e90335d   4 minutes ago   659MB
</pre> 

- Observe the contents and layers of the image created 
<pre>
$ sudo docker image history student[1-6]/mysqlserver
IMAGE          CREATED          CREATED BY                                      SIZE      COMMENT
01e39e90335d   15 minutes ago   CMD ["mysqld"]                                  0B        buildkit.dockerfile.v0
<missing>      15 minutes ago   EXPOSE map[3306/tcp:{}]                         0B        buildkit.dockerfile.v0
<missing>      15 minutes ago   ENV MYSQL_DATABASE=mysql                        0B        buildkit.dockerfile.v0
<missing>      15 minutes ago   ENV MYSQL_ROOT_PASSWORD=capdata                 0B        buildkit.dockerfile.v0
<missing>      15 minutes ago   ADD sql/ /docker-entrypoint-initdb.d # build…   3.38MB    buildkit.dockerfile.v0
<missing>      15 minutes ago   COPY my.cnf /etc/mysql/conf.d/my.cnf # build…   70B       buildkit.dockerfile.v0
<missing>      15 minutes ago   VOLUME [/mysqldata]                             0B        buildkit.dockerfile.v0
<missing>      15 minutes ago   RUN /bin/sh -c mkdir /mysqldata # buildkit      0B        buildkit.dockerfile.v0
<missing>      15 minutes ago   RUN /bin/sh -c apt-get update && apt-get ins…   54.5MB    buildkit.dockerfile.v0
<missing>      6 days ago       /bin/sh -c #(nop)  CMD ["mysqld"]               0B
<missing>      6 days ago       /bin/sh -c #(nop)  EXPOSE 3306 33060            0B
<missing>      6 days ago       /bin/sh -c #(nop)  ENTRYPOINT ["docker-entry…   0B
<missing>      6 days ago       /bin/sh -c ln -s usr/local/bin/docker-entryp…   34B
<missing>      6 days ago       /bin/sh -c #(nop) COPY file:e9c22353a1133b89…   14.2kB
<missing>      6 days ago       /bin/sh -c #(nop) COPY dir:2e040acc386ebd23b…   1.12kB
<missing>      6 days ago       /bin/sh -c #(nop)  VOLUME [/var/lib/mysql]      0B
<missing>      6 days ago       /bin/sh -c {   echo mysql-community-server m…   456MB
<missing>      6 days ago       /bin/sh -c echo 'deb [ signed-by=/etc/apt/ke…   99B
<missing>      6 days ago       /bin/sh -c #(nop)  ENV MYSQL_VERSION=8.0.34-…   0B
<missing>      6 days ago       /bin/sh -c #(nop)  ENV MYSQL_MAJOR=8.0          0B
<missing>      6 days ago       /bin/sh -c set -eux;  key='859BE8D7C586F5384…   2.29kB
<missing>      6 days ago       /bin/sh -c set -eux;  apt-get update;  apt-g…   49.9MB
<missing>      6 days ago       /bin/sh -c mkdir /docker-entrypoint-initdb.d    0B
<missing>      6 days ago       /bin/sh -c set -eux;  savedAptMark="$(apt-ma…   4.23MB
<missing>      6 days ago       /bin/sh -c #(nop)  ENV GOSU_VERSION=1.16        0B
<missing>      6 days ago       /bin/sh -c apt-get update && apt-get install…   9.96MB
<missing>      6 days ago       /bin/sh -c groupadd -r mysql && useradd -r -…   329kB
<missing>      6 days ago       /bin/sh -c #(nop)  CMD ["bash"]                 0B
<missing>      6 days ago       /bin/sh -c #(nop) ADD file:3d726bf0abbc08d6d…   80.5MB
</pre>
- Run the image in a container named mysqlserver1:
<pre>
$ sudo docker run -tid --name mysqlserver1 student[1-6]/mysqlserver:latest
8f5d8cbe3d09d8a7238325947218ac2056f14e5d1435a379f34b58b825ac2dd0

$ sudo docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS          PORTS                 NAMES
8f5d8cbe3d09   student[1-6]/mysqlserver:latest   "docker-entrypoint.s…"   16 seconds ago   Up 15 seconds   3306/tcp, 33060/tcp   mysqlserver1
</pre>
- Check the container logs to see of everything starts as expected:
<pre>
$ watch sudo docker logs mysqlserver1
(...) 
2023-08-04 09:13:54+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.0.34-1debian11 started.
2023-08-04 09:13:55+00:00 [Note] [Entrypoint]: Switching to dedicated user 'mysql'
2023-08-04 09:13:55+00:00 [Note] [Entrypoint]: Entrypoint script for MySQL Server 8.0.34-1debian11 started.
2023-08-04 09:13:55+00:00 [Note] [Entrypoint]: Initializing database files
2023-08-04T09:13:55.624784Z 0 [Warning] [MY-011068] [Server] The syntax '--skip-host-cache' is deprecated and will be removed in a future release. Please use SET GLOBAL host_cache_size=0 instead.
2023-08-04T09:13:55.626764Z 0 [System] [MY-013169] [Server] /usr/sbin/mysqld (mysqld 8.0.34) initializing of server in progress as process 79
2023-08-04T09:13:55.664640Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
2023-08-04T09:13:56.732508Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
2023-08-04T09:13:58.832867Z 6 [Warning] [MY-010453] [Server] root@localhost is created with an empty password ! Please consider switching off the --initialize-insecure option.
2023-08-04 09:14:03+00:00 [Note] [Entrypoint]: Database files initialized
2023-08-04 09:14:03+00:00 [Note] [Entrypoint]: Starting temporary server
mysqld will log errors to /mysqldata/ea7438ce3304.err
mysqld is running as pid 121
2023-08-04 09:14:04+00:00 [Note] [Entrypoint]: Temporary server started.
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leapseconds' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/tzdata.zi' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
2023-08-04 09:14:07+00:00 [Note] [Entrypoint]: Creating database mysql
2023-08-04 09:14:07+00:00 [Note] [Entrypoint]: /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/1_sakila-schema.sql
2023-08-04 09:14:08+00:00 [Note] [Entrypoint]: /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/2_sakila-data.sql
2023-08-04 09:14:11+00:00 [Warn] [Entrypoint]: /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/README.md
2023-08-04 09:14:11+00:00 [Note] [Entrypoint]: Stopping temporary server
2023-08-04 09:14:14+00:00 [Note] [Entrypoint]: Temporary server stopped
2023-08-04 09:14:14+00:00 [Note] [Entrypoint]: MySQL init process done. Ready for start up.
2023-08-04T09:14:14.964493Z 0 [Warning] [MY-011068] [Server] The syntax '--skip-host-cache' is deprecated and will be removed in a future release. Please use SET GLOBAL host_cache_size=0 instead.
2023-08-04T09:14:14.964621Z 0 [System] [MY-010116] [Server] /usr/sbin/mysqld (mysqld 8.0.34) starting as process 1
2023-08-04T09:14:15.002460Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
2023-08-04T09:14:15.448862Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
2023-08-04T09:14:15.848283Z 0 [Warning] [MY-010068] [Server] CA certificate ca.pem is self signed.
2023-08-04T09:14:15.848701Z 0 [System] [MY-013602] [Server] Channel mysql_main configured to support TLS. Encrypted connections are now supported for this channel.
2023-08-04T09:14:15.853677Z 0 [Warning] [MY-011810] [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory.
2023-08-04T09:14:15.916321Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/run/mysqld/mysqlx.sock
2023-08-04T09:14:15.916904Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.34'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
</pre>
- Connect to the docker container and connect to the MySQL database server and inspect the contents by listings databases and objects.  
<pre>
$ sudo docker exec -it mysqlserver1 bash
root@ea7438ce3304:/#  mysql --user=root --socket=/var/run/mysqld/mysqld.sock --password
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 8.0.34 MySQL Community Server - GPL

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases ;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sakila             |
| sys                |
+--------------------+
5 rows in set (0.02 sec)

mysql> show tables from sakila ;
+----------------------------+
| Tables_in_sakila           |
+----------------------------+
| actor                      |
| actor_info                 |
| address                    |
| category                   |
| city                       |
| country                    |
| customer                   |
| customer_list              |
| film                       |
| film_actor                 |
| film_category              |
| film_list                  |
| film_text                  |
| inventory                  |
| language                   |
| nicer_but_slower_film_list |
| payment                    |
| rental                     |
| sales_by_film_category     |
| sales_by_store             |
| staff                      |
| staff_list                 |
| store                      |
+----------------------------+
23 rows in set (0.00 sec)
mysql> exit
root@ea7438ce3304:/# exit
</pre>
- To test the Python code against the new MySQL docker container, create a new container by :
  <ol>- creating an image from python:latest</ol>
  <ol>- setup python3-pip using apt package manager</ol>
  <ol>- setup mysqlclient and lxml python packages using pip</ol>
  <ol>- create a directory named /var/lib/myagent</ol>
  <ol>- clone your devops_student[1-6] repo and checkout into branch MYSQL_1</ol>
  <ol>- copy the contents of the local repo over /var/lib/myagent</ol>
  <ol>- get the IP address of the mysqlserver1 container</ol>
  <ol>- add a row identifying mysqlserver1 by IP at the end of /etc/hosts </ol>
<pre>
# First get the IP Address of mysqlserver1
$ sudo docker inspect mysqlserver1 | grep -i IPAddr
            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.2",
                    "IPAddress": "172.17.0.2",

# Then create the Dockerfile accordingly:
$ cd ~/FORMATION/DEVOPS101/DOCKER
$ vi Dockerfile
(...)
FROM python:latest
RUN apt-get update && apt-get install -y python3-pip
RUN pip install mysqlclient lxml
RUN mkdir /var/lib/myagent
RUN git clone https://students-capdata:TOKEN@github.com/Capdata/devops_student[1-6].git 
RUN cd devops_student[1-6] && git checkout MYSQL_1
RUN cp -pR /devops_student1/student1/* /var/lib/myagent/
</pre>
- Build the image and run the container :
<pre>
$ sudo docker build -t student[1-6]/myagent .
[+] Building 5.5s (11/11) FINISHED
(...)
 => => naming to docker.io/student[1-6]/myagent

$ sudo docker image ls
REPOSITORY             TAG       IMAGE ID       CREATED         SIZE
student[1-6]/myagent       latest    7ba54b321dc7   4 minutes ago   1.11GB
student[1-6]/mysqlserver   latest    8e8017633e91   21 hours ago    659MB
(...)

$ sudo docker run -tid --name agent1 --add-host "mysqlserver1:172.17.0.2" student1/myagent
0812e0d714144012d6abb2b04afbacafc3f3ccccfea60fc65ae6674ed6f80fe6
</pre>  

- And finally test the python my_healthcheck against mysqlserver1 container:
<pre>
$ sudo docker exec -it agent1 bash
root@99585881bddf:/# cd /var/lib/myagent
root@99585881bddf:/var/lib/myagent# python3 my_healthcheck.py
Version detectee : ({'version()': '8.0.34'},)
</pre>
- Exit from the container and the student shell:
<pre>
root@99585881bddf:/var/lib/myagent# exit
$ exit
</pre>

# LAB 3 : ANSIBLE
Deploy a new MySQL instance with ANSIBLE

## Step 1: setting up the nodes and configure connection 
### Control Node creation & configuration
- Prepare the first LXC container to host the Control Node by launching an ubuntu:20.04 image named controlnode using LXC client command line:
<pre>
$ su - student 
$ sudo lxc launch ubuntu:20.04 controlnode
Creating controlnode
Starting controlnode

$ sudo lxc list controlnode
+-------------+---------+-----------------------+-----------------------------------------------+-----------+-----------+
|    NAME     |  STATE  |         IPV4          |                     IPV6                      |   TYPE    | SNAPSHOTS |
+-------------+---------+-----------------------+-----------------------------------------------+-----------+-----------+
| controlnode | RUNNING | 10.108.127.196 (eth0) | fd42:55eb:ffed:5765:216:3eff:fe3d:ffc4 (eth0) | CONTAINER | 0         |
+-------------+---------+-----------------------+-----------------------------------------------+-----------+-----------+
</pre>

- Connect to the controlnode container and update the apt package local repo, then setup python3-pip : 
<pre>$ sudo lxc exec controlnode bash
root@controlnode:~$ apt-get update
(...)
root@controlnode:~$ apt-get install -y python3-pip
(...)
</pre>

- Setup ansible version=2.9.9 using PIP:
<pre>
root@controlnode:~$ pip3 install ansible==2.9.9
Collecting ansible==2.9.9
  Downloading ansible-2.9.9.tar.gz (14.2 MB)
     |████████████████████████████████| 14.2 MB 14.5 MB/s
(...)
root@controlnode:~$ ansible --version
ansible 2.9.9
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.8/dist-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.8.10 (default, May 26 2023, 14:05:08) [GCC 9.4.0]
</pre>
- Exit from the controlnode container
<pre>
root@controlnode:~$ exit
exit
</pre>


### Managed Node creation & configuration
- Prepare a second LXC container to host the Managed Node by launching another ubuntu:20.04 image named managednode using LXC client command line:
<pre>
$ sudo lxc launch ubuntu:20.04 managednode
Creating managednode
Starting managednode

$ sudo lxc list
+-------------+---------+-----------------------+-----------------------------------------------+-----------+-----------+
|    NAME     |  STATE  |         IPV4          |                     IPV6                      |   TYPE    | SNAPSHOTS |
+-------------+---------+-----------------------+-----------------------------------------------+-----------+-----------+
| controlnode | RUNNING | 10.108.127.196 (eth0) | fd42:55eb:ffed:5765:216:3eff:fe3d:ffc4 (eth0) | CONTAINER | 0         |
+-------------+---------+-----------------------+-----------------------------------------------+-----------+-----------+
| managednode | RUNNING | 10.108.127.170 (eth0) | fd42:55eb:ffed:5765:216:3eff:fe81:81f6 (eth0) | CONTAINER | 0         |
+-------------+---------+-----------------------+-----------------------------------------------+-----------+-----------+
</pre>
- Connect to the managednode container, check python3 version and setup a group and user named both ansible as explained in the training:
<pre>
$ sudo lxc exec managednode bash
root@managednode:~$ python3 --version
Python 3.8.10

root@managednode:~$ groupadd ansible
root@managednode:~$ useradd -d /home/ansible -g ansible -m -s /bin/bash ansible
root@managednode:~$ passwd ansible
New password: ******
Retype new password: ******
passwd: password updated successfully
</pre>

- Modify /etc/sudoers to allow ansible sudo any command without password prompting and check by calling apt package manager from the ansible user context:
<pre>
root@managednode:~$ vi /etc/sudoers
(...)
# ANSIBLE
%ansible	ALL=(ALL)	NOPASSWD: ALL

root@managednode:~$ su - ansible
ansible@managednode:~$ sudo apt-cache search mysql-server
mysql-server - MySQL database server (metapackage depending on the latest version)
mysql-server-8.0 - MySQL database server binaries and system database setup
mysql-server-core-8.0 - MySQL database server binaries
</pre>
- Exit from the managednode container:
<pre>
ansible@managednode:~$ exit
logout
root@managednode:~$ exit
exit
</pre>

### Setting up SSH connection
- First we need to allow the managed node SSH server to allow password and publickey authentication methods:
<pre>
$ sudo lxc exec managednode bash
root@managednode:~$ vi /etc/ssh/sshd_config
(...)
PubkeyAuthentication yes
PasswordAuthentication yes
(...)

root@managednode:~$ systemctl restart ssh.service
root@managednode:~$ systemctl status ssh.service
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2023-08-10 09:52:41 UTC; 8s ago
       Docs: man:sshd(8)
             man:sshd_config(5)
    Process: 1092 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
   Main PID: 1093 (sshd)
      Tasks: 1 (limit: 1126)
     Memory: 1.0M
     CGroup: /system.slice/ssh.service
             └─1093 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups

Aug 10 09:52:41 managednode systemd[1]: Starting OpenBSD Secure Shell server...
Aug 10 09:52:41 managednode sshd[1093]: Server listening on 0.0.0.0 port 22.
Aug 10 09:52:41 managednode sshd[1093]: Server listening on :: port 22.
Aug 10 09:52:41 managednode systemd[1]: Started OpenBSD Secure Shell server.
</pre>
- Exit from managednode
- <pre>
root@managednode:~$ exit
</pre> 

- Then we need to generate SSH ecdsa keys on the controlnode and copy the public key over to the managednode to allow controle node -> managed node communication (don't put a passphrase):
<pre>
$ sudo lxc exec controlnode bash
root@controlnode:~$ ssh-keygen -t ecdsa -b 521
Generating public/private ecdsa key pair.
Enter file in which to save the key (/root/.ssh/id_ecdsa):
Enter passphrase (empty for no passphrase): [DON'T]
Enter same passphrase again: [DON'T]
Your identification has been saved in /root/.ssh/id_ecdsa
Your public key has been saved in /root/.ssh/id_ecdsa.pub
The key fingerprint is:
SHA256:JN8vYv3Ik7elm4b/qiYCovetZ+QVtroeonYPs9M4he8 root@controlnode
The key's randomart image is:
+---[ECDSA 521]---+
|                 |
|                 |
|      . .        |
|       +o.       |
|     . .So.      |
|  . o o o. .     |
| . .+O.oo oo. .  |
|. o.=*Oo.o=+o+   |
| o.o+XEo o+*O=.  |
+----[SHA256]-----+

root@controlnode:~$ ssh-copy-id ansible@managednode.lxd
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_ecdsa.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
ansible@managednode.lxd's password:

Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'ansible@managednode.lxd'"
and check to make sure that only the key(s) you wanted were added.
root@controlnode:~$ exit
</pre>

- Test the connection : 
The passphrase should not be required anymore
<pre>
root@controlnode:~$ ssh ansible@managednode.lxd -n date
Thu Aug 10 11:06:20 UTC 2023
</pre>
</pre>

- Finally from the controlnode container, test a ansible ping to the managed node to check that the connection is OK:
<pre>
root@controlnode:~$ ansible -u ansible --inventory "managednode.lxd," all -m ping
managednode.lxd | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
</pre>

## Step 2 : set up roles, playbooks, vaults and jinja2 templates to deploy a MySQL instance in the managednode

- 3 roles will be used:
<ol>- rl_prepa_install_mysql : prerequisites</ol>
<ol>- rl_install_MySQL : MySQL setup</ol>
<ol>- rl_postinstall_MySQL : post-installation tasks</ol>

- Such as : 
<pre>
/etc/ansible/group_vars/all/
	|__ secret.yml		# vault password for user root@localhost 
	|__ mysql_vars.yml		# MySQL configuration variables for Jinja2

~/Install_MySQL/
	|__ playbook_install_MySQL.yml  # Main playbook 

	|__ rl_prepa_install_mysql
		|__ tasks/main.yml		 # preparation

	|__ rl_install_MySQL
		|__ tasks/main.yml		 # setup

	|__ rl_postinstall_MySQL
		|__ tasks/main.yml		 # post-setup
		|__ templates/my.cnf.j2	 # Jinja2 template for MySQL configuration file
		|__ handlers/main.yml	 # handling post-setup tasks
</pre>

### Configuring the inventory 

- Create the directories for /etc/ansible/ group_vars and host_vars, and create a minimal inventory.yml file with:
<ol>- managednode in the all: group</ol>
<ol>- python3 as the default python interpreter: group</ol>
<pre>
$ sudo lxc exec controlnode bash
root@controlnode:~$ mkdir -p /etc/ansible/group_vars /etc/ansible/host_vars
$ vi /etc/ansible/inventory.yml
(...)
all:
  hosts:
    managednode.lxd:
  vars:
    ansible_python_interpreter: /usr/bin/python3
</pre>

- And test the ping module using the inventory.yml as inventory:
<pre>
root@controlnode:~$ ansible -u ansible -i /etc/ansible/inventory.yml all -m ping
managednode.lxd | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
</pre>

### Setting up community module for MySQL:
<pre>
root@controlnode:~$ ansible-galaxy collection install community.mysql
Process install dependency map
Starting collection install process
Installing 'community.mysql:3.7.2' to '/root/.ansible/collections/ansible_collections/community/mysql'
</pre>

### Create directory structure for roles and files:
<pre>
root@controlnode:~$ mkdir ~/Install_MySQL
root@controlnode:~$ ansible-galaxy init ~/Install_MySQL/rl_prepa_install_mysql
- Role /root/Install_MySQL/rl_prepa_install_mysql was created successfully
root@controlnode:~$ ansible-galaxy init ~/Install_MySQL/rl_install_MySQL
- Role /root/Install_MySQL/rl_install_MySQL was created successfully
root@controlnode:~$ ansible-galaxy init ~/Install_MySQL/rl_postinstall_MySQL
- Role /root/Install_MySQL/rl_postinstall_MySQL was created successfully
</pre>

### Create the secret vault to store MySQL's root@localhost password:
<pre>
root@controlnode:~$ vi ~/.vault
(...)
capdata

root@controlnode:~$ chmod 600 ~/.vault

root@controlnode:~$ ansible-vault create  --vault-id ~/.vault /etc/ansible/group_vars/all/secret.yml
[WARNING]: /etc/ansible/group_vars/all does not exist, creating...
Vault password: ******
(...)
rootpassword: "******"
</pre>

### Create the main playbook:
<pre>
root@controlnode:~$ vi ~/Install_MySQL/playbook_install_MySQL.yml
(...)
- name: Playbook deploiement et configuration MySQL 8.0
  hosts: all
  remote_user: ansible
  become: yes
  roles:
  - rl_prepa_install_mysql
  - rl_install_MySQL
  - rl_postinstall_MySQL
</pre>

### Create the Role 1) for rl_prepa_install_mysql :
<pre>
root@controlnode:~$ vi ~/Install_MySQL/rl_prepa_install_mysql/tasks/main.yml
(...)
- name: installation GNUPG2
  apt:
    name: gnupg2
    cache_valid_time: 3600
    state: present
- name: installation CURL
  apt:
    name: curl
    cache_valid_time: 3600
    state: present
- name: installation python3-pip
  apt:
    name: python3-pip
    cache_valid_time: 3600
    state: present
- name: installation PyMySQL via PIP
  pip:
    name: PyMySQL
- name: Recup distro UBUNTU dans une variable
  shell: lsb_release -sc
  register: __distro_ubuntu
- name: Recuperation des packages .DEB pour le REPO percona
  shell: wget https://repo.percona.com/apt/percona-release_latest.{{ __distro_ubuntu.stdout }}_all.deb -P /tmp/
- name: installation package DEB pour installer le repo Percona
  apt:
    deb: /tmp/percona-release_latest.{{ __distro_ubuntu.stdout }}_all.deb
- name: Mise a jour du cache APT
  apt:
    update_cache: yes
    cache_valid_time: 3600
- name: activation du repository Percona avec percona-release
  shell: percona-release setup ps80
</pre>

### Create the Role 2) for rl_install_MySQL :
<pre>
root@controlnode:~$ vi ~/Install_MySQL/rl_install_MySQL/tasks/main.yml
(...)
- name: Install Percona-Server
  apt:
    name: percona-server-server
- name: configuration du service systemd
  systemd:
    name: mysql.service
    state: started
    enabled: yes
- name: reboot pour tester le redémarrage du service
  reboot:
    msg: "Attention redemarrage verif service MySQL dans 5 secondes !!!"
    connect_timeout: 5
    reboot_timeout: 300
    pre_reboot_delay: 5
    test_command: uptime
</pre>

### Create the Role 3) for rl_postinstall_MySQL :
<pre>
root@controlnode:~$ vi ~/Install_MySQL/rl_postinstall_MySQL/tasks/main.yml
(...)
- name : verifier si le service est bien demarre
  systemd:
    name: mysql.service
    state: started

- name: changer le plugin d authentification pour root@localhost
  shell: mysql -u root -e 'UPDATE mysql.user SET plugin="mysql_native_password" WHERE user="root" AND host="localhost";'

- name: Flush Privs
  shell: mysql -u root -e 'flush privileges;'

- name: Changer le mot de passe de root
  community.mysql.mysql_user:
    login_host: 'localhost'
    login_user: 'root'
    login_password: ''
    name: 'root'
    password: "{{ rootpassword }}"
    state: present

- name: Appliquer la configuration via le template j2
  template:
    src: my.cnf.j2
    dest: /etc/mysql/my.cnf
    owner: root
    mode: 0644
  notify:
  - restart_percona
</pre>

### Create the Jinja2 template for MySQL configuration file:
<pre>
root@controlnode:~$ vi ~/Install_MySQL/rl_postinstall_MySQL/templates/my.cnf.j2
(...)
[mysqld]
pid_file        = {{ pid_file }}
socket          = {{ socket }}
port            = {{ port }}
datadir         = {{ datadir }}
log_error       = {{ log_error }}
log_bin         = {{ log_bin }}
innodb_buffer_pool_size = {{ innodb_buffer_pool_size }}
</pre>

### Create the mysql_vars.yml to :
<pre>
root@controlnode:~$ vi /etc/ansible/group_vars/all/mysql_vars.yml
(...)
pid_file: /var/lib/mysql/mysql.pid
socket: /var/lib/mysql/mysqld.sock
port: 3306
datadir: /var/lib/mysql
log_error: /var/log/mysql/mysql_error.log
log_bin: mysql_bin
innodb_buffer_pool_size: 33554432
</pre>

### Finally create the handler to handle post-setup tasks:
<pre>
root@controlnode:~$ vi ~/Install_MySQL/rl_postinstall_MySQL/handlers/main.yml
(...)
- name: restart_percona
  systemd:
    name: mysql.service
    state: restarted
</pre>

### And execute the playbook to create the mysql.service on managednode:
<pre>
root@controlnode:~$ ansible-playbook -i /etc/ansible/inventory.yml --vault-id ~/.vault playbook_install_MySQL.yml

PLAY [Playbook deploiement et configuration MySQL 8.0] **************************************************************************************************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************************************************************************************************************************************
ok: [managednode.lxd]

TASK [rl_prepa_install_mysql : installation GNUPG2] *****************************************************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_prepa_install_mysql : installation CURL] *******************************************************************************************************************************************************************************************
ok: [managednode.lxd]

TASK [rl_prepa_install_mysql : installation python3-pip] ************************************************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_prepa_install_mysql : installation PyMySQL via PIP] ********************************************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_prepa_install_mysql : Recup distro UBUNTU dans une variable] ***********************************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_prepa_install_mysql : Recuperation des packages .DEB pour le REPO percona] *********************************************************************************************************************************************************
[WARNING]: Consider using the get_url or uri module rather than running 'wget'.  If you need to use command because get_url or uri is insufficient you can add 'warn: false' to this command task or set 'command_warnings=False' in
ansible.cfg to get rid of this message.
changed: [managednode.lxd]

TASK [rl_prepa_install_mysql : installation package DEB pour installer le repo Percona] *****************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_prepa_install_mysql : Mise a jour du cache APT] ************************************************************************************************************************************************************************************
ok: [managednode.lxd]

TASK [rl_prepa_install_mysql : activation du repository Percona avec percona-release] *******************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_install_MySQL : Install Percona-Server] ********************************************************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_install_MySQL : configuration du service systemd] **********************************************************************************************************************************************************************************
ok: [managednode.lxd]

TASK [rl_install_MySQL : reboot pour tester le redémarrage du service] **********************************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_postinstall_MySQL : verifier si le service est bien demarre] ***********************************************************************************************************************************************************************
ok: [managednode.lxd]

TASK [rl_postinstall_MySQL : changer le plugin d authentification pour root@localhost] ******************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_postinstall_MySQL : Flush Privs] ***************************************************************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_postinstall_MySQL : Changer le mot de passe de root] *******************************************************************************************************************************************************************************
changed: [managednode.lxd]

TASK [rl_postinstall_MySQL : Appliquer la configuration via le template j2] *****************************************************************************************************************************************************************
changed: [managednode.lxd]

RUNNING HANDLER [rl_postinstall_MySQL : restart_percona] ************************************************************************************************************************************************************************************
changed: [managednode.lxd]

PLAY RECAP **********************************************************************************************************************************************************************************************************************************
managednode.lxd            : ok=19   changed=14   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
</pre>
- And finally exit the controlnode:
<pre>
root@controlnode:~$ exit
</pre>

### Test the deployment
- FInally test the deployment by connecting to the mysql instance in the managednode container:
<pre>
$ sudo lxc exec managednode bash
root@managednode:~# mysql --user=root --socket=/var/lib/mysql/mysqld.sock --password
Enter password: *****
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.33-25 Percona Server (GPL), Release '25', Revision '60c9e2c5'

Copyright (c) 2009-2023 Percona LLC and/or its affiliates
Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases ;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.01 sec)

mysql> exit
Bye
</pre>
- Disconnect and shut down both 2 lxc containers
<pre>
root@managednode:~# exit
exit
$ sudo lxc stop managednode controlnode
$ sudo lxc list
+-------------+---------+------+------+-----------+-----------+
|    NAME     |  STATE  | IPV4 | IPV6 |   TYPE    | SNAPSHOTS |
+-------------+---------+------+------+-----------+-----------+
| controlnode | STOPPED |      |      | CONTAINER | 0         |
+-------------+---------+------+------+-----------+-----------+
| managednode | STOPPED |      |      | CONTAINER | 0         |
+-------------+---------+------+------+-----------+-----------+
</pre>
- Finally exit the student shell
<pre>
$ exit
</pre>
# LAB 4 : PROMETHEUS & GRAFANA
In this LAB we will be setting up a mysql_exporter for Prometheus and a Grafan console to get the first metrics
## Setup Prometheus and install a MySQL exporter
### Create a docker container daemon for Prometheus by streaming the image from quay.io/prometheus/prometheus:v2.0.0
- It is important to make the 9090 port available outside of the container by using -p port redirection
<pre>
$ sudo docker run -d --name "prometheus" -p 9090:9090 quay.io/prometheus/prometheus:v2.0.0
905a6b480c5d5198ac993cbd0234696a073d5e3bcb892c5b783c3f77d7b11e0c
$ sudo docker ps -f "name=prometheus"
CONTAINER ID   IMAGE                                  COMMAND                  CREATED         STATUS         PORTS                                       NAMES
905a6b480c5d   quay.io/prometheus/prometheus:v2.0.0   "/bin/prometheus --c…"   3 minutes ago   Up 3 minutes   0.0.0.0:9090->9090/tcp, :::9090->9090/tcp   prometheus
</pre>
- Test if available from your browser, using the public IP corresponding to your environment, eg http://PUBLICIP:9090/graph
![image](https://github.com/Capdata/Devops101/assets/19890935/b1316b6e-767f-4fb8-a32c-19756ca0f205)

### Add a mysql_exporter to prometheus
- Create a mysql user with PROCESS, REPLICATION and SELECT privileges on all objecs in the mysqlserver1 docker container. 
First check that the mysqlserver1 container is up 
<pre>
$ sudo docker ps -f "name=mysqlserver1"
CONTAINER ID   IMAGE                         COMMAND                  CREATED      STATUS          PORTS                 NAMES
ea7438ce3304   student1/mysqlserver:latest   "docker-entrypoint.s…"   6 days ago   Up 55 minutes   3306/tcp, 33060/tcp   mysqlserver1
</pre>
- Then connect to the container and to mysql, and create the user / grant the privileges:
<pre>
$ sudo docker exec -it mysqlserver1 bash
root@ea7438ce3304:/# mysql --user=root --socket=/var/run/mysqld/mysqld.sock --password
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 8.0.34 MySQL Community Server - GPL

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> CREATE USER 'exporter'@'%' IDENTIFIED BY '*****' WITH MAX_USER_CONNECTIONS 3;
Query OK, 0 rows affected (0.01 sec)

mysql> GRANT PROCESS, REPLICATION CLIENT, SELECT ON *.* TO 'exporter'@'%';
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> FLUSH PRIVILEGES ;
Query OK, 0 rows affected (0.00 sec)

mysql> exit
Bye
root@ea7438ce3304:/# exit
exit
</pre>
- Then create another docker container named mysqlexporter1 but this step is a little complex 
<ol>- First on the host, create a ~/.exporter.cnf file to put a config [client] section and map the file inside the docker container so it can use it at runtime.</ol>
note: you can get mysqlserver1 IP by running sudo docker inspect on the container and look for IPAddress property<pre>
$ vi ~/.exporter.cnf
(...)
[client]
host=YOUR_DOCKER_MYSQLSERVER1_IP_HERE
port=3306
user=exporter
password=*******
</pre>

<ol>- Second step, run a mysqlexporter container by mapping the file created into /.my.cnf, and redirecting port 9104 to the outside</ol>
<pre>
$ sudo docker run -d --name mysqlexporter1 -p9104:9104 --mount type=bind,source=/home/student/.exporter.cnf,target=/.my.cnf -e DATA_SOURCE_NAME="exporter:*******@(mysqlserver1:3306)/" prom/mysqld-exporter:latest
0f1da4f9bded76e1ae07d2beff3d984dbf12988bc7db9d33e428da3f77a41678

$ sudo docker logs mysqlexporter1
ts=2023-08-11T09:43:02.586Z caller=mysqld_exporter.go:220 level=info msg="Starting mysqld_exporter" version="(version=0.15.0, branch=HEAD, revision=6ca2a42f97f3403c7788ff4f374430aa267a6b6b)"
ts=2023-08-11T09:43:02.586Z caller=mysqld_exporter.go:221 level=info msg="Build context" build_context="(go=go1.20.5, platform=linux/amd64, user=root@c4fca471a5b1, date=20230624-04:09:04, tags=netgo)"
ts=2023-08-11T09:43:02.586Z caller=mysqld_exporter.go:233 level=info msg="Scraper enabled" scraper=slave_status
ts=2023-08-11T09:43:02.586Z caller=mysqld_exporter.go:233 level=info msg="Scraper enabled" scraper=global_status
ts=2023-08-11T09:43:02.586Z caller=mysqld_exporter.go:233 level=info msg="Scraper enabled" scraper=global_variables
ts=2023-08-11T09:43:02.586Z caller=mysqld_exporter.go:233 level=info msg="Scraper enabled" scraper=info_schema.innodb_cmp
ts=2023-08-11T09:43:02.586Z caller=mysqld_exporter.go:233 level=info msg="Scraper enabled" scraper=info_schema.innodb_cmpmem
ts=2023-08-11T09:43:02.586Z caller=mysqld_exporter.go:233 level=info msg="Scraper enabled" scraper=info_schema.query_response_time
ts=2023-08-11T09:43:02.587Z caller=tls_config.go:274 level=info msg="Listening on" address=[::]:9104
ts=2023-08-11T09:43:02.587Z caller=tls_config.go:277 level=info msg="TLS is disabled." http2=false address=[::]:9104
</pre>

<ol>- Then log in prometheus container, add a section to /etc/prometheus/prometheus.yml file to add a mysqlexporter1 as a new target, and restart prometheus container to validate
note : again use docker inspect to get mysqlexporter1 IP address</ol>
<pre>
$ sudo docker exec -it prometheus sh
/prometheus $ vi /etc/prometheus/prometheus.yml
(...)
  - job_name: 'mysql80'
    static_configs:
      - targets: ['172.17.0.5:9104']
/prometheus $ exit
$ sudo docker restart prometheus
</pre>

<ol>- and finally check that a new target has been added in prometheus, and the mysql metrics are available</ol>

![image](https://github.com/Capdata/Devops101/assets/19890935/3b4432ae-e1fb-4146-ae8b-72d2648e967e) 
![image](https://github.com/Capdata/Devops101/assets/19890935/3e0c7201-5240-4916-8cfd-4f3e84095411) 

## Adding Grafana
- Run a last container for grafana by pulling the official image in version 5.3.2 at grafana/grafana :
<pre>
$ sudo docker run -d -p 3000:3000 --name=grafana grafana/grafana:5.3.2
16f619d9ddb72b1d147427ebe4e4bd92402ce092aa36bfeff24ca8ad3b496b16

$ sudo docker ps -f 'name=grafana'
CONTAINER ID   IMAGE                        COMMAND     CREATED              STATUS              PORTS                                       NAMES
16f619d9ddb7   grafana/grafana:5.3.2   "/run.sh"   About a minute ago   Up About a minute   0.0.0.0:3000->3000/tcp, :::3000->3000/tcp   grafana
</pre>

- And test the connection with your browser:
  
![image](https://github.com/Capdata/Devops101/assets/19890935/10027272-739a-4654-a942-25b5a128486b)

- Add a data source for mysqlserver1 :
  
![image](https://github.com/Capdata/Devops101/assets/19890935/5442dd8f-49bc-41fe-b141-3acbe6409486)

- Finally create a dashboard for mysqlserver1 with the metrics of your choice:
  
 ![image](https://github.com/Capdata/Devops101/assets/19890935/437f4321-8961-4a30-9e79-6cece9006635)






