https://gist.github.com/bahamat/8f5df9789c99afe482fc430bf0ea3de7

### copy dapi-cnapi.sh to headnode
### bash ./dapi-cnapi.sh [JOBUUID]

### example
#### error message
[root@centos-7 ~]# docker run -d -p 80 --name=kkw-docker-1 httpd<br>
/usr/bin/docker-current: Error response from daemon: (DockerNoComputeResourcesError) No compute resources available. (12a9771c-8415-4de9-ae54-7422f41caea3).<br>
See '/usr/bin/docker-current run --help'.<br>
#### check error
[root@headnode (bmt) ~]# bash ./cnapi.sh 6905e171-16a4-4ccc-9f72-b229f7ae3fa9<br>
<pre>
  {
    "step": "Servers with enough unreserved CPU",
    "remaining": [],
    "reasons": {
      "d8dfd424-d21d-0010-0387-0015b2a86352": "VM's calculated 25 CPU is less than server's spare 0",
      "d8dfd424-d21d-0010-0387-0015b2a86358": "VM's calculated 25 CPU is less than server's spare -900",
      "d8dfd424-d21d-0010-0387-0015b2a8637c": "VM's calculated 25 CPU is less than server's spare -400",
      "d8dfd424-d21d-0010-0387-0015b2a89204": "VM's calculated 25 CPU is less than server's spare 0"
    }
</pre>
