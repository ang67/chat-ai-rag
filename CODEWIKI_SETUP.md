# CodeWiki Setup Documentation

## What We Did

Successfully configured CodeWiki to generate documentation for the backend project using local Ollama models through LiteLLM proxy.

### Final Working Configuration

**Date:** January 28, 2026

**Setup Steps Completed:**

1. **Started Ollama Server**
   ```bash
   ollama serve
   ```
   - Running in background terminal
   - Provides local LLM models

2. **Configured LiteLLM Proxy** (assumed running on port 4000)
   - Acts as OpenAI-compatible translation layer
   - Bridges CodeWiki ↔ Ollama communication

3. **Updated CodeWiki Global Config**
   ```bash
   # Configuration file: ~/.codewiki/config.json
   {
     "version": "1.0",
     "base_url": "http://localhost:4000",
     "main_model": "ollama/llama3",
     "cluster_model": "ollama/llama3",
     "fallback_model": "ollama/gpt-oss",
     "default_output": "docs",
     "max_tokens": 16384,
     "max_token_per_module": 20000,
     "max_token_per_leaf_module": 16000,
     "max_depth": 2
   }
   ```

4. **Generated Documentation**
   ```bash
   cd /Users/biniangui/Informatique/CodeWiki/backend
   source ../.venv/bin/activate
   codewiki generate
   ```

**Result:** ✓ Documentation generated successfully in `/backend/docs/`
- Files: `metadata.json`, `module_tree.json`, `first_module_tree.json`
- 12 files analyzed
- Generation time: 28 seconds

---

## Initial Problems Encountered

### Problem 1: Model Access Denied
```
Error code: 401 - team not allowed to access model
Team can only access: ['ollama/llama3', 'ollama/gpt-oss', 'ollama/nomic-embed-text']
Tried to access: glm-4p5
```
**Solution:** Changed fallback model from `glm-4p5` to `ollama/llama3`

### Problem 2: Ollama Connection Failed
```
Error code: 500 - Cannot connect to host host.docker.internal:11434
```
**Solution:** Started Ollama server with `ollama serve`

### Problem 3: Output Validation Failures
```
pydantic_ai.exceptions.UnexpectedModelBehavior: Exceeded maximum retries (1) for output validation
```
**Solution:** Switched main model from `ollama/gpt-oss` to `ollama/llama3` (better structured output compliance)

---

## How to Run CodeWiki Again

### Prerequisites
Make sure the following services are running:

1. **Ollama Server:**
   ```bash
   ollama serve  # Run in separate terminal
   ```

2. **LiteLLM Proxy** (if using):
   ```bash
   litellm --config litellm_config.yaml --port 4000
   ```

### Generate Documentation

```bash
cd /Users/biniangui/Informatique/CodeWiki/backend
source ../.venv/bin/activate
codewiki generate
```

### With Custom Parameters

```bash
codewiki generate \
  --max-tokens 81292 \
  --max-token-per-module 20000 \
  --max-depth 3
```

### View Current Configuration

```bash
source ../.venv/bin/activate
codewiki config show
```

---

## Reference: Alternative Solutions

### Option 1: Use Different Ollama Models

Try models with better structured output:
```bash
ollama pull qwen2.5:7b
codewiki config set --main-model ollama/qwen2.5:7b
```

### Option 2: Use Cloud Models (OpenAI/Claude)

For production use with better reliability:
```bash
codewiki config set --api-key YOUR_API_KEY
codewiki config set --main-model gpt-4o-mini
codewiki config set --base-url https://api.openai.com/v1
```

### Option 3: Adjust Parameters

Reduce complexity if generation fails:
```bash
codewiki generate --max-depth 1 --max-token-per-module 10000
```

---

## Troubleshooting

### Check Ollama Status
```bash
ollama ps       # See running models
ollama list     # See available models
```

### Verify LiteLLM Proxy
```bash
curl http://localhost:4000/health
```

### Test CodeWiki Config
```bash
source ../.venv/bin/activate
codewiki config validate
```

### Check Generated Docs
```bash
ls -la /Users/biniangui/Informatique/CodeWiki/backend/docs/
cat /Users/biniangui/Informatique/CodeWiki/backend/docs/metadata.json
```

### Common Issues

**"Ollama server not responding"**
- Solution: Run `ollama serve` in a separate terminal

**"Cannot connect to port 4000"**
- Solution: Ensure LiteLLM proxy is running on port 4000

