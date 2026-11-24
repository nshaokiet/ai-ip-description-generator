"""Opt-in disposable-checkout contract probe, NOT website/runtime integration.
Run only with the four exact candidate modules copied into a disposable checkout.
No candidate imports are added to accepted-main backend runtime or pytest discovery.
P0_SOURCE_PROBE_OUTPUT must name a fresh owned test output directory.
Authorizer callbacks below are TEST DOUBLES, never Human/session authority.
"""
import subprocess
from pathlib import Path
PINNED = {
 "confidentiality.py": "3f34217638c0ed1fcf7e91b74fa47b163fa1cd96",
 "manual_prior_art.py": "5a8abca89889433f99199b1ca0c6a687f64433b6",
 "document_assets.py": "e6ed73a702e8a9fbf9126ca1a651f2e3e57d57fb",
 "business_document_outputs.py": "87b39dc8e0bd6241cfea5dc2e7912255bba178f1",
}
for filename, commit in PINNED.items():
 path = "backend/app/services/" + filename
 expected = subprocess.check_output(["git", "show", commit + ":" + path])
 assert Path(path).read_bytes().replace(b"\r\n", b"\n") == expected, path
from pathlib import Path
from types import SimpleNamespace
from dataclasses import replace
from datetime import datetime, timezone, timedelta
import json, hashlib, os
from fastapi.testclient import TestClient
from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.custody_review import review_documents
from backend.app.services.product_synthetic_workflow import OfflineSyntheticWorkflow
from backend.app.services.uspto_document_package import assemble_uspto_document_package
from backend.app.services.confidentiality import SourceRevision, OfflineConfidentialityGate
from backend.app.services.manual_prior_art import ManualPriorArtWorkflow, ManualSearchRecord, PriorArtError
from backend.app.services.business_document_outputs import render_business_document_set
from backend.app.services.document_assets import DocumentAssetInspector, AssetInspectionError
from tests.backend.test_product_synthetic_workflow import SourceCheckingRuntime, IDENTITIES, B_IDENTITY, register
from tests.e2e.provider_tripwire import ProviderTripwire

