import Link from "next/link";

import { VisualizerShell } from "@/components/VisualizerShell";

export default function HomePage() {
  return (
    <>
      <div className="mx-auto flex max-w-7xl items-center justify-end px-4 pt-4 md:px-8">
        <Link
          href="/dashboard"
          className="rounded-full border border-slate-700 px-4 py-2 text-xs uppercase tracking-[0.2em] text-slate-300 hover:border-pulse/60"
        >
          Premium Dashboard
        </Link>
      </div>
      <VisualizerShell />
    </>
  );
}
