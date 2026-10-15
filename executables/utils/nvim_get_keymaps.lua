
-- Export global Neovim mappings as a JSON overlay.
-- Run with:
--   nvim --headless -l ~/.config/nvim/export-keymap-overlay.lua
--
-- Output:
--   ~/.config/nvim/keymap-overlay.json

local output = vim.fn.stdpath("config") .. "/keymap-overlay.json"

local mode_info = {
  { id = "normal",          label = "Normal mode",          mode = "n" },
  { id = "visual",          label = "Visual mode",          mode = "x" },
  { id = "select",          label = "Select mode",          mode = "s" },
  { id = "operator-pending",label = "Operator-pending mode",mode = "o" },
  { id = "insert",          label = "Insert mode",          mode = "i" },
  { id = "command-line",    label = "Command-line mode",    mode = "c" },
  { id = "terminal",        label = "Terminal mode",        mode = "t" },
}

local modifier_names = {
  C = "CTRL",
  S = "SHIFT",
  M = "ALT",
  A = "ALT",
  D = "CMD",
}

-- Split a mapping lhs into individual keys, keeping <...> tokens intact.
local function split_keys(lhs)
  local keys = {}
  local i = 1

  while i <= #lhs do
    if lhs:sub(i, i) == "<" then
      local j = lhs:find(">", i, true)
      if j then
        keys[#keys + 1] = lhs:sub(i, j)
        i = j + 1
      else
        keys[#keys + 1] = vim.fn.strcharpart(lhs, #keys, 1)
        i = i + 1
      end
    else
      local rest = lhs:sub(i)
      local char = vim.fn.strcharpart(rest, 0, 1)
      keys[#keys + 1] = char
      i = i + #char
    end
  end

  return keys
end

-- Convert one key into the reference format, e.g. <C-d> -> CTRL-D.
local function format_key(key)
  local inner = key:match("^<(.-)>$")

  if not inner then
    return key
  end

  local parts = {}
  for part in inner:gmatch("[^%-]+") do
    parts[#parts + 1] = part
  end

  if #parts == 1 then
    return parts[1]:upper()
  end

  local result = {}
  for i = 1, #parts - 1 do
    local mod = parts[i]:upper()
    result[#result + 1] = modifier_names[mod] or mod
  end

  result[#result + 1] = parts[#parts]:upper()
  return table.concat(result, "-")
end

-- Describe the first key using base + mods.
local function first_key(key)
  local inner = key:match("^<(.-)>$")

  if not inner then
    return {
      base = key,
      mods = {},
    }
  end

  local parts = {}
  for part in inner:gmatch("[^%-]+") do
    parts[#parts + 1] = part
  end

  local mods = {}
  for i = 1, #parts - 1 do
    mods[#mods + 1] = parts[i]:upper()
  end

  local base = parts[#parts]

  -- Match the reference convention: CTRL-D has base "d".
  if #mods > 0 and #base == 1 then
    base = base:lower()
  end

  return {
    base = base,
    mods = mods,
  }
end

local result = { modes = {} }

for _, info in ipairs(mode_info) do
  local mode_result = {
    id = info.id,
    label = info.label,
    commands = {},
  }

  for _, mapping in ipairs(vim.api.nvim_get_keymap(info.mode)) do
    local raw_keys = split_keys(mapping.lhs)
    local keys = {}

    for _, key in ipairs(raw_keys) do
      keys[#keys + 1] = format_key(key)
    end

    local desc = mapping.desc
    if not desc or desc == "" then
      desc = mapping.rhs ~= "" and mapping.rhs or "(no description)"
    end

    mode_result.commands[#mode_result.commands + 1] = {
      keys = keys,
      first = first_key(raw_keys[1] or ""),
      desc = desc,
    }
  end

  result.modes[#result.modes + 1] = mode_result
end

local file, err = io.open(output, "w")
if not file then
  error("Could not write " .. output .. ": " .. err)
end

-- Pretty-print JSON with two-space indentation.
local function pretty_json(value, indent)
  indent = indent or 0
  local pad = string.rep(" ", indent)
  local child_pad = string.rep(" ", indent + 2)

  if type(value) ~= "table" then
    return vim.json.encode(value)
  end

  local is_array = vim.islist(value)
  local parts = {}

  if is_array then
    for _, v in ipairs(value) do
      parts[#parts + 1] =
        child_pad .. pretty_json(v, indent + 2)
    end

    if #parts == 0 then
      return "[]"
    end

    return "[\n" .. table.concat(parts, ",\n")
      .. "\n" .. pad .. "]"
  end

  for k, v in pairs(value) do
    parts[#parts + 1] =
      child_pad .. vim.json.encode(k) .. ": "
      .. pretty_json(v, indent + 2)
  end

  if #parts == 0 then
    return "{}"
  end

  return "{\n" .. table.concat(parts, ",\n")
    .. "\n" .. pad .. "}"
end

file:write(pretty_json(result), "\n")
file:close()

print("Wrote keymap overlay to " .. output)

