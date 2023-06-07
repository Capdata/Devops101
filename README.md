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
$ git config --global user.name "David Baffaleuf" # <-- put your name in here
$ git config --global user.email "dbaffaleuf@capdata-osmozium.com" # <-- put your email in here
$ git config --list
user.name=David Baffaleuf
user.email=dbaffaleuf@capdata-osmozium.com
</pre>
- Clone repository :
<pre>
$ git clone https://github.com/Capdata/Devops101.git
Cloning into 'Devops101'...
remote: Enumerating objects: 30, done.
remote: Counting objects: 100% (30/30), done.
remote: Compressing objects: 100% (25/25), done.
remote: Total 30 (delta 4), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (30/30), 8.43 KiB | 1.05 MiB/s, done.
</pre>
- Navigate the local files:
<pre>
$ tree Devops101/
Devops101/
├── README.md
├── my
│   ├── cs.xml
│   ├── myGetVersion.py
│   └── myconnect.py
└── my_healthcheck.py
</pre>
<ol>
  <li>my_healthcheck.py : is the main program</li>
  <li>my/cs.xml : is the connection string configuration file</li>
  <li>my/myGetVersion.py : just a simple SQL code definition for getting version in MySQL, host of myGetVersion class</li>
  <li>my/myconnect.py: where the MySQL connection happens, host of alldbmyconnection class, requires MySQLdb PIP package</li>
</ol>
 
- Create a new branch called CONN_INIT_1, and in the context of this new branch, modify the my.cs.xml file to reflect the correct connection string parameters (given by the trainer)    
<pre>
$ cd ~/FORMATION/DEVOPS101/GIT

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

student@ip-192-1-1-124:~/FORMATION/DEVOPS101/GIT/Devops101$ vi my/cs.xml
(...)
</pre>

- Check differences with git diff and if OK, commit to the local repo:

<pre>
$ git diff
diff --git a/my/cs.xml b/my/cs.xml
index 5607a38..d0fca98 100644
--- a/my/cs.xml
+++ b/my/cs.xml
@@ -1,8 +1,8 @@
 <?xml version="1.0" encoding="UTF-8"?>
 <connectionstring>
-        <host>myhostname</host>
-        <port>myport</port>
-        <user>myuser</user>
-        <passwd>mypassword</passwd>
-        <database>mydb</database>
+        <host>host1</host>
+        <port>33060</port>
+        <user>root</user>
+        <passwd>pa$$w0rd</passwd>
+       <database>sakila</database>
 </connectionstring>

$ git add my/cs.xml

$ git status
On branch CONN_INIT_1
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   my/cs.xml


$ git commit -m "changing connection string parameters..."
[CONN_INIT_1 e6e596a] changing connection string parameters...
 1 file changed, 5 insertions(+), 5 deletions(-)

$ git status
On branch CONN_INIT_1
nothing to commit, working tree clean
</pre>

- Modify code to change credentials in connection property file
- Check differences & Commit locally in locla branch
- Push local branch to repo. 

# LAB 2 : DOCKER
- Check Docker engine setup
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
