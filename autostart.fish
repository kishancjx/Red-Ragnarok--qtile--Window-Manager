#!/usr/bin/fish


#compositor
picom -b &

#wallpaper using nitrogen
nitrogen --restore &

#to start clipman at the beginning
xfce4-clipman &

#flameshot
flameshot &

#set capslock as escape key
setxkbmap -option caps:swapescape &

