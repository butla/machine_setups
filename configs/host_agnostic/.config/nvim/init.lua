vim.cmd('source ~/.config/nvim/config.vim')

-- LSP setup (nvim 0.11+ native API; nvim-lspconfig provides server definitions via runtimepath)
-- pyright detects the active virtualenv via VIRTUAL_ENV env var + python in PATH,
-- which the v() shell function sets before launching nvim.
local cmp_lsp_ok, cmp_lsp = pcall(require, 'cmp_nvim_lsp')
vim.lsp.config('pyright', {
  capabilities = cmp_lsp_ok and cmp_lsp.default_capabilities() or nil,
  settings = {
    python = {
      analysis = {
        autoSearchPaths = true,
        useLibraryCodeForTypes = true,
      }
    }
  }
})
vim.lsp.enable('pyright')

-- Completion setup
local cmp_ok, cmp = pcall(require, 'cmp')
if cmp_ok then
  cmp.setup({
    snippet = {
      expand = function(args) vim.snippet.expand(args.body) end,
    },
    mapping = cmp.mapping.preset.insert({
      ['<C-Space>'] = cmp.mapping.complete(),
      ['<CR>']      = cmp.mapping.confirm({ select = true }),
      ['<Tab>']     = cmp.mapping(function(fallback)
        if cmp.visible() then cmp.select_next_item() else fallback() end
      end, { 'i', 's' }),
      ['<S-Tab>']   = cmp.mapping(function(fallback)
        if cmp.visible() then cmp.select_prev_item() else fallback() end
      end, { 'i', 's' }),
    }),
    sources = cmp.config.sources({ { name = 'nvim_lsp' } }),
  })
end

-- Treesitter setup
local ts_ok, treesitter = pcall(require, 'nvim-treesitter.configs')
if ts_ok then
  treesitter.setup({
    ensure_installed = {
      'python', 'lua', 'vim', 'vimdoc', 'bash',
      'yaml', 'json', 'toml',
      'markdown', 'markdown_inline',
      'html', 'css',
    },
    highlight = {
      enable = true,
      additional_vim_regex_highlighting = false,
    },
    indent = { enable = true },
  })
end

-- Neo-tree config
require("neo-tree").setup({
  close_if_last_window = false,
  popup_border_style = "rounded",
  enable_git_status = true,
  enable_diagnostics = true,
  filesystem = {
    window = {
      position = "left",
      width = 70,
    },
    filtered_items = {
      hide_dotfiles = false,
      hide_gitignored = true,
      hide_by_name = { ".git" },
    },
  },
})
