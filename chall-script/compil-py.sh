rm ctf_script
rm ctf_script.c

~/.local/bin/cython --embed -o ctf_script.c ctf_script.pyx
gcc -o ctf_script ctf_script.c -I/usr/include/python3.11 -lpython3.11
