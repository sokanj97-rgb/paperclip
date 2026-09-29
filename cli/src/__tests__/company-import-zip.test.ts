import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { resolveInlineSourceFromPath } from "../commands/client/company.js";
import { createStoredZipArchive } from "./helpers/zip.js";

const tempDirs: string[] = [];

afterEach(async () => {
  for (const dir of tempDirs.splice(0)) {
    await rm(dir, { recursive: true, force: true });
  }
});

describe("resolveInlineSourceFromPath", () => {
  it("imports portable files from a zip archive instead of scanning the parent directory", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "paperclip-company-import-zip-"));
    tempDirs.push(tempDir);

    const archivePath = path.join(tempDir, "paperclip-demo.zip");
    const archive = createStoredZipArchive(
      {
        "COMPANY.md": "# Company\n",
        ".paperclip.yaml": "schema: paperclip/v1\n",
        "agents/ceo/AGENT.md": "# CEO\n",
        "notes/todo.txt": "ignore me\n",
      },
      "paperclip-demo",
    );
    await writeFile(archivePath, archive);

    const resolved = await resolveInlineSourceFromPath(archivePath);

    expect(resolved).toEqual({
      rootPath: "paperclip-demo",
      files: {
        "COMPANY.md": "# Company\n",
        ".paperclip.yaml": "schema: paperclip/v1\n",
        "agents/ceo/AGENT.md": "# CEO\n",
      },
    });
  });

  it("keeps skill scripts and references from a package directory", async () => {
    const tempDir = await mkdtemp(path.join(os.tmpdir(), "paperclip-company-import-dir-"));
    tempDirs.push(tempDir);

    const files: Record<string, string> = {
      "COMPANY.md": "# Company\n",
      "skills/render/SKILL.md": "# Render\n",
      "skills/render/scripts/render.py": "print('hi')\n",
      "skills/render/references/recipe.json": "{}\n",
      "notes/todo.txt": "ignore me\n",
    };
    for (const [relativePath, content] of Object.entries(files)) {
      await mkdir(path.dirname(path.join(tempDir, relativePath)), { recursive: true });
      await writeFile(path.join(tempDir, relativePath), content);
    }

    const resolved = await resolveInlineSourceFromPath(tempDir);

    expect(resolved.files).toEqual({
      "COMPANY.md": "# Company\n",
      "skills/render/SKILL.md": "# Render\n",
      "skills/render/scripts/render.py": "print('hi')\n",
      "skills/render/references/recipe.json": "{}\n",
    });
  });
});
