### usb prepare

### head install
variable os_console vga</br>

#### adminui/cloudapi install
sdcadm post-setup common-external-nics</br>
sdcadm post-setup cloudapi</br>

### compute install
sdc-server setup -s {CN_UUID} hostname={hostname}</br>
