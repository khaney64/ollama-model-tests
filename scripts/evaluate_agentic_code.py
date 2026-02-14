#!/usr/bin/env python3
"""
Agentic Task Evaluation Script

This script evaluates each model's generated output for the agentic task against
the criteria specified in requirements/agentic.md. It tests for planning quality,
tool selection, data flow correctness, error handling, and implementation completeness.

Evaluation Criteria (70% automated, 30% manual review):
- Planning Quality (25%): Clear decomposition with logical dependencies
- Tool Selection (20%): Appropriate tools chosen for each operation
- Data Flow (20%): Correct information flow between steps
- Error Handling (15%): Comprehensive try/except blocks and graceful degradation
- Completeness (15%): All requirements met, all 3 portfolios processed
- Code Quality (5%): Well-structured, readable, commented code

Usage:
    python scripts/evaluate_agentic_code.py
"""

import os
import sys
import ast
import subprocess
import re
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class AgenticEvaluator:
    def __init__(self, mode="cpu", ctx_size=None):
        self.base_dir = Path(__file__).parent.parent
        self.models_dir = self.base_dir / "models"
        self.requirements_dir = self.base_dir / "requirements"
        self.mode = mode
        self.ctx_size = ctx_size
        self.results = {}

        # Expected tools for the task
        self.expected_tools = {
            'get_stock_prices',
            'get_portfolio_holdings',
            'calculate_portfolio_value',
            'calculate_volatility_score',
            'check_risk_threshold',
            'generate_report',
            'send_notification',
            'log_operation'
        }

        # Required portfolios
        self.required_portfolios = ['PORT-001', 'PORT-002', 'PORT-003']

        # Risk configuration that should be used
        self.expected_risk_config = {
            'max_volatility': 35.0,
            'min_value': 50000,
            'max_value': 2000000
        }

    def evaluate_model(self, model_name: str) -> Dict[str, Any]:
        """Evaluate a single model's agentic task implementation"""
        print(f"\nEvaluating {model_name}...")

        model_dir = self.models_dir / model_name / "results" / "agentic"

        # Build path based on mode
        if self.mode == "gpu" and self.ctx_size:
            output_file = model_dir / "gpu" / f"ctx-{self.ctx_size}" / "output.md"
        else:
            output_file = model_dir / self.mode / "output.md"

        if not output_file.exists():
            return {
                'model': model_name,
                'status': 'No output.md found',
                'scores': {'total': 0}
            }

        result = {
            'model': model_name,
            'status': 'evaluated',
            'scores': {},
            'issues': [],
            'automated_checks': {},
            'manual_review_notes': []
        }

        # Parse the output file
        sections = self._parse_output_sections(output_file, result)

        if not sections:
            result['status'] = 'Failed to parse output sections'
            result['scores']['total'] = 0
            return result

        # AUTOMATED CHECKS (70% of score)

        # 1. Output Format (10%) - All 3 sections present
        result['scores']['output_format'] = self._evaluate_output_format(sections, result)

        # 2. Tool Coverage (10%) - At least 6 tools used
        result['scores']['tool_coverage'] = self._evaluate_tool_coverage(sections, result)

        # 3. Execution Success (15%) - Code runs without errors
        result['scores']['execution'] = self._evaluate_execution(sections, result)

        # 4. Data Flow (15%) - Outputs passed as inputs correctly
        result['scores']['data_flow'] = self._evaluate_data_flow(sections, result)

        # 5. Error Handling (10%) - Try/except blocks present
        result['scores']['error_handling'] = self._evaluate_error_handling(sections, result)

        # 6. Logging Completeness (10%) - At least 5 log_operation calls
        result['scores']['logging'] = self._evaluate_logging(sections, result)

        # MANUAL REVIEW GUIDELINES (30% of score)
        # These generate notes for human reviewers

        # 7. Planning Logic Quality (10%)
        result['manual_review_notes'].append(self._generate_planning_review_notes(sections))

        # 8. Tool Orchestration Strategy (10%)
        result['manual_review_notes'].append(self._generate_orchestration_review_notes(sections))

        # 9. Design Justification (10%)
        result['manual_review_notes'].append(self._generate_justification_review_notes(sections))

        # Calculate automated score (70%)
        automated_weights = {
            'output_format': 0.10,
            'tool_coverage': 0.10,
            'execution': 0.15,
            'data_flow': 0.15,
            'error_handling': 0.10,
            'logging': 0.10
        }

        automated_score = sum(result['scores'][criterion] * weight
                             for criterion, weight in automated_weights.items()
                             if criterion in result['scores'])

        # Manual review score placeholder (30%)
        # Reviewers will fill this in based on the notes
        manual_score_placeholder = 3.0  # Default to 50% of 30% (medium quality)

        total_score = automated_score + manual_score_placeholder

        result['scores']['automated'] = round(automated_score, 2)
        result['scores']['manual_placeholder'] = manual_score_placeholder
        result['scores']['total'] = round(total_score, 2)
        result['scores']['letter_grade'] = self._get_letter_grade(total_score)

        return result

    def _parse_output_sections(self, output_file: Path, result: Dict) -> Dict[str, str]:
        """Parse output.md into sections: plan, implementation, justification.

        Handles varied model output formats:
        - Any header level (# through ####)
        - Optional 'Section N:' prefix before keyword
        - Optional parenthetical suffix like '(Python)' or '(Markdown)'
        - Code blocks that appear before section headers (code-first outputs)
        """
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()

            sections = {}

            # Build a list of code fence ranges so we can ignore # lines inside them
            fence_ranges = []
            for m in re.finditer(r'```[^\n]*\n.*?```', content, re.DOTALL):
                fence_ranges.append((m.start(), m.end()))

            def is_in_fence(pos):
                return any(s <= pos < e for s, e in fence_ranges)

            # Find positions of all real markdown headers (not inside code fences)
            real_header_positions = []
            for m in re.finditer(r'^\s*#{1,4}\s+', content, re.MULTILINE):
                if not is_in_fence(m.start()):
                    real_header_positions.append(m.start())

            # Flexible header pattern:
            # - Any header level: #{1,4}
            # - Optional "Section N:" prefix (non-capturing)
            # - Keyword match
            hdr = r'^\s*#{1,4}\s+(?:Section\s*\d+[:\s]*)?\s*'

            def best_match(keywords):
                """Find the header matching keywords with the most content."""
                pattern = hdr + r'(' + keywords + r')\b[^\n]*'
                best_content = None
                best_len = -1
                for m in re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE):
                    if is_in_fence(m.start()):
                        continue
                    # Find next real header after this one
                    section_end = len(content)
                    for h_pos in real_header_positions:
                        if h_pos > m.end():
                            section_end = h_pos
                            break
                    section_text = content[m.end():section_end].strip()
                    if len(section_text) > best_len:
                        best_content = section_text
                        best_len = len(section_text)
                return best_content

            plan_text = best_match(r'Execution Plan|Plan|Step-by-Step Plan')
            impl_text = best_match(r'Implementation|Code|Python Implementation')
            just_text = best_match(r'Design Justification|Justification|Reasoning')

            if plan_text:
                sections['plan'] = plan_text

            if impl_text:
                sections['implementation'] = impl_text
                # Extract code from markdown code blocks within implementation section
                code_match = re.search(r'```(?:python)?\n(.*?)```', impl_text, re.DOTALL)
                if code_match:
                    sections['code'] = code_match.group(1).strip()
                elif '```' not in impl_text:
                    # No code fences at all - text itself might be raw code
                    if re.search(r'^\s*(?:def |import |from |class )', impl_text, re.MULTILINE):
                        sections['code'] = impl_text

            if just_text:
                sections['justification'] = just_text

            # Fallback: if no code found in implementation section, search entire document
            # for code blocks (handles code-first outputs like gemma3, llama3.1)
            if 'code' not in sections:
                all_code_blocks = re.findall(r'```(?:python)?\n(.*?)```', content, re.DOTALL)
                if all_code_blocks:
                    # Use the largest code block as the implementation
                    largest_block = max(all_code_blocks, key=len).strip()
                    if len(largest_block) > 50:  # Skip tiny snippets
                        sections['code'] = largest_block
                        if 'implementation' not in sections:
                            sections['implementation'] = largest_block

            return sections

        except Exception as e:
            result['issues'].append(f"Failed to parse output file: {e}")
            return {}

    def _evaluate_output_format(self, sections: Dict, result: Dict) -> float:
        """Evaluate presence of all 3 required sections (10%)"""
        score = 10.0

        if 'plan' not in sections or len(sections['plan']) < 100:
            score -= 3.5
            result['issues'].append("Missing or incomplete Execution Plan section")

        if 'implementation' not in sections or len(sections['implementation']) < 200:
            score -= 3.5
            result['issues'].append("Missing or incomplete Implementation section")

        if 'justification' not in sections or len(sections['justification']) < 100:
            score -= 3.0
            result['issues'].append("Missing or incomplete Design Justification section")

        result['automated_checks']['output_format'] = {
            'has_plan': 'plan' in sections,
            'has_implementation': 'implementation' in sections,
            'has_justification': 'justification' in sections
        }

        return max(0.0, score)

    def _evaluate_tool_coverage(self, sections: Dict, result: Dict) -> float:
        """Evaluate tool usage (10%) - at least 6 tools should be used"""
        if 'code' not in sections:
            result['issues'].append("No code found for tool coverage analysis")
            return 0.0

        code = sections['code']
        tools_used = set()

        for tool in self.expected_tools:
            if tool in code:
                tools_used.add(tool)

        score = 10.0
        num_tools = len(tools_used)

        if num_tools < 6:
            score = num_tools * (10.0 / 6.0)  # Linear scale up to 6 tools
            result['issues'].append(f"Only {num_tools} tools used (expected at least 6)")

        result['automated_checks']['tool_coverage'] = {
            'tools_used': sorted(list(tools_used)),
            'count': num_tools,
            'missing': sorted(list(self.expected_tools - tools_used))
        }

        return round(score, 2)

    def _evaluate_execution(self, sections: Dict, result: Dict) -> float:
        """Test if code executes without errors (15%)"""
        if 'code' not in sections:
            result['issues'].append("No code to execute")
            return 0.0

        try:
            # Create a temporary directory for execution
            with tempfile.TemporaryDirectory() as tmpdir:
                tmpdir_path = Path(tmpdir)

                # Write the code to a file
                test_file = tmpdir_path / "test_agent.py"

                # Add imports from tools_reference at the top
                full_code = f"""import sys
sys.path.insert(0, r'{self.requirements_dir}')

from tools_reference import (
    get_stock_prices,
    get_portfolio_holdings,
    calculate_portfolio_value,
    calculate_volatility_score,
    check_risk_threshold,
    generate_report,
    send_notification,
    log_operation
)

{sections['code']}
"""

                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write(full_code)

                # Try to execute the code
                exec_result = subprocess.run(
                    [sys.executable, str(test_file)],
                    cwd=tmpdir_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if exec_result.returncode != 0:
                    stderr = exec_result.stderr.strip()
                    if stderr:
                        error_lines = stderr.split('\n')
                        error_msg = error_lines[-1].strip() if error_lines else "Unknown error"
                        result['issues'].append(f"Code execution failed: {error_msg}")
                    else:
                        result['issues'].append("Code execution failed with no error output")

                    result['automated_checks']['execution'] = {
                        'success': False,
                        'error': error_msg if stderr else 'Unknown'
                    }
                    return 0.0

                result['automated_checks']['execution'] = {
                    'success': True,
                    'stdout_length': len(exec_result.stdout)
                }

                return 10.0

        except subprocess.TimeoutExpired:
            result['issues'].append("Code execution timed out (>30s)")
            result['automated_checks']['execution'] = {'success': False, 'error': 'Timeout'}
            return 0.0
        except Exception as e:
            result['issues'].append(f"Execution test failed: {e}")
            result['automated_checks']['execution'] = {'success': False, 'error': str(e)}
            return 0.0

    def _evaluate_data_flow(self, sections: Dict, result: Dict) -> float:
        """Evaluate data flow correctness (15%)"""
        if 'code' not in sections:
            return 0.0

        code = sections['code']
        score = 10.0
        issues = []

        # Check that holdings data is retrieved and used for price fetching
        if 'get_portfolio_holdings' in code and 'get_stock_prices' in code:
            # Look for pattern of extracting symbols from holdings
            if not re.search(r'symbol|holdings.*\[.*symbol', code, re.IGNORECASE):
                score -= 2.0
                issues.append("May not be extracting symbols from holdings for price fetching")

        # Check that prices are passed to calculate_portfolio_value
        if 'calculate_portfolio_value' in code:
            # Should have both holdings and prices as arguments
            if not re.search(r'calculate_portfolio_value\s*\([^)]*holdings[^)]*price|calculate_portfolio_value\s*\([^)]*price[^)]*holdings', code, re.IGNORECASE):
                score -= 2.0
                issues.append("May not be passing both holdings and prices to calculate_portfolio_value")

        # Check that symbols are passed to calculate_volatility_score
        if 'calculate_volatility_score' in code:
            if not re.search(r'calculate_volatility_score\s*\([^)]*symbol', code, re.IGNORECASE):
                score -= 2.0
                issues.append("May not be passing symbols to calculate_volatility_score")

        # Check that risk check receives value and volatility
        if 'check_risk_threshold' in code:
            if not re.search(r'check_risk_threshold\s*\([^)]*value[^)]*volatil|check_risk_threshold\s*\([^)]*volatil[^)]*value', code, re.IGNORECASE):
                score -= 2.0
                issues.append("May not be passing both value and volatility to check_risk_threshold")

        # Check that report data is comprehensive
        if 'generate_report' in code:
            # Should construct a data dict with multiple fields
            if not re.search(r'\{[^}]*(portfolio_id|client_name)[^}]*(total_value|volatility)', code, re.IGNORECASE):
                score -= 2.0
                issues.append("May not be constructing comprehensive portfolio_data for report")

        # Check that report is passed to notification
        if 'send_notification' in code and 'generate_report' in code:
            # Report should be stored and used
            if not re.search(r'report\s*=.*generate_report|.*=.*generate_report.*send_notification', code, re.IGNORECASE):
                score -= 1.0
                issues.append("May not be passing report to notification")

        if issues:
            result['issues'].extend(issues)

        result['automated_checks']['data_flow'] = {
            'score': score,
            'issues_found': len(issues)
        }

        return max(0.0, score)

    def _evaluate_error_handling(self, sections: Dict, result: Dict) -> float:
        """Evaluate error handling presence (10%)"""
        if 'code' not in sections:
            return 0.0

        code = sections['code']
        score = 10.0

        # Count try/except blocks
        try_count = code.count('try:')
        except_count = code.count('except')

        if try_count == 0 or except_count == 0:
            score = 0.0
            result['issues'].append("No error handling (try/except) found")
        elif try_count < 2:
            score = 5.0
            result['issues'].append("Minimal error handling - should wrap each portfolio processing")

        # Check for continue or pass in except blocks (graceful degradation)
        has_graceful_handling = 'continue' in code or ('except' in code and 'pass' in code)

        if not has_graceful_handling and try_count > 0:
            score -= 2.0
            result['issues'].append("Error handling present but may not continue processing on failure")

        result['automated_checks']['error_handling'] = {
            'try_blocks': try_count,
            'except_blocks': except_count,
            'has_graceful_degradation': has_graceful_handling
        }

        return max(0.0, score)

    def _evaluate_logging(self, sections: Dict, result: Dict) -> float:
        """Evaluate logging completeness (10%) - at least 5 log_operation calls"""
        if 'code' not in sections:
            return 0.0

        code = sections['code']

        # Count log_operation calls
        log_count = code.count('log_operation')

        score = min(10.0, log_count * 2.0)  # 2 points per log, up to 5 logs

        if log_count < 5:
            result['issues'].append(f"Only {log_count} log_operation calls (expected at least 5)")

        result['automated_checks']['logging'] = {
            'log_operation_calls': log_count
        }

        return score

    def _generate_planning_review_notes(self, sections: Dict) -> str:
        """Generate notes for manual review of planning quality (10%)"""
        if 'plan' not in sections:
            return "**Planning Quality (10%):** REVIEW REQUIRED - No plan section found"

        plan = sections['plan']

        notes = ["**Planning Quality (10%):** MANUAL REVIEW REQUIRED"]
        notes.append("  Evaluate:")
        notes.append("  - Are steps clearly numbered and described?")
        notes.append("  - Are data dependencies identified?")
        notes.append("  - Is the sequence logical and efficient?")
        notes.append("  - Is error handling strategy mentioned?")

        # Auto-detect some basic qualities
        has_numbered_steps = bool(re.search(r'^\s*\d+\.', plan, re.MULTILINE))
        has_tools_mentioned = any(tool in plan for tool in self.expected_tools)

        if has_numbered_steps:
            notes.append("  ✓ Plan has numbered steps")
        else:
            notes.append("  ✗ Plan lacks clear numbered steps")

        if has_tools_mentioned:
            notes.append("  ✓ Tools are mentioned in plan")
        else:
            notes.append("  ✗ Tools not clearly mentioned in plan")

        return "\n".join(notes)

    def _generate_orchestration_review_notes(self, sections: Dict) -> str:
        """Generate notes for manual review of tool orchestration (10%)"""
        notes = ["**Tool Orchestration Strategy (10%):** MANUAL REVIEW REQUIRED"]
        notes.append("  Evaluate:")
        notes.append("  - Are tools orchestrated in the right sequence?")
        notes.append("  - Is there any redundant tool usage?")
        notes.append("  - Are all necessary tools used?")
        notes.append("  - Is the orchestration efficient?")

        if 'code' in sections:
            code = sections['code']

            # Check for loop over portfolios
            has_portfolio_loop = bool(re.search(r'for.*PORT-|for.*portfolio', code, re.IGNORECASE))

            # Check for modular function structure
            has_functions = bool(re.search(r'^def\s+\w+', code, re.MULTILINE))

            if has_portfolio_loop:
                notes.append("  ✓ Code loops over portfolios")
            else:
                notes.append("  ✗ May not be processing multiple portfolios")

            if has_functions:
                notes.append("  ✓ Code uses functions (modular structure)")
            else:
                notes.append("  ✗ Code lacks function structure")

        return "\n".join(notes)

    def _generate_justification_review_notes(self, sections: Dict) -> str:
        """Generate notes for manual review of design justification (10%)"""
        if 'justification' not in sections:
            return "**Design Justification (10%):** REVIEW REQUIRED - No justification section found"

        justification = sections['justification']

        notes = ["**Design Justification (10%):** MANUAL REVIEW REQUIRED"]
        notes.append("  Evaluate:")
        notes.append("  - Are design decisions explained?")
        notes.append("  - Is the orchestration sequence justified?")
        notes.append("  - Are trade-offs discussed?")
        notes.append("  - Is the reasoning sound?")

        # Check for key topics
        has_orchestration_discussion = bool(re.search(r'orchestrat|sequence|order|flow', justification, re.IGNORECASE))
        has_error_discussion = bool(re.search(r'error|exception|fail|graceful', justification, re.IGNORECASE))
        has_data_flow_discussion = bool(re.search(r'data|pass|flow|input|output', justification, re.IGNORECASE))

        if has_orchestration_discussion:
            notes.append("  ✓ Discusses orchestration/sequencing")
        if has_error_discussion:
            notes.append("  ✓ Discusses error handling strategy")
        if has_data_flow_discussion:
            notes.append("  ✓ Discusses data flow")

        if not (has_orchestration_discussion or has_error_discussion or has_data_flow_discussion):
            notes.append("  ✗ Justification lacks discussion of key design aspects")

        return "\n".join(notes)

    def _get_letter_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 9.0:
            return 'A'
        elif score >= 8.0:
            return 'B'
        elif score >= 7.0:
            return 'C'
        elif score >= 6.0:
            return 'D'
        else:
            return 'F'

    def evaluate_all_models(self):
        """Evaluate all models and generate report"""
        print("Starting evaluation of all agentic task implementations...")

        # Find all models with output.md in agentic results for the specified mode
        # Each entry is (model_dir_name, ctx_size_or_None)
        model_entries = []
        for model_dir in self.models_dir.iterdir():
            if model_dir.is_dir():
                if self.mode == "gpu" and self.ctx_size:
                    output_file = model_dir / "results" / "agentic" / "gpu" / f"ctx-{self.ctx_size}" / "output.md"
                    if output_file.exists():
                        model_entries.append((model_dir.name, self.ctx_size))
                elif self.mode == "gpu" and not self.ctx_size:
                    # Scan all ctx-* subdirectories
                    gpu_dir = model_dir / "results" / "agentic" / "gpu"
                    if gpu_dir.is_dir():
                        for ctx_dir in sorted(gpu_dir.iterdir()):
                            if ctx_dir.is_dir() and ctx_dir.name.startswith("ctx-"):
                                output_file = ctx_dir / "output.md"
                                if output_file.exists():
                                    ctx = ctx_dir.name.replace("ctx-", "")
                                    model_entries.append((model_dir.name, ctx))
                else:
                    output_file = model_dir / "results" / "agentic" / self.mode / "output.md"
                    if output_file.exists():
                        model_entries.append((model_dir.name, None))

        print(f"Found {len(model_entries)} models to evaluate:")
        for model_name, ctx in model_entries:
            label = f"{model_name} (ctx-{ctx})" if ctx else model_name
            print(f"  - {label}")

        # Evaluate each model
        all_results = []
        for model_name, ctx in model_entries:
            saved_ctx = self.ctx_size
            self.ctx_size = ctx
            result = self.evaluate_model(model_name)
            # Include ctx size in model name for GPU reports without specific ctx
            if ctx and not saved_ctx:
                result['model'] = f"{model_name} (ctx-{ctx})"
            all_results.append(result)
            self.results[result['model']] = result
            self.ctx_size = saved_ctx

        # Generate report
        report_path = self._generate_report(all_results)

        print(f"\nEvaluation complete! Results saved to {report_path}")

    def _generate_report(self, results: List[Dict]) -> Path:
        """Generate the evaluation report"""
        report_path = self.base_dir / "reports" / self.mode / "report_card_agentic.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        # Sort results by total score
        results.sort(key=lambda x: x['scores'].get('total', 0), reverse=True)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Agentic Task Implementation Report Card\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Executive Summary
            grade_dist = {}
            for result in results:
                grade = result['scores'].get('letter_grade', 'N/A')
                grade_dist[grade] = grade_dist.get(grade, 0) + 1

            f.write("## Executive Summary\n\n")
            f.write(f"Evaluated **{len(results)}** agentic task implementations against the requirements in `requirements/agentic.md`.\n\n")
            f.write("**Grade Distribution:**\n")
            for grade in ['A', 'B', 'C', 'D', 'F', 'N/A']:
                if grade in grade_dist:
                    f.write(f"- {grade}: {grade_dist[grade]} model(s)\n")
            f.write("\n")

            f.write("**Scoring Breakdown:**\n")
            f.write("- **Automated Checks (70%)**: Output format, tool coverage, execution, data flow, error handling, logging\n")
            f.write("- **Manual Review (30%)**: Planning quality, tool orchestration strategy, design justification\n")
            f.write("\n")

            # Summary Rankings
            f.write("## Summary Rankings\n\n")
            f.write("| Rank | Model | Grade | Total | Automated (70%) | Manual* (30%) | Pass |\n")
            f.write("|------|-------|-------|-------|-----------------|---------------|------|\n")

            for i, result in enumerate(results, 1):
                scores = result['scores']
                passed = "✓" if scores.get('total', 0) >= 7.0 else "✗"
                f.write(f"| {i} | {result['model']} | {scores.get('letter_grade', 'N/A')} | "
                       f"{scores.get('total', 0):.1f} | {scores.get('automated', 0):.1f} | "
                       f"{scores.get('manual_placeholder', 0):.1f} | {passed} |\n")

            f.write("\n*Manual review scores are placeholder (50% of 30%). Reviewers should adjust based on notes below.*\n\n")

            # Detailed Automated Scores
            f.write("## Automated Evaluation Scores\n\n")
            f.write("| Model | Format | Tools | Execution | Data Flow | Error Handle | Logging |\n")
            f.write("|-------|--------|-------|-----------|-----------|--------------|----------|\n")

            for result in results:
                scores = result['scores']
                f.write(f"| {result['model']} | {scores.get('output_format', 0):.1f} | "
                       f"{scores.get('tool_coverage', 0):.1f} | {scores.get('execution', 0):.1f} | "
                       f"{scores.get('data_flow', 0):.1f} | {scores.get('error_handling', 0):.1f} | "
                       f"{scores.get('logging', 0):.1f} |\n")

            f.write("\n")

            # Detailed Results
            f.write("## Detailed Evaluation Results\n\n")

            for result in results:
                f.write(f"### {result['model']}\n\n")
                f.write(f"**Overall Grade: {result['scores'].get('letter_grade', 'N/A')} "
                       f"({result['scores'].get('total', 0):.1f}/10.0)**\n\n")

                if result['status'] != 'evaluated':
                    f.write(f"**Status:** {result['status']}\n\n")
                    continue

                # Automated Scores
                f.write("#### Automated Scores (70%)\n\n")
                scores = result['scores']
                f.write(f"- **Output Format (10%):** {scores.get('output_format', 0):.1f}/10.0\n")
                f.write(f"- **Tool Coverage (10%):** {scores.get('tool_coverage', 0):.1f}/10.0\n")
                f.write(f"- **Execution Success (15%):** {scores.get('execution', 0):.1f}/10.0\n")
                f.write(f"- **Data Flow Correctness (15%):** {scores.get('data_flow', 0):.1f}/10.0\n")
                f.write(f"- **Error Handling (10%):** {scores.get('error_handling', 0):.1f}/10.0\n")
                f.write(f"- **Logging Completeness (10%):** {scores.get('logging', 0):.1f}/10.0\n\n")
                f.write(f"**Automated Subtotal:** {scores.get('automated', 0):.1f}/7.0\n\n")

                # Automated Checks Details
                if 'automated_checks' in result and result['automated_checks']:
                    f.write("#### Automated Check Details\n\n")
                    checks = result['automated_checks']

                    if 'tool_coverage' in checks:
                        tc = checks['tool_coverage']
                        f.write(f"**Tools Used ({tc['count']}/8):** {', '.join(tc['tools_used'])}\n\n")
                        if tc['missing']:
                            f.write(f"**Missing Tools:** {', '.join(tc['missing'])}\n\n")

                    if 'execution' in checks:
                        ex = checks['execution']
                        f.write(f"**Execution:** {'✓ Success' if ex['success'] else '✗ Failed'}\n\n")

                    if 'error_handling' in checks:
                        eh = checks['error_handling']
                        f.write(f"**Error Handling:** {eh['try_blocks']} try blocks, "
                               f"{eh['except_blocks']} except blocks\n\n")

                    if 'logging' in checks:
                        lg = checks['logging']
                        f.write(f"**Logging:** {lg['log_operation_calls']} log_operation calls\n\n")

                # Issues
                if result['issues']:
                    f.write("#### Issues Found\n\n")
                    for issue in result['issues']:
                        f.write(f"- {issue}\n")
                    f.write("\n")

                # Manual Review Notes
                if result['manual_review_notes']:
                    f.write("#### Manual Review Guidelines (30%)\n\n")
                    for note_section in result['manual_review_notes']:
                        f.write(f"{note_section}\n\n")

            # Evaluation Criteria
            f.write("---\n\n")
            f.write("## Evaluation Criteria\n\n")

            f.write("### Automated Checks (70%)\n\n")

            f.write("#### Output Format (10%)\n")
            f.write("- Execution Plan section present and substantial\n")
            f.write("- Implementation section with Python code present\n")
            f.write("- Design Justification section present and substantial\n\n")

            f.write("#### Tool Coverage (10%)\n")
            f.write("- At least 6 of 8 tools used appropriately\n")
            f.write("- Tools are called (not just imported)\n\n")

            f.write("#### Execution Success (15%)\n")
            f.write("- Code executes without errors against mock tools\n")
            f.write("- Code completes within 30 seconds\n")
            f.write("- No syntax errors or runtime exceptions\n\n")

            f.write("#### Data Flow Correctness (15%)\n")
            f.write("- Holdings data used to extract symbols for price fetching\n")
            f.write("- Holdings and prices passed to calculate_portfolio_value\n")
            f.write("- Symbols passed to calculate_volatility_score\n")
            f.write("- Value and volatility passed to check_risk_threshold\n")
            f.write("- Comprehensive portfolio_data constructed for report\n")
            f.write("- Report passed to notification\n\n")

            f.write("#### Error Handling (10%)\n")
            f.write("- Try/except blocks present\n")
            f.write("- At least 2 try blocks (one per portfolio processing)\n")
            f.write("- Graceful degradation (continue/pass on error)\n\n")

            f.write("#### Logging Completeness (10%)\n")
            f.write("- At least 5 log_operation calls\n")
            f.write("- Logs cover major operations (analysis start/end, risk checks, notifications)\n\n")

            f.write("### Manual Review (30%)\n\n")

            f.write("#### Planning Quality (10%)\n")
            f.write("- Clear decomposition of goal into logical steps\n")
            f.write("- Numbered steps with descriptions\n")
            f.write("- Data dependencies identified\n")
            f.write("- Sequence is logical and efficient\n")
            f.write("- Error handling strategy mentioned\n\n")

            f.write("#### Tool Orchestration Strategy (10%)\n")
            f.write("- Tools orchestrated in correct sequence\n")
            f.write("- No redundant tool usage\n")
            f.write("- All necessary tools used\n")
            f.write("- Orchestration is efficient\n")
            f.write("- Code processes all 3 portfolios\n\n")

            f.write("#### Design Justification (10%)\n")
            f.write("- Design decisions are explained\n")
            f.write("- Orchestration sequence is justified\n")
            f.write("- Trade-offs are discussed\n")
            f.write("- Reasoning is sound and demonstrates understanding\n")
            f.write("- Addresses data flow, error handling, and efficiency\n\n")

            f.write("---\n\n")
            f.write("**Passing Score:** 7.0/10.0\n\n")
            f.write("*Report generated by evaluate_agentic_code.py*\n")

        return report_path

    def _get_timestamp(self) -> str:
        """Get current timestamp for report"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Evaluate agentic task implementations')
    parser.add_argument('--mode', type=str, required=True, choices=["cloud", "cpu", "gpu"],
                       help="Execution mode")
    parser.add_argument('--ctx-size', type=int, default=None,
                       help="Context size for GPU mode (e.g., 8192)")

    args = parser.parse_args()

    evaluator = AgenticEvaluator(mode=args.mode, ctx_size=args.ctx_size)
    evaluator.evaluate_all_models()
