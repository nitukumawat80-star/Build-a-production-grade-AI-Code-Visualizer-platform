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
        self._call_history: list[CallFrame] = []
        self._function_defs: dict[str, ast.FunctionDef] = {}
        self._memory_state: dict[str, Any] = {}
        self._step_index = 0

    def run(self, code: str) -> tuple[list[TimelineStep], list[str], list[CallFrame], dict[str, Any]]:
        parsed = ast.parse(code)
        globals_scope: dict[str, Any] = {"__builtins__": SAFE_BUILTINS.copy()}
        locals_scope: dict[str, Any] = {}

        self._steps = []
        self._output = []
        self._call_stack = []
        self._call_history = []
        self._function_defs = {}
        self._memory_state = {}
        self._step_index = 0

        for node in parsed.body:
            returned, value = self._execute_node(node, globals_scope, locals_scope)
            if returned:
                locals_scope["__return__"] = value
                break

        return self._steps, self._output, copy.deepcopy(self._call_history), self._memory_state

    def _snapshot(
        self,
        node: ast.AST,
        action: str,
        locals_scope: dict[str, Any],
        globals_scope: dict[str, Any],
        output: str | None = None,
        title: str | None = None,
    ) -> None:
        self._steps.append(
            TimelineStep(
                index=self._step_index,
                title=title or node.__class__.__name__,
                line=getattr(node, "lineno", 0),
                action=action,
                locals={k: self._clean(v) for k, v in locals_scope.items()},
                globals={k: self._clean(v) for k, v in globals_scope.items() if k != "__builtins__"},
                stack_depth=len(self._call_stack),
                output=output,
            )
        )
        self._memory_state.update({k: self._clean(v) for k, v in locals_scope.items()})
        self._memory_state.update({k: self._clean(v) for k, v in globals_scope.items() if k != "__builtins__"})
        self._step_index += 1

    def _clean(self, value: Any) -> Any:
        if callable(value):
            return f"<callable:{getattr(value, '__name__', 'anonymous')}>"
        return value

    def _execute_block(
        self,
        body: list[ast.stmt],
        globals_scope: dict[str, Any],
        locals_scope: dict[str, Any],
    ) -> tuple[bool, Any]:
        for node in body:
            returned, value = self._execute_node(node, globals_scope, locals_scope)
            if returned:
                return True, value
        return False, None

    def _execute_node(
        self,
        node: ast.AST,
        globals_scope: dict[str, Any],
        locals_scope: dict[str, Any],
    ) -> tuple[bool, Any]:
        if isinstance(node, ast.Assign):
            value = self._eval(node.value, globals_scope, locals_scope)
            for target in node.targets:
                self._assign_target(target, value, globals_scope, locals_scope)
            self._snapshot(node, "assignment", locals_scope, globals_scope)
            return False, None

        if isinstance(node, ast.AugAssign):
            current = self._eval(node.target, globals_scope, locals_scope)
            delta = self._eval(node.value, globals_scope, locals_scope)
            result = self._apply_aug(node.op, current, delta)
            self._assign_target(node.target, result, globals_scope, locals_scope)
            self._snapshot(node, "augmented_assignment", locals_scope, globals_scope)
            return False, None

        if isinstance(node, ast.Expr):
            expr_value = self._eval(node.value, globals_scope, locals_scope)
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                if node.value.func.id == "print":
                    rendered = "" if expr_value is None else str(expr_value)
                    self._output.append(rendered)
                    self._snapshot(node, "print", locals_scope, globals_scope, output=rendered)
                    return False, None
            self._snapshot(node, "expression", locals_scope, globals_scope)
            return False, None

        if isinstance(node, ast.If):
            condition = bool(self._eval(node.test, globals_scope, locals_scope))
            self._snapshot(node, f"if_condition={condition}", locals_scope, globals_scope)
            branch = node.body if condition else node.orelse
            return self._execute_block(branch, globals_scope, locals_scope)

        if isinstance(node, ast.For):
            iterable = self._eval(node.iter, globals_scope, locals_scope)
            iterable_values = list(iterable) if iterable is not None else []
            limit = 200
            for idx, value in enumerate(iterable_values):
                if idx >= limit:
                    break
                self._assign_target(node.target, value, globals_scope, locals_scope)
                self._snapshot(node, f"for_iteration={idx}", locals_scope, globals_scope)
                returned, return_value = self._execute_block(node.body, globals_scope, locals_scope)
                if returned:
                    return True, return_value
            return False, None

        if isinstance(node, ast.While):
            guard = 0
            while bool(self._eval(node.test, globals_scope, locals_scope)):
                if guard >= 200:
                    break
                self._snapshot(node, f"while_iteration={guard}", locals_scope, globals_scope)
                returned, return_value = self._execute_block(node.body, globals_scope, locals_scope)
                if returned:
                    return True, return_value
                guard += 1
            return False, None

        if isinstance(node, ast.FunctionDef):
            self._function_defs[node.name] = node
            self._snapshot(node, "function_definition", locals_scope, globals_scope, title=f"def {node.name}")
            return False, None

        if isinstance(node, ast.Return):
            value = self._eval(node.value, globals_scope, locals_scope) if node.value else None
            locals_scope["__return__"] = value
            self._snapshot(node, "return", locals_scope, globals_scope, title="return")
            return True, value

        if isinstance(node, ast.Pass):
            self._snapshot(node, "pass", locals_scope, globals_scope)
            return False, None

        self._snapshot(node, "node_skipped", locals_scope, globals_scope)
        return False, None

    def _assign_target(
        self,
        target: ast.AST,
        value: Any,
        globals_scope: dict[str, Any],
        locals_scope: dict[str, Any],
    ) -> None:
        if isinstance(target, ast.Name):
            locals_scope[target.id] = value
            return

        if isinstance(target, ast.Subscript):
            container = self._eval(target.value, globals_scope, locals_scope)
            index = self._eval(target.slice, globals_scope, locals_scope)
            try:
                container[index] = value
            except Exception:
                return
            return

        if isinstance(target, (ast.Tuple, ast.List)) and isinstance(value, (list, tuple)):
            for inner_target, inner_value in zip(target.elts, value):
                self._assign_target(inner_target, inner_value, globals_scope, locals_scope)

    def _eval(self, expr: ast.AST | None, globals_scope: dict[str, Any], locals_scope: dict[str, Any]) -> Any:
        if expr is None:
            return None

        if isinstance(expr, ast.Constant):
            return expr.value

        if isinstance(expr, ast.Name):
            if expr.id in locals_scope:
                return locals_scope[expr.id]
            if expr.id in globals_scope:
                return globals_scope[expr.id]
            return self._function_defs.get(expr.id)

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
            fn_name = expr.func.id if isinstance(expr.func, ast.Name) else None
            args = [self._eval(arg, globals_scope, locals_scope) for arg in expr.args]
            kwargs = {
                keyword.arg: self._eval(keyword.value, globals_scope, locals_scope)
                for keyword in expr.keywords
                if keyword.arg is not None
            }

            if fn_name == "print":
                return " ".join(str(item) for item in args)

            if fn_name and fn_name in self._function_defs:
                return self._invoke_user_function(fn_name, args, kwargs, globals_scope, locals_scope)

            fn = self._resolve_callable(expr.func, globals_scope, locals_scope)
            frame = CallFrame(
                function=getattr(fn, "__name__", fn_name or "anonymous"),
                line=getattr(expr, "lineno", 0),
                depth=len(self._call_stack) + 1,
                locals={f"arg_{idx}": value for idx, value in enumerate(args)},
            )
            self._call_history.append(copy.deepcopy(frame))
            self._call_stack.append(frame)
            try:
                return fn(*args, **kwargs)
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

    def _invoke_user_function(
        self,
        name: str,
        args: list[Any],
        kwargs: dict[str, Any],
        globals_scope: dict[str, Any],
        outer_locals: dict[str, Any],
    ) -> Any:
        fn_def = self._function_defs[name]
        function_locals = self._bind_function_arguments(fn_def, args, kwargs, globals_scope, outer_locals)

        frame = CallFrame(
            function=name,
            line=getattr(fn_def, "lineno", 0),
            depth=len(self._call_stack) + 1,
            locals={k: self._clean(v) for k, v in function_locals.items()},
        )
        self._call_history.append(copy.deepcopy(frame))
        self._call_stack.append(frame)
        self._snapshot(fn_def, f"call:{name}", function_locals, globals_scope, title=f"call {name}()")

        try:
            returned, value = self._execute_block(fn_def.body, globals_scope, function_locals)
            if returned:
                return value
            return function_locals.get("__return__")
        finally:
            self._call_stack.pop()

    def _bind_function_arguments(
        self,
        fn_def: ast.FunctionDef,
        args: list[Any],
        kwargs: dict[str, Any],
        globals_scope: dict[str, Any],
        outer_locals: dict[str, Any],
    ) -> dict[str, Any]:
        function_locals: dict[str, Any] = {}
        params = list(fn_def.args.args)
        defaults = [self._eval(default, globals_scope, outer_locals) for default in fn_def.args.defaults]
        default_start = len(params) - len(defaults)

        for index, param in enumerate(params):
            if param.arg in kwargs:
                function_locals[param.arg] = kwargs[param.arg]
            elif index < len(args):
                function_locals[param.arg] = args[index]
            elif index >= default_start:
                function_locals[param.arg] = defaults[index - default_start]
            else:
                function_locals[param.arg] = None

        return function_locals

    def _resolve_callable(
        self, fn_expr: ast.AST, globals_scope: dict[str, Any], locals_scope: dict[str, Any]
    ) -> Any:
        if isinstance(fn_expr, ast.Name):
            if fn_expr.id in locals_scope:
                return locals_scope[fn_expr.id]
            if fn_expr.id in globals_scope:
                return globals_scope[fn_expr.id]
            builtins_scope = globals_scope.get("__builtins__", {})
            if isinstance(builtins_scope, dict) and fn_expr.id in builtins_scope:
                return builtins_scope[fn_expr.id]
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
        if isinstance(op, ast.FloorDiv):
            return left // right
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
        if isinstance(op, ast.FloorDiv):
            return current // delta
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
        if isinstance(op, ast.In):
            return left in right
        if isinstance(op, ast.NotIn):
            return left not in right
        if isinstance(op, ast.Is):
            return left is right
        if isinstance(op, ast.IsNot):
            return left is not right
        return False
