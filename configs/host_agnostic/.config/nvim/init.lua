vim.cmd('source ~/.config/nvim/config.vim')

-- TODO
-- - install pyright with pamac and test this (:checkhealth lsp)
-- - try jedi lsp and virtualenvs
require'lspconfig'.pyright.setup{}
