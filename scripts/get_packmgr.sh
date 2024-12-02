source /etc/os-release

if [[ $ID_LIKE == 'debian' || $ID == 'debian' ]];then
    echo -n "apt"
fi
if [[ $ID == 'fedora' || $ID_LIKE == 'fedora' ]];then
    echo -n "dnf"
fi
if [[ $ID == 'arch' || $ID_LIKE == 'arch' ]];then
    echo -n "pacman"
fi