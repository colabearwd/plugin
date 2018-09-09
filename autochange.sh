grep -Ilr push_url  ./ | xargs -n1 -- sed -i 's/1.1.1.1/1.1.1.1/g'
