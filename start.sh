if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Tsunemoriii-3/Streamm.git /Streamm
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone https://github.com/Tsunemoriii-3/Streamm /Streamm
fi
cd /Streamm
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 -m Powers
