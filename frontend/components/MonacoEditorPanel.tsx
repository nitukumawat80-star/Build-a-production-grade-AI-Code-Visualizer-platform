"use client";

import Editor from "@monaco-editor/react";

type Props = {
  language: string;
  code: string;
  onChange: (value: string) => void;
};

export function MonacoEditorPanel({ language, code, onChange }: Props) {
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
      />
    </div>
  );
}
