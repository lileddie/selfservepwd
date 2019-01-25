import re
from ldap3 import Server, Connection, ALL, NTLM
from deets import *

#set server to log into:
server = Server(adServer,use_ssl=True, get_info=ALL)
conn = Connection(server, user=user, password=loginpass, authentication=NTLM, auto_bind=True)

#we need to capture the user's email address from the auth header for below
#this is necessary to get the full CN of the user so we can modify their pass below
def passwordChange(username,newpassword):
    conn.search('dc=domain,dc=name', '(mail='+username+'@domain.name)')
    result=re.search('(CN=.*?),',str(conn.entries[0])).group(1)
    dn=result+',OU=Group,DC=domain,DC=name'
    #now change the password
    r=conn.extend.microsoft.modify_password(user=dn, new_password=newpassword)
    status=re.search('\'description\': \'(.*?)\'',str(conn.result)).group(1)
    return status

def passwordReset(username):
    conn.search('dc=domain,dc=name', '(mail='+username+'@domain.name)')
    result=re.search('(CN=.*?),',str(conn.entries[0])).group(1)
    dn=result+',OU=Group,DC=domain,DC=name'
    #now change the password
    r=conn.extend.microsoft.modify_password(user=dn, new_password=str(passwordReset))
    status=re.search('\'description\': \'(.*?)\'',str(conn.result)).group(1)
    return status
