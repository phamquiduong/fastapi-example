
echo "################################## Run nginx"
export DOLLAR='$'
envsubst < /tmp/nginx.conf.template > /etc/nginx/nginx.conf # /etc/nginx/conf.d/default.conf

chmod 644 /etc/crontab && /etc/init.d/cron restart
nginx -g "daemon off;"