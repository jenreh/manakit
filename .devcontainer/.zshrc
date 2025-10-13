if command -v pyenv 1>/dev/null 2>&1; then
    eval "$(pyenv init -)"
fi

if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export PATH=$HOME/bin:/usr/local/bin:$PATH
# Disable oh-my-zsh auto-update
export DISABLE_AUTO_UPDATE="true"
export DISABLE_UPDATE_PROMPT="true"

# Load Antigen
source $WORKSPACE/.devcontainer/antigen.zsh

# Use oh-my-zsh
antigen use oh-my-zsh

# Bundles
antigen bundle command-not-found
antigen bundle common-aliases
antigen bundle docker
antigen bundle git
antigen bundle git-extras
antigen bundle npm
antigen bundle agkozak/zsh-z
antigen bundle chitoku-k/fzf-zsh-completions
antigen bundle greymd/docker-zsh-completion
antigen bundle history-substring-search
antigen bundle jenreh/zsh-autoswitch-virtualenv
antigen bundle zsh-interactive-cd
antigen bundle zsh-users/zsh-autosuggestions
antigen bundle zsh-users/zsh-completions
antigen bundle zsh-users/zsh-syntax-highlighting

# Theme
antigen theme romkatv/powerlevel10k

# Apply changes
antigen apply

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
