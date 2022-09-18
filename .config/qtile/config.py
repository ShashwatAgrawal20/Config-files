################################################################
########################     IMPORTS     #######################
################################################################

import os
import re
import socket
import subprocess
from libqtile import bar, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Backlight, Spacer
from libqtile.widget.image import Image
from libqtile.dgroups import simple_key_binder

mod = "mod4"
myTerminal = "kitty"  # guess_terminal()
Primary_Menu = "dmenu_run"

################################################################
########################   KEYBINDINGS   #######################
################################################################

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(myTerminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),


    Key([mod], "p", lazy.spawn(Primary_Menu),
        desc="Launch Dmenu"),  # Launching the Dmenu

    Key(["control", "shift"], "e", lazy.spawn("emacsclient -c -a 'emacs'"),
        desc='Doom Emacs'),  # Launch EmacsClient
]

################################################################
########################      COLORS      ######################
################################################################

# Dracula

colors = [["#282a36", "#282a36"],  # background (dark grey) [0]
          ["#44475a", "#44475a"],  # light grey [1]
          ["#f8f8f2", "#f8f8f2"],  # forground (white) [2]
          ["#6272a4", "#6272a4"],  # blue/grey) [3]
          ["#8be9fd", "#8be9fd"],  # cyan [4]
          ["#50fa7b", "#50fa7b"],  # green [5]
          ["#ffb86c", "#ffb86c"],  # orange [6]
          ["#ff79c6", "#ff79c6"],  # pink [7]
          ["#bd93f9", "#bd93f9"],  # purple [8]
          ['#ff5555', '#ff5555'],  # red [9]
          ["#f1fa8c", "#f1fa8c"]]  # yellow [10]


# colors = [["#2B3339", "#2B3339"],  #background (dark grey) [0]
# ["#7C8377", "#7C8377"],  #light grey [1]
# ["#D5C9AB", "#D5C9AB"],  #forground (beige) [2]
# ["#6272a4", "#6272a4"],  #blue/grey) [3]
# ["#7FBBB3", "#7FBBB3"],  #blue [4]
# ["#A7C080", "#A7C080"],  #green [5]
# ["#E69875", "#E69875"],  #orange [6]
# ["#D196B3", "#D196B3"],  #pink [7]
# ["#A7C080", "#A7C080"],  #green [8]
# ['#ED8082', '#ED8080'],  #red [9]
# ["#D5C9AB", "#D5C9AB"]]  #beige [10]

################################################################
########################    WORKSPACES    ######################
################################################################

groups = [Group(name="1", label="", layout="monadtall"),
          Group(name="2", label="", layout="monadtall"),
          Group(name="3", label="", layout="monadtall"),
          Group(name="4", label="", layout="monadtall"),
]

dgroups_key_binder = simple_key_binder(mod)


for i in groups:
    keys.extend(
        [
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
                desc="Switch to & move focused window to group {}".format(
                    i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

################################################################
########################     LAYOUTS      ######################
################################################################

layouts = [
    layout.MonadTall(border_focus=colors[3], margin=2),
    layout.Max(),

    #layout.Columns(border_focus = colors[3], margin = 5),
    # layout.Max(),
    #layout.Bsp(border_focus = colors[3], margin = 2),
    #layout.RatioTile(border_focus = colors[3], margin = 2),
    #layout.Tile(border_focus = colors[3], margin = 2),
    # layout.Max()
    #layout.MonadTall(border_focus = colors[3], margin = 2),
    #layout.MonadWide(border_focus = colors[3], margin = 2),
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize=10,
    padding=2,
    background=colors[0],
)
extension_defaults = widget_defaults.copy()

################################################################
########################      Top Bar     ######################
################################################################

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename='~/.config/qtile/icon/python.png',
                    scale='False',
                    margin_x=5,
                    mouse_callbacks={
                        'Button1': lambda: qtile.cmd_spawn(Primary_Menu)}
                ),

                widget.Sep(
                    linewidth=2,
                    padding=5,
                    foreground=colors[2]
                ),

                widget.GroupBox(
                    margin_x=5,
                    active=colors[2],
                    inactive=["FFD43B"],
                    highlight_color=["#2B3339", "4B8BBE"],
                    highlight_method='line',
                ),

                widget.Prompt(),

                widget.Sep(
                    linewidth=2,
                    padding=5,
                    foreground=colors[2]
                ),

                widget.WindowName(
                    foreground=colors[5]
                ),

                widget.Chord(
                    chords_colors={
                        "launch": ("#ff5555", "#ff5555"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(),

                widget.Sep(
                    linewidth=2,
                    padding=5,
                    foreground=colors[2]
                ),

                widget.Net(
                    interface='wlan0',
                    format=' {down} ↓↑ {up}',
                    padding=5,
                    foreground=colors[7],
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                        myTerminal + ' -e nmtui')},
                ),

                widget.Sep(
                    linewidth=2,
                    padding=5,
                    foreground=colors[2]
                ),

                widget.CPU(
                    format=' {freq_current}GHz {load_percent}%',
                    padding=10,
                    foreground=colors[10],
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                        myTerminal + ' -e htop')},
                ),

                widget.Sep(
                    linewidth=2,
                    padding=5,
                    foreground=colors[2]
                ),

                widget.Memory(
                    foreground=colors[4],
                    fmt=' {}',
                    padding=10,
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                        myTerminal + ' -e htop')},

                ),

                widget.Sep(
                    linewidth=2,
                    padding=5,
                    foreground='#ffffff'
                ),

                widget.Clock(
                    format=' %a %d %m %Y |  %I:%M %p',
                    foreground=colors[8],
                    padding=10,
                ),

                widget.Sep(
                    linewidth=2,
                    padding=5,
                    foreground='#ffffff'
                ),

                widget.QuickExit(
                    fmt=' ',
                    foreground=colors[9],
                    padding=10
                ),

            ],
            20,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_focus = colors[8],
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


################################################################
########################   AUTOSTARTUP   #######################
################################################################

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