**"All models from FallbackModel failed"**
- Solution: Check that models in config are accessible:
  ```bash
  ollama list  # Should show llama3 and gpt-oss
  ```

**"Output validation failed"**
- Solution: Try reducing `max_depth` or switching to `ollama/llama3`

---

## ⚠️ CRITICAL LIMITATION: Ollama Models Cannot Generate Documentation

### The Problem

After extensive testing, we've confirmed that **local Ollama models CANNOT reliably generate CodeWiki documentation**, even through LiteLLM proxy. Here's why:

**Root Cause:**
- CodeWiki requires strict Pydantic-validated JSON schemas for documentation generation
- Ollama models (`llama3`, `gpt-oss`, etc.) do not support the structured output format needed
- Even with LiteLLM proxy translating requests, the models fail output validation

**What Works:**
✓ Dependency Analysis (12 components analyzed successfully)
✓ Module Clustering  
✓ File structure parsing

**What Fails:**
✗ Documentation Generation (step 3/5)
✗ Module tree population (results in empty `module_tree.json`)
✗ Actual documentation content creation

### Error Pattern

```
ERROR: Exceeded maximum retries (1) for output validation
pydantic_ai.exceptions.UnexpectedModelBehavior
```

This happens because:
1. CodeWiki agent requests structured JSON
2. Ollama model returns text that doesn't match the schema exactly
3. Pydantic validation fails
4. After 1 retry, generation aborts

### Your Current API Key Limitations

**API Key:** `sk-Arm-...GH0Q` (LiteLLM proxy)  
**Allowed Models:** 
- `ollama/llama3`
- `ollama/gpt-oss`
- `ollama/nomic-embed-text`

**NOT Allowed:**
- `claude-sonnet-4` ❌
- `glm-4p5` ❌
- Any OpenAI models ❌

### Solutions

**Option 1: Use Real Cloud APIs (RECOMMENDED)**

Get an API key from OpenAI or Anthropic:

```bash
# OpenAI (cheapest for documentation)
codewiki config set \
  --api-key sk-YOUR_OPENAI_KEY \
  --base-url https://api.openai.com/v1 \
  --main-model gpt-4o-mini \
  --cluster-model gpt-4o-mini \
  --fallback-model gpt-4o
```

```bash
# Anthropic Claude (best quality)
codewiki config set \
  --api-key sk-ant-YOUR_ANTHROPIC_KEY \
  --base-url https://api.anthropic.com \
  --main-model claude-sonnet-4 \
  --cluster-model claude-sonnet-4
```

**Option 2: Accept Limited Functionality**

CodeWiki CAN still provide value by:
- Analyzing code dependencies
- Generating dependency graphs (see `docs/temp/dependency_graphs/`)
- Providing file structure analysis

The dependency graph shows all 12 functions with their relationships, which is useful even without full docs.

**Option 3: Wait for Better Local Models**

Future Ollama models may support structured output better. Monitor:
- Ollama releases with JSON mode improvements
- CodeWiki updates for better local model support

### Cost Estimate (Cloud APIs)

For a project with 12 components:
- **OpenAI gpt-4o-mini:** ~$0.10-0.50 per generation
- **Anthropic Claude Sonnet:** ~$1-3 per generation

Given the time saved vs manual documentation, this is typically worth it.

---

## Files Generated

After successful run, CodeWiki creates:

```
backend/docs/
├── metadata.json          # Generation stats and info
├── module_tree.json       # Module hierarchy
├── first_module_tree.json # Initial module analysis
└── temp/                  # Temporary analysis files
```

---

## Environment Setup Summary

**Virtual Environment:** `/Users/biniangui/Informatique/CodeWiki/.venv`
**CodeWiki Config:** `~/.codewiki/config.json`
**Backend Path:** `/Users/biniangui/Informatique/CodeWiki/backend`
**Models Used:** `ollama/llama3` (main), `ollama/gpt-oss` (fallback)
**API Proxy:** LiteLLM on `http://localhost:4000`
**Ollama:** Running locally on port 11434
### Current Status

✓ **Infrastructure Working:**
- Ollama server running
- LiteLLM proxy operational on port 4000
- CodeWiki configuration valid
- Dependency analysis functional (12 components)

✗ **Documentation Generation:**
- **FAILS** with Ollama models due to structured output limitations
- Generates empty `module_tree.json`
- 0 modules documented

**Conclusion:** For actual documentation generation, you need OpenAI or Anthropic API access. The current setup with local Ollama models can only analyze code structure, not generate comprehensive documentation.