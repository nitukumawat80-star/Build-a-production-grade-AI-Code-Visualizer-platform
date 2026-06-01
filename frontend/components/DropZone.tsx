"use client";

import { UploadCloud } from "lucide-react";

type Props = {
  onCodeDrop: (content: string) => void;
};

export function DropZone({ onCodeDrop }: Props) {
  return (
    <label
      className="flex cursor-pointer items-center justify-center gap-2 rounded-2xl border border-dashed border-slate-600 bg-slate-900/45 p-5 text-sm text-slate-300 transition hover:border-pulse/70"
      onDragOver={(event) => event.preventDefault()}
      onDrop={(event) => {
        event.preventDefault();
        const file = event.dataTransfer.files?.[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => onCodeDrop(String(reader.result || ""));
        reader.readAsText(file);
      }}
    >
      <UploadCloud size={18} className="text-pulse" />
      Drag and drop code file here
      <input
        type="file"
        className="hidden"
        accept=".py,.js,.java,.cpp,.cc,.txt"
        onChange={(event) => {
          const file = event.target.files?.[0];
          if (!file) return;
          const reader = new FileReader();
          reader.onload = () => onCodeDrop(String(reader.result || ""));
          reader.readAsText(file);
        }}
      />
    </label>
  );
}
