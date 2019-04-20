grep -Ilr push_url  ./ | xargs -n1 -- sed -i 's/1.1.1.1/1.1.1.1/g'
grep -Ilr push_url  ./ | xargs -n1 -- sed -i 's/mysql_account/root/g'
grep -Ilr push_url  ./ | xargs -n1 -- sed -i 's/mysql_passwd/passwd/g'
grep -Ilr push_url  ./ | xargs -n1 -- sed -i 's/mysql_database/myproject/g'

chmod +x get-args/*
chmod +x rasp-plugin/*
chmod +x ubuntu-plugin/*
