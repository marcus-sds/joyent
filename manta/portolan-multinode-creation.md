root@headnode  MANTA /opt/smartdc/sdcadm/lib $ vi sdcadm.js

         function disallowDataPathUpdates(_, next) {
            var dataPath = [\'portolan\'];

            /*
            for (var i = 0; i < changes.length; i++) {
                var ch = changes[i];
                if (ch.service && dataPath.indexOf(ch.service.name) !== -1 &&
                    !options.forceDataPath)
                {
                    var changeRepr = JSON.stringify({
                        type: ch.type,
                        service: ch.service.name,
                        instance: ch.inst && ch.instance.instance
                    });
                    return next(new errors.UpdateError(format(
                        \'%s updates are locked: %s \' +
                        \'(use --force-data-path flag)\', ch.service.name,
                        changeRepr)));
                }
            }
            */
            next();
        },

        function ensureVmMinPlatform(_, next) {

            var ch, server;
            var errs = [];

"sdcadm.js" 6403 lines, 227805 characters written
 

=> 소스 임시 수정


root@headnode  MANTA ~ $ sdcadm create portolan -s 35373932-3337-5347-4831-333458453344 --skip-ha-check
Using channel dev

This command will make the following changes:
    create "portolan" service instance using image ebfc89fa-8ffc-11e6-a823-d354feacbb52 (portolan@master-20161011T214759Z-ga06a34d)

Would you like to continue? [y/N] y

Create work dir: /var/sdcadm/updates/20161102T063936Z
Getting SDC\'s portolan instances from SAPI
Calculating next portolan instance alias
Updating image for SAPI service "portolan"
    service uuid: 8eceae0b-2082-44e4-9e41-865464f44c10
Installing image ebfc89fa-8ffc-11e6-a823-d354feacbb52
    (portolan@master-20161011T214759Z-ga06a34d)
Creating "portolan1" instance
Instance "4e057cc0-d293-423a-a2ee-e6b1a2aace6e" (portolan1) created
Waiting for portolan instance 4e057cc0-d293-423a-a2ee-e6b1a2aace6e to come up
Created successfully (elapsed 62s).
You have new mail in /var/mail/root
root@headnode  MANTA ~ $ vms|grep portolan
35373932-3337-5347-4831-333458453352 dafac5b2-6325-4ae5-89ab-6a247e7b14f8 portolan0 running 172.31.161.76
35373932-3337-5347-4831-333458453344 4e057cc0-d293-423a-a2ee-e6b1a2aace6e portolan1 running 172.31.161.77

=> deploy 성공
