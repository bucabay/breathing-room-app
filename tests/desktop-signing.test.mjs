import test from "node:test";
import assert from "node:assert/strict";
import {chooseSigningIdentity,parseSigningIdentities,stableSignature} from "../scripts/desktop-signing.mjs";

test("local desktop signing reuses the pinned certificate instead of changing identities",()=>{
  const first="A".repeat(40),second="B".repeat(40);
  const identities=parseSigningIdentities(`  1) ${first} "Apple Development: Example (FIRST)"\n  2) ${second} "Apple Development: Example (SECOND)"\n     2 valid identities found\n`);
  assert.equal(identities.length,2);assert.equal(chooseSigningIdentity(identities).hash,first);assert.equal(chooseSigningIdentity(identities,second.toLowerCase()).hash,second);
  assert.throws(()=>chooseSigningIdentity(identities,"C".repeat(40)),/will not silently change identity/);assert.throws(()=>chooseSigningIdentity([]),/No Apple Development/);
});
test("hash-based ad-hoc identities and unbound app identifiers are not considered stable",()=>{
  const signed='Identifier=app.breathingroom.mac\nTeamIdentifier=EXAMPLETEAM\nAuthority=Apple Development\ndesignated => identifier "app.breathingroom.mac" and anchor apple generic and certificate leaf[subject.OU] = "EXAMPLETEAM"';
  assert.equal(stableSignature(signed),true);
  assert.equal(stableSignature(signed.replace('and anchor apple generic','')),false);
  assert.equal(stableSignature('Identifier=breathing_room-hash\nSignature=adhoc\nTeamIdentifier=not set\ndesignated => cdhash H"hash"'),false);
  assert.equal(stableSignature(signed.replace('Identifier=app.breathingroom.mac','Identifier=another.app')),false);
});
