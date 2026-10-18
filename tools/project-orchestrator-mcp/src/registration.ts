import { lstatSync, readFileSync } from 'node:fs';
import { isAbsolute } from 'node:path';

export type RegistrationManifest = {
  manifest_version: 1;
  task_id: string;
  title: string;
  priority: number;
  dependencies: string[];
  authorization_ref: string;
  frozen_until_epoch_ms: number | null;
};

export class RegistrationError extends Error {
  constructor(readonly code: string) { super(code); this.name = 'RegistrationError'; }
}

const TASK_ID = /^[A-Z0-9-]{3,50}$/;
const RECEIPT = /^https:\/\/github\.com\/nshaokiet\/ai-ip-description-generator\/(?:issues|pull)\/[1-9][0-9]*#(?:issuecomment-[1-9][0-9]*|discussion_r[1-9][0-9]*)$/;
const KEYS = ['manifest_version','task_id','title','priority','dependencies','authorization_ref','frozen_until_epoch_ms'];

// JSON.parse silently accepts duplicate names (including escaped-equivalent names).
// Scan every object after JSON syntax validation, comparing decoded key strings.
function rejectDuplicateKeys(raw: string): void {
  let i = 0;
  const space = () => { while (/\s/.test(raw[i] ?? '') && i < raw.length) i++; };
  const quoted = (): string => {
    const start = i++;
    while (i < raw.length) {
      if (raw[i] === '\\') { i += 2; continue; }
      if (raw[i++] === '"') return JSON.parse(raw.slice(start, i)) as string;
    }
    throw new RegistrationError('REGISTRATION_INVALID_MANIFEST');
  };
  const value = (): void => {
    space();
    if (raw[i] === '{') {
      i++; space();
      const seen = new Set<string>();
      while (raw[i] !== '}') {
        const key = quoted();
        if (seen.has(key)) throw new RegistrationError('REGISTRATION_INVALID_MANIFEST');
        seen.add(key); space(); i++; value(); space();
        if (raw[i] !== ',') break;
        i++; space();
      }
      i++;
    } else if (raw[i] === '[') {
      i++; space();
      while (raw[i] !== ']') {
        value(); space();
        if (raw[i] !== ',') break;
        i++; space();
      }
      i++;
    } else if (raw[i] === '"') {
      quoted();
    } else {
      while (i < raw.length && !/[\s,}\]]/.test(raw[i]!)) i++;
    }
  };
  value();
}

export function validateRegistration(value: unknown): RegistrationManifest {
  if (!value || typeof value !== 'object' || Array.isArray(value))
    throw new RegistrationError('REGISTRATION_INVALID_MANIFEST');
  const m = value as Record<string, unknown>;
  if (Object.keys(m).length !== KEYS.length || KEYS.some(k => !Object.hasOwn(m, k)) ||
      m.manifest_version !== 1 || typeof m.task_id !== 'string' || !TASK_ID.test(m.task_id) ||
      typeof m.title !== 'string' || m.title.length === 0 ||
      [...m.title].length > 200 || m.title.trim() !== m.title ||
      /[\u0000-\u001f\u007f-\u009f]/u.test(m.title) ||
      !Number.isSafeInteger(m.priority) || (m.priority as number) < 0 || (m.priority as number) > 100 ||
      !Array.isArray(m.dependencies) || m.dependencies.length > 50 ||
      m.dependencies.some(d => typeof d !== 'string' || !TASK_ID.test(d)) ||
      new Set(m.dependencies).size !== m.dependencies.length || m.dependencies.includes(m.task_id) ||
      typeof m.authorization_ref !== 'string' || m.authorization_ref.length > 2048 ||
      !RECEIPT.test(m.authorization_ref) ||
      !(m.frozen_until_epoch_ms === null ||
        (Number.isSafeInteger(m.frozen_until_epoch_ms) && (m.frozen_until_epoch_ms as number) >= 0)))
    throw new RegistrationError('REGISTRATION_INVALID_MANIFEST');
  return {
    manifest_version: 1, task_id: m.task_id, title: m.title, priority: m.priority as number,
    dependencies: (m.dependencies as string[]).slice().sort(),
    authorization_ref: m.authorization_ref, frozen_until_epoch_ms: m.frozen_until_epoch_ms as number | null
  };
}

export function readRegistrationManifest(file: string): RegistrationManifest {
  try {
    if (!isAbsolute(file)) throw new Error('relative path');
    const stat = lstatSync(file);
    if (!stat.isFile() || stat.size > 65536) throw new Error('not a regular bounded file');
    const raw = new TextDecoder('utf-8', { fatal: true }).decode(readFileSync(file));
    const object: unknown = JSON.parse(raw);
    rejectDuplicateKeys(raw);
    return validateRegistration(object);
  } catch {
    throw new RegistrationError('REGISTRATION_INVALID_MANIFEST');
  }
}
