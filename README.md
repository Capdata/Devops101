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
A user token will be given to you during the training. It will be referred as TOKEN in the docs... Your student number will be referred as -YOURNUMBER 1-6-, eg devops_student1, etc... 
<pre>
$ git clone https://students-capdata:TOKEN@github.com/Capdata/devops_student-YOURNUMBER 1-6-.git
Cloning into 'devops_studentXX'...
remote: Enumerating objects: 30, done.
remote: Counting objects: 100% (30/30), done.
remote: Compressing objects: 100% (25/25), done.
remote: Total 30 (delta 4), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (30/30), 8.43 KiB | 1.05 MiB/s, done.
</pre>
- Navigate the local files:
<pre>
$ tree devops_studentXX/
devops_studentXX/
├── README.md
└── studentXX
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
 
- Create a new branch called CONN_INIT_1, and in the context of this new branch, modify the my.cs.xml file to reflect the correct connection string parameters (given by the trainer)    
<pre>
$ cd ~/FORMATION/DEVOPS101/GIT/devops_studentXX

$ git branch -a
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main

$ git branch CONN_INIT_1

$ git branch -a
  CONN_INIT_1
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main

$ git checkout CONN_INIT_1
Switched to branch 'CONN_INIT_1'

$ git branch -a
* CONN_INIT_1
  main
  remotes/origin/HEAD -> origin/main
  remotes/origin/main

$ vi studentXX/my/cs.xml    # [XX == 1-6]
(...)
</pre>

- add new directory and files, and commit to the local repo:

<pre>
$ git add --all

$ git status
On branch CONN_INIT_1
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   student1/my/cs.xml

$ git commit -m "changing connection string parameters..."
[CONN_INIT_1 277aec0] changing connection string parameters...
 1 file changed, 5 insertions(+), 5 deletions(-)

$ git status
On branch CONN_INIT_1
nothing to commit, working tree clean
</pre>

- Check if local repo is up to date and push local branch to remote repo:
<pre>
$ git pull origin main
From https://github.com/Capdata/devops_studentXX
 * branch            main       -> FETCH_HEAD
Already up to date.

$ git push origin CONN_INIT_1 
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Compressing objects: 100% (5/5), done.
Writing objects: 100% (5/5), 623 bytes | 623.00 KiB/s, done.
Total 5 (delta 1), reused 0 (delta 0)
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
remote:
remote: Create a pull request for 'CONN_INIT_1' on GitHub by visiting:
remote:      https://github.com/Capdata/devops_student1/pull/new/CONN_INIT_1
remote:
To https://github.com/Capdata/devops_student1.git
 * [new branch]      CONN_INIT_1 -> CONN_INIT_1
</pre>

- Disconnects from the host
<pre>exit</pre>

# LAB 2 : DOCKER
- Connect to the host as student user:
<pre>
$ su - student
</pre>
- Create a new local branch called DOCKER_INIT_1 and checkout to this branch.
- Under student[1-6]/dockerfiles, create a new Dockerfile to build a custom MySQL image using the following parameters and details in the training manual:
<ol>
  <li>Version : latest</li>
  <li>additionnal packages to install : vim</li>
  <li>Create Data Directory : /mysqldata</li>
  <li>Mount Docker Volume /mysqldata</li> 
  <li>Mount student[1-6]/sql local git directory to the docker entry point</li>
  <li>Copy student[1-6]/etc/my.cnf local git file into the containers='s /etc/mysql</li>
</ol>
... and use also the information as per the student[1-6]/my/cs.xml to expose TCP port, set username, password and database environment variables. 
<pre>
$ cd ~/FORMATION/DEVOPS101/GIT/Devops101/dockerfiles
$ vi Dockerfile
(...)
FROM mysql:latest
RUN apt-get update && apt-get install -y vim
RUN mkdir /mysqldata
VOLUME /mysqldata
COPY my.cnf /etc/mysql/conf.d/my.cnf
ADD sql/ /docker-entrypoint-initdb.d
ENV MYSQL_ROOT_PASSWORD=********
ENV MYSQL_DATABASE *******
EXPOSE *****/tcp
CMD ["mysqld"]
</pre>

- Create a persistent volume for MySQL
- Create a dockerfile for MySQL
- Build the image
- Run the MySQL Container based on the created image
- Observe layer history and try to optimize the image
- Run a simple Ubuntu 20.04 docker container from the public repository 
- Connect to the container and get the MySQL monitoring script
- Test the script and check connection to MySQL Database 

# LAB 3 : ANSIBLE
- Deploy a new MySQL instance with ANSIBLE
- 
# LAB 4 : PROMETHEUS & GRAFANA
