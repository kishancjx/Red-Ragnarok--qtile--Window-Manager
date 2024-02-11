
# Imports
from libqtile import bar, layout, widget,hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import subprocess,os,re,socket
from libqtile.utils import guess_terminal
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration

# Variables
powerline_right={ "decorations": [PowerLineDecoration(path="arrow_right")] }
powerline_left={ "decorations": [PowerLineDecoration(path="arrow_left")] }
mod = "mod4" #This will setup windows key as my mod key
terminal= guess_terminal() #This will automatically try to guess the terminal


# Hooks and Functions
@hook.subscribe.startup
def autostart():
    # subprocess.run([os.path.expanduser("~/.config/qtile/autostart.fish")])
    subprocess.call(["/usr/bin/fish", "-c", os.path.expanduser("~/.config/qtile/autostart.fish")])


# Keybindings
keys = [

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    #Extras
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "f", lazy.window.toggle_fullscreen(),desc="Toggle fullscreen on the focused window",),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),


    ## Launching Stuffs
    Key(["mod1"], "space", lazy.spawn("rofi -show drun"),desc="Launch Rofi"),
    Key(["mod1","shift"],"v",lazy.spawn("xfce4-popup-clipman"),desc="open clip man for clipboard history"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod],"print",lazy.spawn("flameshot gui"),desc="Lauches Flameshot"),

]




#Workspaces
groups = [Group(i) for i in "1234567890"]
for i in groups:
    keys.extend([
        
           # mod1 + letter of group = switch to group
           Key(
               [mod],
               i.name,
               lazy.group[i.name].toscreen(),
                 desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
             Key(
                [mod, "shift"],
                 i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),

         ])


#Layouts
layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp( border_width=4,border_focus="#f40000",border_normal="#c74a4a",border_on_single=True,margin=8),
    # layout.Matrix(),
    # layout.MonadTall(border_width=4,border_focus="#f40000",border_normal="#c74a4a",margin=8),
    # layout.MonadWide(),
    # layout.RatioTile(),
   #  layout.Tile(),
   #  layout.TreeTab(),
   #  layout.VerticalTile(),
   #  layout.Zoomy(),
]


#WIDGETS
widget_defaults = dict(
    font="FiraCode",
    # font="TerminessTTF Nerd Font",
    fontsize=12,
    padding=2,
     )
extension_defaults = widget_defaults.copy()
screens = [
    Screen(
    top=bar.Bar(
            [
                widget.Image(filename="/home/kishancjx/.config/qtile/images/fire.svg"),
                  # widget.CurrentLayout(),

                widget.GroupBox(
                    fontsize=15,
                    highlight_method="line",
                    block_highlight_text_color="#ff0000",
                    highlight_color=['#000000','#000000'],
                    active="#ffffa9" , inactive="#292624",
                    disable_drag=True,
                    this_current_screen_border="#f40000",rounded=True
                    ,**powerline_left
                ),

                widget.WindowName(
                    format="  {state}{name}",
                    fmt='<i><b>{}</b></i>',
                    empty_group_string="                 KISHANCJX THE GREAT                 ",
                    foreground="#000000",
                    background="#ff0000",**powerline_right,fontsize=15,max_chars=55,
                ),


                widget.TextBox(
                        font="FontAwesome",
                        text="  ",
                        foreground="#ffffa9",
                        background="#000000",
                        padding = 0,
                        fontsize=16
                ),
                               
                widget.CPU(
                    format='CPU: {load_percent:.0f}%',
                    fontsize=12,foreground="#ffffa9",
                    fmt="<b>{}</b>"
                ),

                widget.ThermalSensor(
                    tag_sensor="Tctl",
                    format=' | {temp:.0f}{unit}',
                    **powerline_left,
                    fontsize=12,
                    fmt='<b>{}</b>',
                    foreground="#ffffa9"
                ),

                 widget.TextBox(
                        font="FontAwesome",
                        text="  ",
                        foreground="#000000",
                        background="#14a2ff",
                        padding = 0,
                        fontsize=16
                 ),

                widget.Memory(
                    fmt='<b>{}</b>',format='RAM:{MemUsed: .0f}{mm} / 16000{mm}',
                    padding=5,**powerline_left,
                    background="#14a2ff",foreground="#000000",fontsize=12
                ),

                widget.Prompt(),
                
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
            
                widget.Systray(
                    foreground="#000000",
                    background="#780000",**powerline_right,
                    padding=5,icon_size=20
                ),
              
                widget.Clock(
                    fmt="<b>{}</b>",
                    format="%d-%m-%Y %a %I:%M %p ",
                    **powerline_right,background="#bb4504",
                    fontsize=12,foreground="#ffffa9"
                ),
                  
            ],
            24,
        ),
    ),
]



