#!/usr/bin/bash
gcc -Werror -Wall generator.c -o generator
./generator
mv test-cases.txt ../Backend/test-cases.txt
mv sections.txt ../Backend/sections.txt
rm generator
