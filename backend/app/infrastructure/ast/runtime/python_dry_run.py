from __future__ import annotations

import ast
import copy
from typing import Any

from app.domain.entities.analysis import CallFrame, TimelineStep

SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "enumerate": enumerate,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "range": range,
    "reversed": reversed,
    "round": round,
    "sorted": sorted,
    "str": str,
    "sum": sum,
}


class PythonDryRunEngine:
    def __init__(self) -> None:
        self._steps: list[TimelineStep] = []
        self._output: list[str] = []
        self._call_stack: list[CallFrame] = []
        self._step_index = 0

    def run(self, code: str) -> tuple[list[TimelineStep], list[str], list[CallFrame], dict[str, Any]]:
        parsed = ast.parse(code)
        globals_scope: dict[str, Any] = {"__builtins__": SAFE_BUILTINS.copy()}
        locals_scope: dict[str, Any] = {}

        for node in parsed.body:
            self._execute_node(node, globals_scope, locals_scope)

        return self._steps, self._output, copy.deepcopy(self._call_stack), locals_scope

    def _snapshot(
        self,
        node: ast.AST,
        action: str,
        locals_scope: dict[str, Any],
        globals_scope: dict[str, Any],
        output: str | None = None,
    ) -> None:
        self._steps.append(
            TimelineStep(
                index=self._step_index,
                title=node.__class__.__name__,
                line=getattr(node, "lineno", 0),
                action=action,
                locals={k: self._clean(v) for k, v in locals_scope.items()},
                globals={k: self._clean(v) for k, v in globals_scope.items() if k not in {"__builtins__"}},
                output=output,
            )
        )
        self._step_index += 1

    def _clean(self, value: Any) -> Any:
        if callable(value):
            return f"<callable:{getattr(value, '__name__', 'anonymous')}>"
        return value

    def _execute_node(self, node: ast.AST, globals_scope: dict[str, Any], locals_scope: dict[str, Any]) -> None:
        if isinstance(node, ast.Assign):
            value = self._eval(node.value, globals_scope, locals_scope)
            for target in node.targets:
                if isinstance(target, ast.Name):
                    locals_scope[target.id] = value
            self._snapshot(node, "assignment", locals_scope, globals_scope)
            return

        if isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name):
            current = locals_scope.get(node.target.id, 0)
            delta = self._eval(node.value, globals_scope, locals_scope)
            locals_scope[node.target.id] = self._apply_aug(node.op, current, delta)
            self._snapshot(node, "augmented_assignment", locals_scope, globals_scope)
            return

        if isinstance(node, ast.Expr):
            expr_value = self._eval(node.value, globals_scope, locals_scope)
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                if node.value.func.id == "print":
                    rendered = "" if expr_value is None else str(expr_value)
                    self._output.append(rendered)
                    self._snapshot(node, "print", locals_scope, globals_scope, output=rendered)
                    return
            self._snapshot(node, "expression", locals_scope, globals_scope)
            return

        if isinstance(node, ast.If):
            condition = bool(self._eval(node.test, globals_scope, locals_scope))
            self._snapshot(node, f"if_condition={condition}", locals_scope, globals_scope)
            branch = node.body if condition else node.orelse
            for child in branch:
                self._execute_node(child, globals_scope, locals_scope)
            return

        if isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            iterable = self._eval(node.iter, globals_scope, locals_scope)
            limit = 200
            for idx, value in enumerate(iterable):
                if idx >= limit:
                    break
                locals_scope[node.target.id] = value
                self._snapshot(node, f"for_iteration={idx}", locals_scope, globals_scope)
                for child in node.body:
                    self._execute_node(child, globals_scope, locals_scope)
            return

        if isinstance(node, ast.While):
            guard = 0
            while bool(self._eval(node.test, globals_scope, locals_scope)):
                if guard >= 200:
                    break
                self._snapshot(node, f"while_iteration={guard}", locals_scope, globals_scope)
                for child in node.body:
                    self._execute_node(child, globals_scope, locals_scope)
                guard += 1
            return

        if isinstance(node, ast.FunctionDef):
            compiled = compile(ast.Module(body=[node], type_ignores=[]), "<visualizer>", "exec")
            exec(compiled, globals_scope, locals_scope)
            self._snapshot(node, "function_definition", locals_scope, globals_scope)
            return

        if isinstance(node, ast.Return):
            value = self._eval(node.value, globals_scope, locals_scope) if node.value else None
            locals_scope["__return__"] = value
            self._snapshot(node, "return", locals_scope, globals_scope)
            return

        self._snapshot(node, "node_skipped", locals_scope, globals_scope)

    def _eval(self, expr: ast.AST, globals_scope: dict[str, Any], locals_scope: dict[str, Any]) -> Any:
        if isinstance(expr, ast.Constant):
            return expr.value

        if isinstance(expr, ast.Name):
            if expr.id in locals_scope:
                return locals_scope[expr.id]
            if expr.id in globals_scope:
                return globals_scope[expr.id]
            return None

        if isinstance(expr, ast.BinOp):
            left = self._eval(expr.left, globals_scope, locals_scope)
            right = self._eval(expr.right, globals_scope, locals_scope)
            return self._apply_binop(expr.op, left, right)

        if isinstance(expr, ast.UnaryOp):
            operand = self._eval(expr.operand, globals_scope, locals_scope)
            if isinstance(expr.op, ast.USub):
                return -operand
            if isinstance(expr.op, ast.Not):
                return not operand
            return operand

        if isinstance(expr, ast.BoolOp):
            values = [self._eval(v, globals_scope, locals_scope) for v in expr.values]
            if isinstance(expr.op, ast.And):
                return all(values)
            return any(values)

        if isinstance(expr, ast.Compare):
            left = self._eval(expr.left, globals_scope, locals_scope)
            if len(expr.ops) != 1 or len(expr.comparators) != 1:
                return False
            right = self._eval(expr.comparators[0], globals_scope, locals_scope)
            op = expr.ops[0]
            return self._apply_compare(op, left, right)

        if isinstance(expr, ast.Call):
            fn = self._resolve_callable(expr.func, globals_scope, locals_scope)
            args = [self._eval(arg, globals_scope, locals_scope) for arg in expr.args]

            if getattr(expr.func, "id", "") == "print":
                return " ".join(str(item) for item in args)

            frame = CallFrame(
                function=getattr(fn, "__name__", getattr(expr.func, "id", "anonymous")),
                line=getattr(expr, "lineno", 0),
                depth=len(self._call_stack) + 1,
                locals={f"arg_{idx}": value for idx, value in enumerate(args)},
            )
            self._call_stack.append(frame)
            try:
                return fn(*args)
            finally:
                self._call_stack.pop()

        if isinstance(expr, ast.List):
            return [self._eval(el, globals_scope, locals_scope) for el in expr.elts]

        if isinstance(expr, ast.Tuple):
            return tuple(self._eval(el, globals_scope, locals_scope) for el in expr.elts)

        if isinstance(expr, ast.Dict):
            return {
                self._eval(k, globals_scope, locals_scope): self._eval(v, globals_scope, locals_scope)
                for k, v in zip(expr.keys, expr.values)
            }

        if isinstance(expr, ast.Subscript):
            value = self._eval(expr.value, globals_scope, locals_scope)
            index = self._eval(expr.slice, globals_scope, locals_scope)
            try:
                return value[index]
            except Exception:
                return None

        if isinstance(expr, ast.Slice):
            lower = self._eval(expr.lower, globals_scope, locals_scope) if expr.lower else None
            upper = self._eval(expr.upper, globals_scope, locals_scope) if expr.upper else None
            step = self._eval(expr.step, globals_scope, locals_scope) if expr.step else None
            return slice(lower, upper, step)

        try:
            compiled = compile(ast.Expression(expr), "<visualizer>", "eval")
            return eval(compiled, globals_scope, locals_scope)
        except Exception:
            return None

    def _resolve_callable(
        self, fn_expr: ast.AST, globals_scope: dict[str, Any], locals_scope: dict[str, Any]
    ) -> Any:
        if isinstance(fn_expr, ast.Name):
            if fn_expr.id in locals_scope:
                return locals_scope[fn_expr.id]
            if fn_expr.id in globals_scope:
                return globals_scope[fn_expr.id]
        return lambda *args, **kwargs: None

    def _apply_binop(self, op: ast.AST, left: Any, right: Any) -> Any:
        if isinstance(op, ast.Add):
            return left + right
        if isinstance(op, ast.Sub):
            return left - right
        if isinstance(op, ast.Mult):
            return left * right
        if isinstance(op, ast.Div):
            return left / right
        if isinstance(op, ast.Mod):
            return left % right
        if isinstance(op, ast.Pow):
            return left**right
        return None

    def _apply_aug(self, op: ast.AST, current: Any, delta: Any) -> Any:
        if isinstance(op, ast.Add):
            return current + delta
        if isinstance(op, ast.Sub):
            return current - delta
        if isinstance(op, ast.Mult):
            return current * delta
        if isinstance(op, ast.Div):
            return current / delta
        return current

    def _apply_compare(self, op: ast.AST, left: Any, right: Any) -> bool:
        if isinstance(op, ast.Eq):
            return left == right
        if isinstance(op, ast.NotEq):
            return left != right
        if isinstance(op, ast.Lt):
            return left < right
        if isinstance(op, ast.LtE):
            return left <= right
        if isinstance(op, ast.Gt):
            return left > right
        if isinstance(op, ast.GtE):
            return left >= right
        return False
