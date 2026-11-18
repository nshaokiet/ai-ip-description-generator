"""Deterministic Python/Node shared-gate tests, on both native CI platforms."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import threading
import time
from types import SimpleNamespace

from fastapi.responses import Response
import pytest

from backend.app.services.product_web_host_control import restrict_owned
from backend.app.services.product_web_publication import PublicationGate, PublicationError

ROOT = Path(__file__).resolve().parents[2]
MODULE = (ROOT / "frontend/tools/product-web-publication.mjs").as_uri()
SCRIPT = """
import fs from 'node:fs';
const input = JSON.parse(fs.readFileSync(0,'utf8'));
const {publish} = await import(input.module);
const response = {destroyed:false,headersSent:false,outputSize:0,socket:{writable:!input.blocked,destroyed:false},
  writeHead(status) {this.headersSent=true;},
  end(body) {
    if (input.entered) {
      fs.writeFileSync(input.entered,'1');
      const end=performance.now()+2000;
      while (!fs.existsSync(input.release) && performance.now()<end)
        Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,5);
      if (!fs.existsSync(input.release)) throw new Error('test_barrier_timeout');
    }
    this.bytes=body.length;
    if(input.buffered) this.outputSize=body.length;
  },destroy() {this.destroyed=true;}};
let outcomes=[];
for (let index=0;index<(input.repeat??1);index++) {
  try {
    await publish(input.host,input.receipt,input.request,response,Buffer.from(input.body),200,
      {'Content-Type':'application/json'},0,{clock:()=>input.now??0});
    outcomes.push({published:true,bytes:response.bytes});
  } catch(error) {outcomes.push({published:false,code:error.message,...(input.buffered?{destroyed:response.destroyed}:{})});}
  response.headersSent=false;
}
console.log(JSON.stringify(outcomes));
"""


@pytest.fixture
def channel(tmp_path):
    restrict_owned(tmp_path)
    gate = PublicationGate(tmp_path)
    item = SimpleNamespace(owner="b" * 64, token="synthetic-session", selector="c" * 32,
                           ref=SimpleNamespace(revision=1))
    response = Response(b'{"synthetic":true}', media_type="application/json")
    path = f"/api/product-web/v1/documents/{item.selector}/review"
    gate.issue(item, 0, 1, "review", path, 120000, response, lambda: None)
    data = {"module": MODULE, "host": {"publication": {"root": str(gate.root), "instance": gate.instance}},
            "receipt": response.headers["x-aiip-publication"],
            "request": {"method": "GET", "url": path, "headers": {"cookie": "__Host-aiip_web=" + item.token}},
            "body": response.body.decode()}
    return gate, item, data


def node(data):
    result = subprocess.run(["node", "--input-type=module", "-e", SCRIPT], input=json.dumps(data),
                            text=True, capture_output=True, timeout=5, check=True)
    assert not result.stderr
    return json.loads(result.stdout)


@pytest.mark.parametrize("reason", ["logout", "cancel", "expiry", "operator", "shutdown"])
def test_revoke_before_node_gate_denies_private_buffer(channel, reason):
    gate, item, data = channel
    gate.invalidate([item.owner], close=reason == "shutdown")
    assert node(data)[0]["published"] is False


def test_committed_publication_is_single_use_and_revoke_does_not_recall(channel):
    gate, item, data = channel
    result = node({**data, "repeat": 2})
    assert result == [{"published": True, "bytes": len(data["body"])},
                      {"published": False, "code": "authority_revoked"}]
    gate.invalidate([item.owner])
    assert not json.loads(gate.path.read_text())["receipts"]


@pytest.mark.parametrize("tamper", ["owner", "document", "revision", "epoch", "action", "digest", "deadline", "instance", "path", "operation"])
def test_bound_identity_payload_and_deadline_fail_closed(channel, tamper):
    gate, _, data = channel
    if tamper == "owner":
        data["request"]["headers"]["cookie"] = "__Host-aiip_web=other-owner"
    elif tamper == "instance":
        data["host"]["publication"]["instance"] = "d" * 64
    elif tamper == "deadline":
        data["now"] = 120000
    elif tamper == "digest":
        data["body"] = "different synthetic output"
    elif tamper == "path":
        data["request"]["url"] += "?forged=1"
    else:
        with gate.transaction() as state:
            grant = state["receipts"][data["receipt"]]
            grant[tamper] = {"document": "e"*32,"revision":0,"epoch":-1,
                             "action":"render","operation":0}[tamper]
    assert node(data)[0]["published"] is False


def test_receipt_substitution_for_artifact_revision_is_denied(channel):
    gate, _, data = channel
    with gate.transaction() as state:
        grant = state["receipts"][data["receipt"]]
        path = grant["path"].replace("/review", "/revisions/2/artifacts/USPTO_APPLICATION_DRAFT.pdf")
        grant.update(path=path, action="download")
        data["request"]["url"] = path
    assert node(data)[0]["published"] is False


def test_ipc_timeout_and_crashed_gate_owner_never_publish(channel, monkeypatch):
    gate, item, data = channel
    gate.latch.mkdir()
    try:
        assert node(data) == [{"published":False,"code":"publication_unavailable"}]
        import backend.app.services.product_web_publication as module
        monkeypatch.setattr(module,"WAIT_SECONDS",0.02)
        with pytest.raises(PublicationError): gate.invalidate([item.owner])
        assert gate.failed
    finally:
        gate.latch.rmdir()
    with pytest.raises(PublicationError): gate.invalidate([item.owner])
    assert node(data)[0]["published"] is False  # Failure marker survives peer recovery.


@pytest.mark.parametrize("state",["blocked","buffered"])
def test_transport_backpressure_never_leaves_private_http_output_queued(channel,state):
    _,_,data=channel
    result=node({**data,state:True})[0]
    assert not result["published"]
    if state=="buffered": assert result["destroyed"]


@pytest.mark.parametrize("failure", ["missing", "corrupt", "closed"])
def test_peer_state_failure_denies(channel, failure):
    gate, _, data = channel
    if failure == "missing": gate.path.unlink()
    elif failure == "corrupt": gate.path.write_text("{",encoding="utf-8")
    else: gate.invalidate(close=True)
    assert node(data)[0]["published"] is False


def test_revoke_cannot_ack_while_node_transport_commit_holds_gate(channel, tmp_path):
    gate, item, data = channel
    entered, release = tmp_path/"entered", tmp_path/"release"
    data.update(entered=str(entered),release=str(release))
    with ThreadPoolExecutor(max_workers=2) as pool:
        publishing = pool.submit(node,data)
        end=time.monotonic()+3
        while not entered.exists() and time.monotonic()<end: time.sleep(0.005)
        assert entered.exists() and gate.latch.is_dir()
        started=threading.Event()
        def revoke():
            started.set()
            gate.invalidate([item.owner])
        revoking=pool.submit(revoke)
        assert started.wait(1)
        assert not revoking.done()  # Node's commit gate still belongs to Node.
        release.write_text("1")
        assert publishing.result(timeout=3)[0]["published"]
        revoking.result(timeout=3)
    assert node(data)[0]["published"] is False


def test_invalidation_holds_gate_before_node_can_publish(channel):
    gate, item, data = channel
    with ThreadPoolExecutor(max_workers=1) as pool:
        with gate.transaction() as state:
            state["receipts"] = {}
            pending=pool.submit(node,data)
            # Python owns the directory until invalidation is written and closed.
            assert gate.latch.is_dir()
        assert pending.result(timeout=3)[0]["published"] is False


def test_two_owners_bounded_and_receipts_contain_no_private_credentials(channel):
    gate, item, data = channel
    second=SimpleNamespace(**{**item.__dict__,"owner":"f"*64,"token":"second-session"})
    gate.issue(second,2,3,"review",data["request"]["url"],120000,
               Response(b"{}",media_type="application/json"),lambda:None)
    state=json.loads(gate.path.read_text())
    assert len(state["receipts"])==2
    assert item.token not in gate.path.read_text() and second.token not in gate.path.read_text()
    gate.invalidate([item.owner])
    assert len(json.loads(gate.path.read_text())["receipts"])==1


@pytest.mark.parametrize("when", ["before_first", "between_fences", "after_complete"])
def test_asgi_response_start_denial_has_no_replacement_or_unhandled_error(when):
    import asyncio
    from backend.app.api.product_web_synthetic import PublicationFence
    from backend.app.services.product_web_bridge import BridgeError
    revoked, sent = False, []
    def fence():
        if revoked: raise BridgeError(401,"authority_revoked")
    async def app(scope,receive,send):
        nonlocal revoked
        scope["state"]["s2_fence"]=fence
        await send({"type":"http.response.start","status":200,"headers":[]})
        if when=="before_first": revoked=True
        await send({"type":"http.response.body","body":b"synthetic protected data"})
    async def transport(message):
        nonlocal revoked
        sent.append(message)
        if when=="between_fences" and message["type"]=="http.response.start": revoked=True
    async def receive(): return {"type":"http.disconnect"}
    asyncio.run(PublicationFence(app)({"type":"http","path":"/api/product-web/v1/documents","state":{}},receive,transport))
    starts=[m["status"] for m in sent if m["type"]=="http.response.start"]
    assert starts==([401] if when=="before_first" else [200])
    assert any(m.get("body")==b"synthetic protected data" for m in sent)==(when=="after_complete")


def test_h11_backpressure_cannot_bypass_final_node_gate(channel):
    import asyncio
    import h11
    import logging
    from uvicorn.protocols.http.h11_impl import RequestResponseCycle
    from uvicorn.protocols.http.flow_control import FlowControl
    from backend.app.api.product_web_synthetic import PublicationFence
    from backend.app.services.product_web_bridge import BridgeError
    gate,item,data=channel
    async def exercise():
        revoked,writes,checks=False,[],[]
        draining=asyncio.Event()
        class Transport:
            def write(self,body):
                writes.append(body)
                if len(writes)==1: flow.pause_writing()
            def close(self): pass
        class Flow(FlowControl):
            async def drain(self):
                draining.set()
                await super().drain()
        transport=Transport()
        flow=Flow(transport)
        conn=h11.Connection(h11.SERVER)
        conn.receive_data(b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        conn.next_event(); conn.next_event()
        scope={"type":"http","method":"GET","path":data["request"]["url"],"headers":[],"state":{}}
        cycle=RequestResponseCycle(scope,conn,transport,flow,logging.getLogger("test"),
            logging.getLogger("test"),False,[],asyncio.Event(),lambda:None)
        def fence():
            checks.append(revoked)
            if revoked: raise BridgeError(401,"authority_revoked")
        async def app(scope,receive,send):
            scope["state"]["s2_fence"]=fence
            await send({"type":"http.response.start","status":200,
                        "headers":[(b"content-length",str(len(data["body"])).encode())]})
            await send({"type":"http.response.body","body":data["body"].encode()})
        pending=asyncio.create_task(PublicationFence(app)(scope,cycle.receive,cycle.send))
        await asyncio.wait_for(draining.wait(),2)
        assert checks==[False,False] and not cycle.response_complete
        gate.invalidate([item.owner])
        revoked=True
        flow.resume_writing()
        await asyncio.wait_for(pending,2)
        assert cycle.response_complete  # Private Python->Node delivery may finish.
    asyncio.run(exercise())
    assert node(data)==[{"published":False,"code":"authority_revoked"}]
