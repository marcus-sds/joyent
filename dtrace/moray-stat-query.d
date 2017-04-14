#!/usr/sbin/dtrace -s
#pragma D option quiet
#pragma D option dynvarsize=16m
#pragma D option bufsize=10m

moray*:::query-start
{
  starts[copyinstr(arg0)] = timestamp;
}

moray*:::query-done
/starts[copyinstr(arg0)] && (timestamp - starts[copyinstr(arg0)]) < 1000000/
{
        starts["1ms-under"]++;
}

moray*:::query-done
/starts[copyinstr(arg0)] && (timestamp - starts[copyinstr(arg0)]) >= 1000000 && (timestamp - starts[copyinstr(arg0)]) < 10000000 /
{
        starts["1ms-over"]++;
}

moray*:::query-done
/starts[copyinstr(arg0)] && (timestamp - starts[copyinstr(arg0)]) >= 10000000 /
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

profile:::tick-10sec
{
        exit(0);
}
