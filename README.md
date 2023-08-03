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
A user token will be given to you during the training. It will be referred as TOKEN in the docs... Your student number will be referred as [1-6], eg devops_student1, devops_student2, etc... 
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
        ├── 3_alter_user_sakila.sql
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

$ vi student[1-6]my/cs.xml    
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
$ cd student1/dockerfiles
$ vi Dockerfile
(...)
FROM mysql:8-debian
RUN apt-get update && apt-get install -y vim
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
student1/mysqlserver   latest    01e39e90335d   4 minutes ago   659MB
</pre> 


- Create a persistent volume for MySQL
<pre>
$ docker volume create mysqlvolume 
# CLEANUP : docker volume rm mysqlvolume 
</pre>

- Run the MySQL Container based on the created image and on the persisted volume

- Observe layer history and try to optimize the image

- Run a simple Ubuntu 20.04 docker container from the public repository 

- Connect to the container and get the MySQL monitoring script

- Test the script and check connection to MySQL Database 

# LAB 3 : ANSIBLE
- Deploy a new MySQL instance with ANSIBLE
- 
# LAB 4 : PROMETHEUS & GRAFANA
