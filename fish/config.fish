# Homebrew on Apple Silicon
if test -x /opt/homebrew/bin/brew
    /opt/homebrew/bin/brew shellenv | source
end
fish_add_path ~/.local/bin ~/.cargo/bin

if status is-interactive
    # No greeting
    set fish_greeting

    # Use starship
    function starship_transient_prompt_func
        starship module character
    end
    starship init fish | source
    enable_transience

    # Smarter cd: `z myproject` jumps to a folder once visited
    zoxide init fish | source

    # Shell history: Ctrl+R searches, Up arrow left alone (fish's own history is nicer there)
    atuin init fish --disable-up-arrow | source

    # Aliases
    # kitty doesn't clear properly so we need to do this weird printing
    alias clear "printf '\033[2J\033[3J\033[1;1H'"
    alias celar "printf '\033[2J\033[3J\033[1;1H'"
    alias claer "printf '\033[2J\033[3J\033[1;1H'"
    alias c 'claude'
    alias ls 'eza --icons'
    if test "$TERM" = "xterm-kitty"
        alias ssh 'kitten ssh'
    end
end
