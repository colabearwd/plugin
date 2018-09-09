grep -Ilr push_url  ./ | xargs -n1 -- sed -i 's/1.1.1.1/1.1.1.1/g'

chmod +x get-args/*
chmod +x rasp-plugin/*
chmod +x ubuntu-plugin/*
