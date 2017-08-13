#!/bin/bash

TARGETS=(.vim)

# utility functions
yn_prompt() {
    while true ; do
        read INPUT
        case "$INPUT" in
            'y' )
                echo 0
                break ;;
            'n' )
                echo 1
                break ;;
            * )
                ;;
        esac
    done
}

create_copy_r() {
    local pwd_target=$1
    local home_target=$2
    echo "cp -r $pwd_target $home_target"
    cp -r $pwd_target $home_target
}


# Copy
for target in ${TARGETS[@]}; do
    pwd_target="$PWD/$target"
    home_target="$HOME/$target"
    home_backup="$HOME/$target"_
    if [ ! -e $pwd_target ]; then
        echo "[Error] not exist $pwd_target"
    elif [ -e $home_target ]; then
        echo -n "[Ask] $home_target is already exist. Move? [y/n] "
        ret=`yn_prompt`
        if [ $ret -eq 0 ]; then
            echo "mv $home_target $home_backup"
            mv $home_target $home_backup
            create_copy_r $pwd_target $home_target
        fi
    else
        create_copy_r $pwd_target $home_target
    fi
done
