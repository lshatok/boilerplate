#!/bin/bash

echo -n "copying agboto_profile..."
[ -f agboto_profile ] && [ ! -f ~/.agboto_profile ] && cp agboto_profile ~/.agboto_profile && echo "[done]" || echo "[failed]"


echo -n "copying agboto_activate..."
[ -f agboto_activate ] && [ ! -f ~/.agboto_activate ] && cp agboto_activate ~/.agboto_activate && echo "[done]" || echo "[failed]"
[ -f ~/.agboto_activate ] && chmod 750 ~/.agboto_activate

if [ -f ~/.bash_profile ]; then
    echo -n "Installing .agboto_profile in ~/.bash_profile.j2..."
    Install=$( [[ $(grep 'agboto_profile' ~/.bash_profile | cut -d'#' -f1) ]] && echo "no" || echo "yes")
    if [ $Install == "yes" ]; then
        echo "[ -f ~/.agboto_profile ] && . ~/.agboto_profile" >> ~/.bash_profile
        echo "[done]"
    else
        echo "[skipped]"
        echo "  .agboto_profile already found in ~/.bash_profile.j2"
    fi
else
    echo "[WARNING] ~/.bash_profile.j2 not found.  Source .agboto_profile manually."
fi


if [ -f ~/.agboto_activate ]; then
    echo "Edit ~/.agboto_activate with your AWS ACCESS ID and SECRET KEYS as required."
    echo
fi


