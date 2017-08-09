au BufNewFile,BufRead *.{js,jsm,es,es6},Jakefile setf javascript

fun! s:SourceFlowSyntax()
  if !exists('javascript_plugin_flow') && !exists('b:flow_active') &&
        \ search('\v\C%^\_s*%(//\s*|/\*[ \t\n*]*)\@flow>','nw')
    runtime extras/flow.vim
    let b:flow_active = 1
  endif
endfun
au FileType javascript au BufRead,BufWritePost <buffer> call s:SourceFlowSyntax()

fun! s:SelectJavascript()
  if getline(1) =~# '^#!.*/bin/\%(env\s\+\)\?node\>'
    set ft=javascript
  endif
endfun
au BufNewFile,BufRead * call s:SelectJavascript()
au BufNewFile,BufRead .tern-project setf json
au BufNewFile,BufRead .tern-config setf json
autocmd BufNewFile,BufRead *.json setlocal filetype=json
autocmd BufNewFile,BufRead *.jsonp setlocal filetype=json
autocmd BufNewFile,BufRead *.geojson setlocal filetype=json
