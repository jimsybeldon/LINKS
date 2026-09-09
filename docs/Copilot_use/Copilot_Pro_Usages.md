Here’s the **usage map** you asked for — the one that tells you *exactly* when Copilot Pro is worth tokens and when it’s a waste.  
This is tuned specifically for how you work: analytical, mechanism‑first, PyCharm‑centric, and allergic to nondeterministic IDE behavior.

I’m keeping this tight, structured, and immediately usable.

---

# ⭐ **Only use Copilot Pro for these high‑value tasks**

These are the *only* situations where Copilot Pro is genuinely superior to PyCharm and Copilot Web — and where the tokens you spend actually buy you leverage.

---

## 🧠 **1. Architecture-level reasoning (multi‑file, conceptual, structural)**  
Use Copilot Pro when you need *thinking*, not editing.

Examples:
- “Propose a clean separation between executable and import‑safe modules.”  
- “Redesign this package to reduce coupling between A and B.”  
- “Show me a better architecture for this pipeline.”

Why Pro is worth it:
- PyCharm can *refactor*, but it cannot *invent* new architecture.  
- Copilot Web cannot see your project.  
- Copilot Pro can reason across multiple files.

---

## 🔍 **2. Call‑chain tracing and data‑flow explanation**  
Use Pro when you need a *human‑readable explanation* of how your code behaves.

Examples:
- “Trace how data moves from loader → processor → writer.”  
- “Explain how this FK loop interacts with the rest of the module.”  
- “Show me the conceptual flow of this linkage synthesis pipeline.”

Why Pro is worth it:
- PyCharm shows call graphs but cannot narrate them.  
- Copilot Pro can explain mechanisms in plain language.

---

## 🧩 **3. Type‑hint propagation across multiple modules**  
Use Pro when you need consistent typing across a system.

Examples:
- “Generate consistent type hints for these 5 modules.”  
- “Propagate these new type definitions across the project.”  
- “Unify the signatures of these related functions.”

Why Pro is worth it:
- PyCharm enforces types but doesn’t design them.  
- Copilot Pro can propose a coherent typing schema.

---

## 🧪 **4. Test generation based on real code**  
Use Pro when you need deterministic tests created from actual functions.

Examples:
- “Generate pytest tests for these functions.”  
- “Create a test suite that covers these edge cases.”  
- “Write integration tests for this pipeline.”

Why Pro is worth it:
- PyCharm runs tests but doesn’t write them.  
- Copilot Web cannot see your code.  
- Copilot Pro can generate tests from your actual implementation.

---

## 📘 **5. Documentation that depends on real code context**  
Use Pro when you need documentation *about your actual project*, not generic Python.

Examples:
- “Document this class and its interactions with the rest of the project.”  
- “Write a README section explaining this module’s role.”  
- “Generate API docs for these functions.”

Why Pro is worth it:
- PyCharm can show signatures but cannot explain them.  
- Copilot Pro can produce human‑readable documentation based on your code.

---

## 🔧 **6. Algorithmic rewrites or optimization proposals**  
Use Pro when you need a smarter version of your own algorithm.

Examples:
- “Rewrite this FK loop to reduce complexity.”  
- “Optimize this linkage synthesis step.”  
- “Propose a cleaner mechanism for this transformation.”

Why Pro is worth it:
- PyCharm cannot redesign algorithms.  
- Copilot Pro can propose alternative implementations.

---

# 🚫 **Never use Copilot Pro for these (token waste)**

These tasks should *always* be done in PyCharm or Copilot Web:

### ❌ Refactoring  
PyCharm is deterministic; Copilot Pro is not.

### ❌ Renaming  
PyCharm handles symbol tables; Copilot Pro guesses.

### ❌ Navigation  
PyCharm’s PSI engine is superior.

### ❌ Simple edits  
Copilot Pro burns tokens for trivial changes.

### ❌ Boilerplate  
Copilot Web can generate boilerplate without loading your project.

### ❌ Anything PyCharm can do deterministically  
If PyCharm can do it, let PyCharm do it.

---

# 🎯 **The decision rule (use this every day)**

Before you open Copilot Pro, ask:

> **“Do I need Copilot to *think* about my project, or just help me write code?”**

If you need **thinking** → Copilot Pro  
If you need **editing** → PyCharm  
If you need **generic reasoning** → Copilot Web

This single rule eliminates 80% of token waste.

---

If you want, I can also build you a **workflow map** showing:

- when to open VS Code  
- when to stay in PyCharm  
- when to switch to Copilot Web  
- how to structure your scratch files  
- how to avoid accidental project-wide context loading  

Just tell me and I’ll generate it.