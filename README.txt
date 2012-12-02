Usage : ./dmesgparser.py

This script parses the log file /var/log/dmesg. It shows duration of each
entries and builds an ascii bar graph (log scale). It assumes that the
CONFIG_PRINTK_TIME kernel option has been set.


	Jp





dmesgparser.py provides a tool like show_delta 

/usr/src/linux-headers-2.6.27-11/scripts/show_delta

dmesg > /tmp/bootup_printks
scripts/show_delta /tmp/bootup_printks

Printk Times
http://elinux.org/Printk_Times

http://www.linuxtopia.org/online_books/linux_kernel/kernel_configuration/ch09s07.html
Kernel log timestamps

The kernel outputs a wide range of messages to its log file. These messages can
be seen by looking at the system log file (usually located in
/var/log/messages), or by running the dmesg command.

Sometimes it is useful to see exactly when those messages were created. dmesg ,
however, does not put any timestamps on the events it shows, and the time
resolution of /var/log/messages is only to the nearest second. You can
configure the kernel to assign each message a timestamp that is accurate down
to the smallest measurable kernel time value (usually in the microsecond
range.)

To enable timestamp options on kernel messages:

Kernel hacking
    [*] Show timing information on printks

