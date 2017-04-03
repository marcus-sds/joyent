### usb prepare

### head install
variable os_console vga</br>

#### adminui/cloudapi install
sdcadm post-setup common-external-nics</br>
sdcadm post-setup cloudapi</br>

### compute install
sdc-server setup -s {CN_UUID} hostname={hostname}</br>

### channel
sdcadm channel set release</br>
sdcadm channel list</br>

### allow local image create
echo '{"metadata": {"IMGAPI_ALLOW_LOCAL_CREATE_IMAGE_FROM_VM": true}}' | sapiadm update $(sdc-sapi /services?name=imgapi | json -H 0.uuid)<br>
