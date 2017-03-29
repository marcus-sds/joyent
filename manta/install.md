### headnode
/usbkey/scripts/setup_manta_zone.sh</br>
muuid=$(updates-imgadm list name=manta-marlin --latest -H -o uuid)</br>
curl -kO https://us-east.manta.joyent.com/Joyent_Dev/public/Manta/manta-marlin-image/$muuid.imgmanifest<br>
curl -kO -C - https://us-east.manta.joyent.com/Joyent_Dev/public/Manta/manta-marlin-image/$muuid.file.gz<br>
sdc-imgadm import -m $muuid.imgmanifest -f $muuid.file.gz<br>

/zones/$(vmadm lookup alias=manta0)/root/opt/smartdc/manta-deployment/networking/gen-coal.sh > /var/tmp/netconfig.json<br>
ln -s /zones/$(vmadm lookup alias=manta0)/root/opt/smartdc/manta-deployment/networking /var/tmp/networking<br>
cd /var/tmp/networking<br>

./manta-net.sh /var/tmp/netconfig.json<br>


### manta node
manta-init -e i@localhost -s production -m [marlin-image-uuid]<br>

manta-shardadm set -i "1.moray"<br>
manta-shardadm set -m "1.moray"<br>
manta-shardadm set -s "1.moray"<br>
manta-create-topology.sh -v 100000 -p 2020<br>
manta-adm genconfig lab > /var/tmp/lab-config.json<br>

manta-adm update -y /var/tmp/lab-config.json nameservice <br>
manta-adm update -y /var/tmp/lab-config.json <br>
manta-marlin -s [storage-node-uuid]
- madtom and marlin-dashboard deploy

### metering configuration
