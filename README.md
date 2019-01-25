# selfservepwd
Self Service AD password tool

Using open source tools we can enable password management without the hassle of logging into AD servers.
This tool was written for a very simple environment (with no password policy in place).  You will need to know a service/admin password to the AD server that has access to update users' passwords.  You will also need a linux server to run the necessary scripts.

## Requirements

SSL certificate and key for the webserver, some knowledge of the linux file system, some python and powershell scripting.

## Stage files, install dependencies

After cloning this repo copy all files to a linux server (centos7 used in this example) like so:
cd selfservepwd/
scp -r . username@server.hostname:/var/tmp/

ssh to the server above install python, pip, httpd, put files in their place

```
cd /var/tmp
yum -y install python-pip
yum -y install python34-setuptools
sudo easy_install-3.4 pip
pip3 install requirements.txt
pip install requirements-2.7.txt
rm -f requirements* README.md .git passwdmgr.png admin-passwdmgr.png LICENSE.md newSchedJob.ps1 pwdNeverExpires.ps1
yum -y install httpd
systemctl enable httpd
mv passwdmgt.conf /var/httpd/config.d/
mv passwdmgr.service /etc/systemd/system/
mkdir /opt/passwdmgr
mv . /opt/passwdmgr/
```

## Modify the config files to suit your environment

Using the editor of your choice modify:
 * /opt/passwdmgr/deets.py with the AD server info.
 * /etc/httpd/conf.d/passwdmgr.conf with AD server info, certificate info, and the domain name of your choice
 * /opt/passwdmgr/templates/index.html - update line 25

## Start the services

```
systemctl daemon-reload
systemctl enable passwdmgr.service
systemctl start passwdmgr.service
systemctl start httpd
```

## Verify the service is up

Once you have created a DNS record for the domain name you chose in the apache config file, you should be able to navigate to the page using HTTPS and your active directory credentials:

![alt screenshot](https://raw.githubusercontent.com/lileddie/selfservepwd/master/passwdmgr.png)

If a user is locked out, or doesn't know their password, a member of the admin team (as defined in line 74 and 75 of file /etc/httpd/conf.d/passwdmgr.conf) can login to the admin site:

![alt admin-screenshot](https://raw.githubusercontent.com/lileddie/selfservepwd/master/admin-passwdmgr.png)

The Unlock Account button will reset the user's password to a static password as defined in /opt/passwdmgr/deets.py line 5.

## Issues With Python AD script

In our implementation we found that when either unlocking or modifying a users' password the "Password Never Expires" flag was being unset on the AD server.  Being unable to find a way to set this with python, the easiest way was to create a weekly powershell script to set accounts to never expire.

Copy the two powershell scripts (newSchedJob.ps1 and pwdNeverExpires.ps1) to your AD server in folder C: > Username > scripts (Create a new folder if necessary)

Change line 2 in newSchedJob.ps1 subsituting your-Server-Hostname with the hostname or IP of the AD server you are logged in to.
Change line 2 of pwdNeverExpires.ps1 with the OU group and domain name used for your implementation of AD.

With Powershell ISE open the newSchedJob.ps1 and run it.  It should create your Job and you can view it from the Task Scheduler under Microsoft > Windows > PowerShell > ScheduledJobs

## Acknoledgement

My friend, stackoverflow

Chrissy LeMaire's [awesome article on created schedule tasks using powershell.](https://blog.netnerds.net/2015/01/create-scheduled-task-or-scheduled-job-to-indefinitely-run-a-powershell-script-every-5-minutes/)

## Authors

* **Troy Schmid**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
