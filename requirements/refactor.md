# Refactor Task: Clean Up Legacy C# Code

## Prompt

You are a senior C# developer tasked with refactoring three legacy files. The code works but has significant code smells, maintainability issues, and violations of SOLID principles.

For each file, provide:
1. A list of issues you identified (with line references)
2. The fully refactored code
3. Any new files/interfaces/classes you extracted
4. Brief explanation of each change

### Files to Refactor

The following three C# files are provided below. Refactor them to be production-quality code following C# best practices, SOLID principles, and clean code guidelines.

**Goals:**
- Extract interfaces where appropriate
- Replace magic numbers with named constants or configuration
- Use proper enums instead of string comparisons
- Apply single responsibility principle
- Add proper error handling (not generic catches)
- Use modern C# features (pattern matching, records, etc.)
- Fix naming conventions to follow C# standards
- Remove dead code and misleading comments
- Replace string concatenation with proper templating
- Make static utility methods into proper injectable services

**Do NOT:**
- Change the external behavior/API of the classes
- Add unit tests (separate task)
- Add NuGet packages beyond standard .NET 8

---

### File 1: OrderProcessor.cs

```csharp
{{ORDER_PROCESSOR_SOURCE}}
```

### File 2: ReportGenerator.cs

```csharp
{{REPORT_GENERATOR_SOURCE}}
```

### File 3: DataHelper.cs

```csharp
{{DATA_HELPER_SOURCE}}
```

---

## Evaluation Criteria

| Criteria | Weight | Description |
|----------|--------|-------------|
| Issue Identification | 20% | Did the model find the major code smells? |
| SOLID Compliance | 20% | Proper SRP, OCP, DIP application |
| Code Quality | 20% | Clean, idiomatic modern C# |
| Completeness | 15% | All three files fully refactored |
| Interfaces/Abstractions | 15% | Appropriate extraction of interfaces and services |
| Explanation Quality | 10% | Clear reasoning for each change |

**Score each criterion 1-10 and calculate weighted total.**

---

*Note: When running this task, the benchmark script automatically inlines the C# source files from `refactor-source/` in place of the `{{PLACEHOLDER}}` tokens above.*
