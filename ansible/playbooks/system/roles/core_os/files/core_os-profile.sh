#!/usr/bin/env bash
## core_os-profile.sh deployed via bootstraps ##

# Format shell prompt #

if [[ -z ${USER} ]]; then
    USER=$(/usr/bin/whoami)
fi

### tput colors ###
#  - tput doesn't cause wrapping issues -  #
_Black=$(tput setaf 0)
_Red=$(tput setaf 1)
_Green=$(tput setaf 2)
_Yellow=$(tput setaf 3)
_Blue=$(tput setaf 4)
_Magenta=$(tput setaf 5)
_Cyan=$(tput setaf 6)
_Reverse=$(tput rev)
_Underline=$(tput smul)
_Underline_Off=$(tput rmul)
_Bold=$(tput bold)
_Off=$(tput sgr0)

ROOTUSER=${_Bold}${_Red}${_Underline}-ROOT-${_Off}

if [[ -n ${PS1} ]]; then
    case $USER in
        root)   PS1="(\A)[${ROOTUSER}@${_Bold}\h${_Off}:\w]\$ "
                ;;
        *)      PS1="(\A)[${_Bold}${_Green}${USER}${_Off}@${_Underline}\h${_Off}:\w]\$ "
                ;;
    esac
    export PS1
fi

export EDITOR=vim
