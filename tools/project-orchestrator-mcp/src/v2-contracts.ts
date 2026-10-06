import { z } from 'zod';

export const text = z.string().trim().min(1).max(4096);
export const sha = z.string().regex(/^[a-f0-9]{40}$/i).transform(v=>v.toLowerCase());
export const id = z.number().int().positive();
export const role = z.enum(['PLANNER','IMPLEMENTER','SECURITY_REVIEWER','QUALITY_REVIEWER']);
export const task = { task_id: text };
export const actor = { actor_id: text, actor_type: z.enum(['HUMAN','ADMIN']) };
export const enrollSchema = z.object({ ...task, risk_class:z.enum(['R0','R1','R2','R3','R4']), authorization_ref:text, activation_commit:sha });
export const assignmentSchema = z.object({ ...task, ...actor, role, agent_id:text, authorization_ref:text,
  status:z.enum(['ASSIGNED','ACTIVE']).default('ACTIVE'), expected_assignment_id:id.nullable().default(null) });
export const specSchema = z.object({ ...task, assignment_id:id, spec_version:text, spec_sha:sha,
  artifact_path:text, authorization_ref:text, status:z.enum(['DRAFT','READY']).default('READY') });
export const freezeSchema = z.object({ ...task, ...actor, spec_version:text, spec_sha:sha,
  approval_ref:text, approval_verification_id:id, expected_frozen_spec_id:id.nullable() });
export const startSchema = z.object({ ...task, implementer_assignment_id:id, spec_sha:sha,
  branch:text, worktree:text, lease_minutes:z.number().int().min(1).max(1440).default(60) });
export const implementationSchema = z.object({ ...task, assignment_id:id, spec_sha:sha, base_sha:sha,
  implementation_sha:sha, evidence_ref:text, expected_current_implementation_evidence_id:id.nullable() });
export const ciSchema = z.object({ ...task, implementation_sha:sha,
  status:z.enum(['PENDING','SUCCESS','FAILURE','CANCELLED','UNKNOWN']), reference:text, source:text, recorded_by:text,
  created_at:z.number().int().nonnegative().optional() });
export const reviewType = z.enum(['SECURITY','QUALITY']);
export const reviewStartSchema = z.object({ ...task, review_type:reviewType, assignment_id:id,
  spec_sha:sha, base_sha:sha, implementation_sha:sha });
export const reviewSubmitSchema = z.object({ review_id:id, assignment_id:id, verdict:z.enum(['PASS','REQUEST_CHANGES','BLOCKED']),
  findings_ref:text, blocking_findings:z.number().int().nonnegative(), evidence_ref:text, artifact_path:text,
  reviewer:text, model_profile:text.optional(), tracked_files_modified:z.boolean() });
export const verificationSchema = z.object({ ...task, ...actor,
  subject_type:z.enum(['HUMAN_AUTHORIZATION','SPECIFICATION','IMPLEMENTATION','CI','SECURITY_REVIEW','QUALITY_REVIEW','PR_BRANCH_STATE','MERGE_RESULT']),
  subject_key:text, applicable_subject_id:id.optional(), decision:z.enum(['ATTEST','REVOKE']),
  verification_level:z.enum(['UNVERIFIED','RECORDED','VERIFIED']), expected_effective_verification_id:id.nullable(),
  recorded_by:text, verifier_type:text.optional(), verifier_id:text.optional(), verification_source:text.optional(),
  verification_reference:text.optional(), verified_at:z.number().int().nonnegative().optional(),
  metadata_json:z.string().refine(v=>{try{JSON.parse(v);return true;}catch{return false;}},'Invalid JSON').optional()
});
export type Enrollment = z.input<typeof enrollSchema>;
export type AssignmentInput = z.input<typeof assignmentSchema>;
export type SpecInput = z.input<typeof specSchema>;
export type FreezeInput = z.input<typeof freezeSchema>;
export type StartInput = z.input<typeof startSchema>;
export type ImplementationInput = z.input<typeof implementationSchema>;
export type CiInput = z.input<typeof ciSchema>;
export type ReviewStartInput = z.input<typeof reviewStartSchema>;
export type ReviewSubmitInput = z.input<typeof reviewSubmitSchema>;
export type VerificationInput = z.input<typeof verificationSchema>;
