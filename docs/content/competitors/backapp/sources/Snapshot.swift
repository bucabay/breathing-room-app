//
//  Snapshot.swift
//  BackApp
//
//  Created by Markus Lind on 28.02.26.
//

import Foundation

/// Metadata about the device when the snapshot was taken.
struct DeviceInfo: Codable, Sendable {
    let machineName: String
    let macOSVersion: String
    let model: String?

    init(machineName: String, macOSVersion: String, model: String? = nil) {
        self.machineName = machineName
        self.macOSVersion = macOSVersion
        self.model = model
    }

    /// Current device info (machine name and macOS version).
    static var current: DeviceInfo {
        let name = Host.current().localizedName ?? "Mac"
        let os = ProcessInfo.processInfo.operatingSystemVersion
        let version = "\(os.majorVersion).\(os.minorVersion).\(os.patchVersion)"
        return DeviceInfo(machineName: name, macOSVersion: version, model: nil)
    }
}

/// One application entry stored in a snapshot.
struct SnapshotAppItem: Identifiable, Codable, Sendable {
    var id: String { bundleId }

    let bundleId: String
    let displayName: String
    let version: String
    let appStoreURL: String?
    let primaryGenre: String?
    let categoryFromPlist: String?
    let isIOSApp: Bool
    let hasAppStoreReceipt: Bool
    let isSystem: Bool

    init(
        bundleId: String,
        displayName: String,
        version: String,
        appStoreURL: String? = nil,
        primaryGenre: String? = nil,
        categoryFromPlist: String? = nil,
        isIOSApp: Bool = false,
        hasAppStoreReceipt: Bool = false,
        isSystem: Bool = false
    ) {
        self.bundleId = bundleId
        self.displayName = displayName
        self.version = version
        self.appStoreURL = appStoreURL
        self.primaryGenre = primaryGenre
        self.categoryFromPlist = categoryFromPlist
        self.isIOSApp = isIOSApp
        self.hasAppStoreReceipt = hasAppStoreReceipt
        self.isSystem = isSystem
    }
}

/// A saved snapshot of the installed applications at a point in time.
struct Snapshot: Identifiable, Codable, Sendable {
    let id: UUID
    let name: String
    let createdAt: Date
    let deviceInfo: DeviceInfo
    let appCount: Int
    let items: [SnapshotAppItem]

    init(
        id: UUID = UUID(),
        name: String,
        createdAt: Date = Date(),
        deviceInfo: DeviceInfo,
        appCount: Int,
        items: [SnapshotAppItem]
    ) {
        self.id = id
        self.name = name
        self.createdAt = createdAt
        self.deviceInfo = deviceInfo
        self.appCount = appCount
        self.items = items
    }

    /// Builds a snapshot from the current device and a list of installed apps.
    static func make(name: String = "Snapshot", deviceInfo: DeviceInfo, apps: [AppRecord]) -> Snapshot {
        let items = apps.map { app in
            SnapshotAppItem(
                bundleId: app.bundleId,
                displayName: app.displayName,
                version: VersionCompare.displayVersion(for: app),
                appStoreURL: app.appStoreURL,
                primaryGenre: app.primaryGenre,
                categoryFromPlist: app.categoryFromPlist,
                isIOSApp: app.isIOSApp,
                hasAppStoreReceipt: app.hasAppStoreReceipt,
                isSystem: app.isSystem
            )
        }
        return Snapshot(name: name, deviceInfo: deviceInfo, appCount: items.count, items: items)
    }
}

/// Versioned container for snapshot export.
struct SnapshotExportFile: Codable {
    static let currentFormatVersion = 1
    let formatVersion: Int
    let snapshot: Snapshot

    init(snapshot: Snapshot, formatVersion: Int = Self.currentFormatVersion) {
        self.formatVersion = formatVersion
        self.snapshot = snapshot
    }
}
