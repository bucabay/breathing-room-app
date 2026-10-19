//! Run with BREATHING_ROOM_RELEASE_ARCHIVE pointing at the staged updater archive.
//! Uses the same verifier and verification mode as tauri-plugin-updater.
use base64::{engine::general_purpose::STANDARD, Engine};
use minisign_verify::{PublicKey, Signature};

#[test]
#[ignore = "requires a signed release archive; run explicitly before publishing"]
fn release_signature_accepts_original_and_rejects_modified_payload() {
    let path = std::env::var("BREATHING_ROOM_RELEASE_ARCHIVE").expect("Supply the signed updater archive");
    let config: serde_json::Value = serde_json::from_str(include_str!("../update-config.json")).unwrap();
    let key_text = String::from_utf8(STANDARD.decode(config["publicKey"].as_str().unwrap()).unwrap()).unwrap();
    let key = PublicKey::decode(&key_text).unwrap();
    let signature_text = std::fs::read_to_string(format!("{path}.sig")).unwrap();
    let decoded = String::from_utf8(STANDARD.decode(signature_text.trim()).unwrap()).unwrap();
    let signature = Signature::decode(&decoded).unwrap();
    let mut payload = std::fs::read(path).unwrap();
    key.verify(&payload, &signature, true).expect("Published archive must match pinned key");
    let version = format!("version:{}", env!("CARGO_PKG_VERSION"));
    assert!(signature.trusted_comment().split('\t').any(|field| field == version));
    let last = payload.len() - 1;
    payload[last] ^= 1;
    assert!(key.verify(&payload, &signature, true).is_err(), "Modified archive must be rejected");
}
