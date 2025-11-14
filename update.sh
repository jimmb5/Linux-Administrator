# kansioon :
cd /home/ubuntu/lemp-app || exit 1

echo " pullataan main "
git pull

echo "restartataan palvelut jotta app.py päivittyy"
sudo systemctl daemon-reload
sudo systemctl enable lemp-app
sudo systemctl restart lemp-app

echo "valmis"
