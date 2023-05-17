# Devops101
(Repo for Devops 101 for DBAs training)

# Prereqs
- 1 github public repo per student (provision for 6 students) with original script, v1.0, MASTER branch only
- 1 EC2 Ubuntu 20.04 / student with each :
  - 1 40Gb GP3 volume mounted on /var/lib/docker
  - 1 40Gb GP3 volume for ZFS storage pool
  - ZFS tools and storage pool of 40Gb
  - lxd setup using ZFS
  - 3 x Ubuntu 20.04 LXD vanilla containers, stopped 
  - student user account with sudo privileges
  - Docker setup
  - Git client
  - Directory : /home/student
  - Internet access 
  - Python3 & pip3

# LAB 1 : GIT
- Configure git
- Create local sandbox 
- Clone repo
- Create DEV branch
- Position on DEV branch
- Modify code to change credentials in connection property file
- Check differences & Commit locally in locla branch
- Push local branch to repo. 

# LAB 2 : DOCKER
- Setup Docker engine 
- Create a persistent volume for MySQL
- Create a dockerfile for MySQL
- Build the image
- Run the MySQL Container based on the created image
- Observe layer history and try to optimize the image
- Run a simple Ubuntu 20.04 docker container from the public repository 
- Connect to the container and get the MySQL monitoring script
- Test the script and check connection to MySQL Database 
- 
# LAB 3 : ANSIBLE

# LAB 4 : PROMETHEUS & GRAFANA
