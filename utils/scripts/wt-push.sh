#!/usr/bin/expect -f
cd  ~/src/ai
spawn git commit -am"latest"
spawn git  push
expect "Username for 'https://github.com':"
send "lshatok";
send "\n";
expect "Password for 'https://lshatok@github.com':"
send "ther3dpi11";
send "\n";
interact
