#!/usr/bin/env bash
## Default Profile for WebTelemetry users

## Export Defaults ##
WT_PATH=/WT
WEBTELEMETRY_PATH=${WT_PATH}/grafana
DASHBOARD_PATH=${WT_PATH}/grafana
WT_PATH=${WT_PATH}/telemetrix
TELEMETRIX_PATH=${WT_PATH}/telemetrix
APP_ENV=production
JAVA_HOME="{{ java.home }}"
export TELEMETRIX_HOME=${WT_PATH}/shared

[ -f /WT/PURPOSE ] && export WT_PURPOSE="$(head -1 /WT/PURPOSE)"

## Setup Git Properties ##
# NOTE: properties do not get set if using 'tmux' #
## need to fix
#_iam=$(who am i | awk '{print $1}')
#if [ -z ${_iam} ]; then
#    GIT_AUTHOR_NAME="${_iam} (${HOSTNAME})"
#    GIT_AUTHOR_EMAIL="ai@wildrivertechnologies.com"
#    _myemail=$(grep ${_iam} /etc/passwd | cut -d: -f5)
#    if [ $(echo ${_myemail} | grep '@') ]; then
#        GIT_AUTHOR_EMAIL="${_myemail}"
#    fi
#    export GIT_AUTHOR_NAME
#    export GIT_AUTHOR_EMAIL
#fi

[ -d ${JAVA_HOME} ] && export JAVA_HOME

echo "=================================="
echo "Configuring WebTelemetry profile.."

[ -d ${WT_PATH} ] && export WT_PATH && echo "  WT_PATH = ${WT_PATH}"
if [ -d ${WEBTELEMETRY_PATH} ]; then
    export WEBTELEMETRY_PATH && echo "  WEBTELEMETRY_PATH = ${WEBTELEMETRY_PATH}"
fi
if [ -d ${DASHBOARD_PATH} ]; then
    export DASHBOARD_PATH && echo "  DASHBOARD_PATH = ${DASHBOARD_PATH}"
fi
if [ -d ${WT_PATH} ]; then
    export WT_PATH && echo "  WT_PATH = ${WT_PATH}"
fi
[ -d ${TELEMETRIX_HOME} ] && echo "  TELEMETRIX_HOME = ${TELEMETRIX_HOME}"


if [ -d ~/.rbenv/bin ]; then
    echo "  rbenv INSTALLED"
    export PATH="~/.rbenv/bin:${PATH}"
    export APP_ENV && echo "  APP_ENV = ${APP_ENV}"
fi

## Check to enable rbenv shims and autocompletion ##
if [ $(type -t rbenv) ]; then
    eval "$(rbenv init -)"
    echo "  RUBY_VER = $(ruby --version | awk '{print $1 $2}')"
fi

## webtelemetry user settings ##
if [[ $(id -un) == webtelemetry ]]; then
    if [ ${WT_CATALINA_PATH} ]; then
        export CATALINA_HOME=${WT_CATALINA_PATH}
        echo "apache-tomcat INSTALLED"
        echo "  CATALINA_HOME=${CATALINA_HOME}"
    fi
fi

## wtuser settings ##
#if [[ $(id -gn) == "wtuser" ]]; then
    # Add any wtuser specific settings here

#fi

## Aliases ##
alias less="less -nR"
alias cddw="cd ${WEBTELEMETRY_PATH}"
alias cddso="cd ${DASHBOARD_PATH}"
alias cdwt="cd ${WT_PATH}"
alias cdanal="cd ${TELEMETRIX_PATH}"
alias sudoa="sudo su - webtelemetry"


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

## if git is installed, enable git-prompt.sh ##
if [ "$PS1" ] && [ -f /usr/bin/git ] && [ -f /etc/bash_completion.d/git-prompt ]; then
    #PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\[${_Blue}\]$(__git_ps1 "(%s)")\[${_Off}\]\$ '
    PS1='${debian_chroot:+($debian_chroot)}(\A)\[${_Bold}${_Green}\]\u\[${_Off}\]@\[${_Underline}\]\h\[${_Off}\]:\[${_Blue}\]\w\[${_Off}\]$(__git_ps1 "(%s)")\$ '
    export PS1
fi

if [ ${WT_PURPOSE} ]; then
    PS1='[${WT_PURPOSE}]\n${debian_chroot:+($debian_chroot)}(\A)\[${_Bold}${_Green}\]\u\[${_Off}\]@\[${_Underline}\]\h\[${_Off}\]:\[${_Blue}\]\w\[${_Off}\]$(__git_ps1 "(%s)")\$ '
    export PS1
fi

## Add apache-ant to path ##
export PATH=$PATH:/usr/local/apache-ant/bin



# source any webtelemetry addon profiles #
if [ -d /WT/profiles/profiles.d ]; then
    _AGprofiles=$(find /WT/profiles/profiles.d -name "*.profile")
    if [ ${_AGprofiles} ]; then
        for _profile in ${_AGprofiles}; do
            source ${_profile}
        done
    fi
fi