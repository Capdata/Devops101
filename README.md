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
 
- Create DEV branch
- Position on DEV branch
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
