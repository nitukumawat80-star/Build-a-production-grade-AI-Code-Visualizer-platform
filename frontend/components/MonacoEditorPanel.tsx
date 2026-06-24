"use client";

import Editor, { OnMount } from "@monaco-editor/react";
import { useCallback, useEffect, useRef } from "react";

type Props = {
  language: string;
  code: string;
  onChange: (value: string) => void;
  activeLine?: number;
};

export function MonacoEditorPanel({ language, code, onChange, activeLine }: Props) {
  const editorRef = useRef<any>(null);
  const monacoRef = useRef<any>(null);
  const decorationIdsRef = useRef<string[]>([]);

  const updateActiveLine = useCallback(() => {
    if (!editorRef.current || !monacoRef.current) return;

    const line = activeLine && activeLine > 0 ? activeLine : 0;
    if (!line) {
      decorationIdsRef.current = editorRef.current.deltaDecorations(decorationIdsRef.current, []);
      return;
    }

    decorationIdsRef.current = editorRef.current.deltaDecorations(decorationIdsRef.current, [
      {
        range: new monacoRef.current.Range(line, 1, line, 1),
        options: {
          isWholeLine: true,
          className: "dry-run-active-line",
          linesDecorationsClassName: "dry-run-active-line-gutter"
        }
      }
    ]);
  }, [activeLine]);

  const handleMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    updateActiveLine();
  };

  useEffect(() => {
    updateActiveLine();
  }, [updateActiveLine]);

  return (
    <div className="panel rounded-2xl p-3 shadow-soft">
      <Editor
        height="380px"
        language={language === "c++" ? "cpp" : language}
        value={code}
        theme="vs-dark"
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          padding: { top: 16 }
        }}
        onChange={(value) => onChange(value || "")}
        onMount={handleMount}
      />
    </div>
  );
}
