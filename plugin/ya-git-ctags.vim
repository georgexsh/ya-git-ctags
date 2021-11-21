if exists("g:ya_git_ctags_loaded")
    finish
endif
let g:ya_git_ctags_loaded = 1


let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 <<EOF
import site
import vim

plugin_root_dir = vim.eval('s:plugin_root_dir')
site.addsitedir(plugin_root_dir)

import git_ctags
EOF


function! s:generate_tags()
    if &readonly
        return
    endif
    python3 git_ctags.run(vim.eval("expand('%:p')"))
endfunction


function! s:delay_gen_tags()
    let t = timer_start(20,  { -> s:generate_tags() })
endfunction


command Ctags call s:generate_tags()
command DelayCtags call s:delay_gen_tags()
