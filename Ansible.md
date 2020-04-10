# ANSIBLE 

* Most likely, in Ubuntu, connecting to the remote server cannot be performed with root. If so, enable it:

```bash
jlhernandez@Ubuntu1804:~$ sudo su -
[sudo] password for jlhernandez: 

root@Ubuntu1804:~# passwd
Enter new UNIX password: 
Retype new UNIX password: 
passwd: password updated successfully

root@Ubuntu1804:~/.ssh# vi /etc/ssh/sshd_config
PermitRootLogin yes

root@Ubuntu1804:~/.ssh# service sshd restart
```

* Test access from Ansible host
```bash
jlhernandez@Julians-MBP .ssh % ssh root@192.168.86.188
root@192.168.86.188 s password: 
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 5.3.0-46-generic x86_64)
```


* Create a passwordless ssh key on the remote Ubuntu host and copy it to the Ansible host

```bash
root@Ubuntu1804:~/.ssh# ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa_centos01
Generating public/private rsa key pair.
Your identification has been saved in /root/.ssh/id_rsa_centos01.
Your public key has been saved in /root/.ssh/id_rsa_centos01.pub.
The key fingerprint is:
SHA256:mrNexDF0SzTN+Q0w6Mjt6PFUSdNjCFU3LNxODBA+qww root@Ubuntu1804
The keys randomart image is:
+---[RSA 2048]----+
|        ..*OBB*..|
|       . oooB+=*.|
|       .o+.+ =++ |
|       .ooo = ...|
|       ESo o     |
|       += +      |
|      +..*       |
|       +. .      |
|     .o          |
+----[SHA256]-----+
```