# Drag floating layouts
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]



#Floating Rules
dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(border_width=3,border_normal="#c74a4a" ,border_focus="#f40000",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True
# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None
wmname = "xzaack"


# #########################################################
# ################ assgin apps to groups ##################
# #########################################################
# # @hook.subscribe.client_new
# # def assign_app_group(client):
# #     d = {}
# #     #####################################################################################
# #     ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
# #     #####################################################################################
# #     d[group_names[0]] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
# #               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
# #     d[group_names[1]] = [ "Atom", "Subl", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
# #                "atom", "subl", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
# #     d[group_names[2]] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
# #               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
# #     d[group_names[3]] = ["Gimp", "gimp" ]
# #     d[group_names[4]] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
# #     d[group_names[5]] = ["Vlc","vlc", "Mpv", "mpv" ]
# #     d[group_names[6]] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
# #               "virtualbox manager", "virtualbox machine", "vmplayer", ]
# #     d[group_names[7]] = ["Thunar", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
# #               "thunar", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
# #     d[group_names[8]] = ["Evolution", "Geary", "Mail", "Thunderbird",
# #               "evolution", "geary", "mail", "thunderbird" ]
# #     d[group_names[9]] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
# #               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
# #     ######################################################################################
# #
# # wm_class = client.window.get_wm_class()[0]
# #
# #     for i in range(len(d)):
# #         if wm_class in list(d.values())[i]:
# #             group = list(d.keys())[i]
# #             client.togroup(group)
# #             client.group.cmd_toscreen(toggle=False)

# # END
# # ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME

# main = None

# # hides the top bar when the archlinux-logout widget is opened
# @hook.subscribe.client_new
# def new_client(window):
#     if window.name == "ArchLinux Logout":
#         qtile.hide_show_bar()

# # shows the top bar when the archlinux-logout widget is closed
# @hook.subscribe.client_killed
# def logout_killed(window):
#     if window.name == "ArchLinux Logout":
#         qtile.hide_show_bar()

# @hook.subscribe.startup_once
# def start_once():
#     home = os.path.expanduser('~')
#     subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

# @hook.subscribe.startup
# def start_always():
#     # Set the cursor to something sane in X
#     subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

# @hook.subscribe.client_new
# def set_floating(window):
#     if (window.window.get_wm_transient_for()
#             or window.window.get_wm_type() in floating_types):
#         window.floating = True

# floating_types = ["notification", "toolbar", "splash", "dialog"]


# follow_mouse_focus = True
# bring_front_click = False
# cursor_warp = False
# floating_layout = layout.Floating(float_rules=[
#     # Run the utility of `xprop` to see the wm class and name of an X client.
#     *layout.Floating.default_float_rules,
#     Match(wm_class='confirmreset'),  # gitk
#     Match(wm_class='makebranch'),  # gitk
#     Match(wm_class='maketag'),  # gitk
#     Match(wm_class='ssh-askpass'),  # ssh-askpass
#     Match(title='branchdialog'),  # gitk
#     Match(title='pinentry'),  # GPG key password entry
#     Match(wm_class='Arcolinux-welcome-app.py'),
#     Match(wm_class='Arcolinux-calamares-tool.py'),
#     Match(wm_class='confirm'),
#     Match(wm_class='dialog'),
#     Match(wm_class='download'),
#     Match(wm_class='error'),
#     Match(wm_class='file_progress'),
#     Match(wm_class='notification'),
#     Match(wm_class='splash'),
#     Match(wm_class='toolbar'),
#     Match(wm_class='Arandr'),
#     Match(wm_class='feh'),
#     Match(wm_class='Galculator'),
#     Match(wm_class='archlinux-logout'),
#     Match(wm_class='xfce4-terminal'),

# ],  fullscreen_border_width = 0, border_width = 0)
# auto_fullscreen = True

# focus_on_window_activation = "focus" # or smart

# wmname = "LG3D"
