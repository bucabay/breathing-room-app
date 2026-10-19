// Deployment-only secret transport. Values arrive on stdin, never in argv/files.
import Foundation
import Security
let args = CommandLine.arguments
guard args.count == 3 else { exit(2) }
let query: [String: Any] = [kSecClass as String: kSecClassGenericPassword, kSecAttrService as String: "app.breathingroom.mac.deploy", kSecAttrAccount as String: args[2]]
if args[1] == "set" {
    let value = FileHandle.standardInput.readDataToEndOfFile()
    guard !value.isEmpty else { exit(2) }
    let changed = SecItemUpdate(query as CFDictionary, [kSecValueData as String:value] as CFDictionary)
    if changed == errSecItemNotFound {
        var add = query; add[kSecValueData as String] = value
        guard SecItemAdd(add as CFDictionary, nil) == errSecSuccess else { exit(1) }
    } else if changed != errSecSuccess { exit(1) }
} else if args[1] == "get" {
    var get = query; get[kSecReturnData as String] = true; get[kSecMatchLimit as String] = kSecMatchLimitOne
    var result: CFTypeRef?
    let status = SecItemCopyMatching(get as CFDictionary, &result)
    if status == errSecItemNotFound { exit(44) }
    guard status == errSecSuccess, let value = result as? Data else { exit(1) }
    FileHandle.standardOutput.write(value)
} else { exit(2) }
