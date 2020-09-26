#!/bin/sh

sort -u edgelist.txt > edgelist.unique
awk '{ split($0, a, " "); print a[1]; split(a[2], b, "/"); print b[1] }' edgelist.unique > nodelist.mega
sort -u nodelist.mega > nodelist.unique
rm nodelist.mega
