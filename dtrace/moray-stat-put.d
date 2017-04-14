#!/usr/sbin/dtrace -s
#pragma D option quiet
#pragma D option dynvarsize=16m
#pragma D option bufsize=10m

moray*:::putobject-start
{
        latency[arg0] = timestamp;
        bucket[arg0] = copyinstr(arg2);
        key[arg0] = copyinstr(arg3);
}

moray*:::putobject-done
/latency[arg0] && (timestamp - latency[arg0]) < 5000000/
{
        starts["1ms-under"]++;
}

moray*:::putobject-done
/latency[arg0] && (timestamp - latency[arg0]) >= 5000000 && (timestamp - latency[arg0]) < 10000000/
{
        starts["1ms-over"]++;
}

moray*:::putobject-done
/latency[arg0] && (timestamp - latency[arg0]) >= 10000000/
{
        starts["10ms-over"]++;
}


profile:::tick-1sec
{
        printf("%d %d %d\n", starts["1ms-under"], starts["1ms-over"], starts["10ms-over"]
        );
        starts["1ms-under"] = 0;
        starts["1ms-over"] = 0;
        starts["10ms-over"] = 0;
}

/* End of program */
profile:::tick-10sec
{
        exit(0);
}