out=Path(os.environ["P0_SOURCE_PROBE_OUTPUT"]).resolve()
out.mkdir(parents=True,exist_ok=True)
results=[]
with ProviderTripwire() as tripwire:
 for index,name in enumerate(("controller.pdf","research-b.docx"),1):
  case=out/f"source-{index}";case.mkdir()
  app=create_app(Settings(storage_root=case/"uploads"))
  owner,actor,context="test_owner","contract_actor","test_only_context"
  authorize=lambda action: action.owner==owner and action.actor==actor and action.context==context
  prior=ManualPriorArtWorkflow(app.state.document_storage,app.state.document_registry,authorizer=authorize)
  assets=DocumentAssetInspector(app.state.document_storage,app.state.document_registry,app.state.document_preparation_service,app.state.document_validator,authorizer=authorize)
  consent=OfflineConfidentialityGate(authorizer=authorize)
  product=OfflineSyntheticWorkflow(app.state.document_storage,app.state.document_registry,
   app.state.document_preparation_service,output_root=case/"custody",extraction_runtime=SourceCheckingRuntime(),
   fixtures=IDENTITIES+(B_IDENTITY,),authorize_invocation=lambda:True,
   review_authorizer=lambda *args:False,enabled=True)
  principal=dict(owner=owner,actor=actor,context=context)
  with TestClient(app) as client:
   host=SimpleNamespace(app=app,client=client)
   doc,payload=register(host,name)
   sha=hashlib.sha256(payload).hexdigest()
   source=SourceRevision(doc,sha,1)
   envelope=app.state.document_preparation_service.prepare_extraction_input(doc).model_dump(exclude_none=True,mode="json")
   consent.classify(source,classification="CONFIDENTIAL",**principal)
   scope=dict(owner=owner,destination="test_provider",purpose="SCIENTIFIC_ANALYSIS")
   consent.grant(source,envelope,expires_at=datetime.now(timezone.utc)+timedelta(minutes=5),
    actor=actor,context=context,**scope)
   assert consent.check(source,envelope,**scope).allowed
   changed=dict(envelope,contract_probe_extra="changed")
   assert not consent.check(source,changed,**scope).allowed
   consent.revoke(source,**principal);assert not consent.check(source,envelope,**scope).allowed
   entry=ManualSearchRecord("Synthetic manual contract probe only","No real prior-art search performed")
   dossier=prior.save(doc,entry,expected_revision=0,reason="TEST_AUTHORIZER_ONLY",**principal)
   prior.decide(doc,expected_revision=1,choice="CONTINUE",reason="TEST_AUTHORIZER_ONLY",**principal)
   assert prior.assess_drafting(doc,expected_revision=1,**principal).allowed
   prior.decide(doc,expected_revision=1,choice="STOP",reason="TEST_ONLY_STOP",**principal)
   assert not prior.assess_drafting(doc,expected_revision=1,**principal).allowed
   prior.decide(doc,expected_revision=1,choice="CONTINUE",reason="TEST_ONLY_CONTINUE",**principal)
   prior.save(doc,replace(entry,limitations="Changed synthetic limits"),expected_revision=1,reason="TEST_ONLY_CHANGE",**principal)
   assert not prior.assess_drafting(doc,expected_revision=2,**principal).allowed
   try:prior.assess_drafting(doc,expected_revision=1,**principal)
   except PriorArtError as error:assert error.code=="STALE_DOSSIER_REVISION"
   else:raise AssertionError("stale dossier accepted")
   inspection=assets.inspect(doc,**principal)
   asset_source_sha=inspection.source_sha256
   del inspection  # Carry no raw image-byte object across C1 deletion.
   ref=product.start(doc)
   assert app.state.document_registry.get(doc) is None
   assert not app.state.document_storage.path_for(doc).exists()
   originals=review_documents(product.review(ref).originals)
   package=assemble_uspto_document_package(**originals)
   assert sha==dossier.source_sha256==asset_source_sha==package["source_identity"]["source_sha256"]==source.source_sha256
   for service,operation in (("P0-PRIOR",lambda:prior.assess_drafting(doc,expected_revision=2,**principal)),("P0-ASSETS",lambda:assets.inspect(doc,**principal))):
    try:operation()
    except (PriorArtError,AssetInspectionError) as error:
     assert error.code=="SOURCE_UNAVAILABLE_OR_CHANGED"
     print("POST_DELETE",name,service,error.code)
    else:raise AssertionError("consumed raw source unexpectedly accepted")
   export=case/"exports";export.mkdir()
   files=render_business_document_set(package,**originals,output_dir=export)
   assert len(files)==7
   manifest=json.loads(files["BUSINESS_OUTPUT_MANIFEST.json"].read_text())
   assert manifest["source_identity"]["source_sha256"]==sha
   assert manifest["review_status"]=="UNREVIEWED" and not manifest["filing_ready"]
   results.append(dict(source=name,source_sha256=sha,all_component_hashes_match=True,
    consent_payload_change_and_revoke_denied=True,prior_revision_change_invalidated=True,
    raw_source_consumed_by_existing_C1=True,post_consumption_prior_and_assets_fail_closed=True,
    business_export_files=6,manifest_files=1,source_analysis="MOCK_VALIDATED_AGAINST_ADMITTED_SOURCE",
    authorizer="TEST_ONLY_NOT_HUMAN_APPROVAL",website_integration=False,independent_review=False))
 tripwire.assert_no_unexpected_activity();counters=tripwire.snapshot();assert all(v==0 for v in counters.values())
summary=dict(status="BOUNDED_CONTRACT_PROBE_ONLY",mvp_ready=False,
 blocker="SOURCE_LIFECYCLE_HANDOFF_NOT_VERIFIED",explanation="Existing C1 consumes raw upload at start; manual evidence/assets need registered bytes. Future consumer needs reviewed custody handoff/sequencing, no silent retention extension.",provider_counters=counters,cases=results)
(out.parent/"cross-contract-result.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))
