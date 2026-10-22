# Competitor baseline verification — batch 2

75 records, array indices 75–149. 298 sourced documentary claims.

Outcomes: {'verified': 63, 'blocked': 6, 'partial': 6}. No alias merges, publication approval, app testing, or maintenance claims inferred from reachability.

## Important findings

- Pearcleaner official repository explicitly places development/releases on hold indefinitely; source-available Apache 2.0 + Commons Clause, not unrestricted open source.
- PowerMyMac FoneDog official URL redirects to TechyCub Mac Cleaner; do not merge with iMyMac based on matching label.
- Clean Doctor official Apple app ID now resolves to AI Cleaner Max; Store description documents iPhone/iPad/Mac.
- StorageRader official destination redirects to StorageRadar; directory spelling is not a separate verified vendor.
- Feex says early access opening soon and upcoming Windows product.
- QDirStat official README now includes macOS target and discusses community macOS binaries; do not infer Linux-only from directory.
- Sequoia legacy URL points to Golden Gate Cache Cleaner; insufficient to assert discontinuation or same-version identity.
- Wayne GoldCore prices are placeholders, not a usable amount; current full build described as beta.

## Alias review

Full 150-name comparison produced the candidate groups listed in JSON. Matching names are not identity proof. Pangalin tools and Techtool Lite/Pro are explicitly distinct siblings; Glary products have distinct official product pages. PowerMyMac/iMyMac remains unresolved.

## Outcomes

| Product | Status | Official destination / caveat |
| --- | --- | --- |
| Nix - The Mac Uninstaller | verified | https://www.ideaxecution.com/nix-mac-uninstaller/ License device scope is inconsistent on the page: prose says all Macs, footnote says up to 2. Do not publish unlimited-device pricing. |
| Noah | verified | https://onnoah.app/  |
| Omni Remover 3 | blocked | https://www.minicreo.com/omni-remover/ https://www.minicreo.com/omni-remover/ — TLS certificate failure: NET::ERR_CERT_AUTHORITY_INVALID; webfetch transport error |
| OnyX | blocked | https://www.titanium-software.fr/en/onyx.html https://www.titanium-software.fr/en/onyx.html — ERR_TIMED_OUT; TLS handshake timeout; webfetch timed out |
| Pangalin Space Manager | verified | https://pangalin.com/space-manager/  |
| Pangalin Uninstaller | verified | https://pangalin.com/pangalin-uninstaller/  |
| Pearcleaner | verified | https://github.com/alienator88/Pearcleaner  |
| Peel Cleaner | verified | https://peel.tuguidragos.com/  |
| Plumby | verified | https://plumby.app/  |
| PowerMyMac | partial | https://www.techycub.com/mac-cleaner/ Observed FoneDog PowerMyMac destination redirects to TechyCub Mac Cleaner. Destination facts verified; historical name equivalence and relation to iMyMac PowerMyMac NOT established. Keep identity partial; no merge. |
| PureMac | verified | https://github.com/momenbasel/PureMac#install  |
| Purge | verified | https://purgemac.com/  |
| Quitty | verified | https://quitty.iad1tya.cyou/  |
| Radix | verified | https://tryradix.app/  |
| RemoveMacAI | verified | https://omlahore.github.io/RemoveMacAI/  |
| Roomy for Mac | verified | https://roomymac.com/  |
| Sensei | verified | https://cindori.com/sensei?atp=alternativeto  |
| Sequoia Cache Cleaner | partial | https://www.northernsoftworks.com/sequoiacachecleaner.html Official legacy URL offers only a pointer to Golden Gate Cache Cleaner, not baseline Sequoia product documentation. Browser later reset connection. No discontinuation or name-equivalence assertion made. |
| Shiny - Mac App | verified | https://www.theodorehq.com/shiny/  |
| Smart Cleaner AI | verified | https://dijitalworlds.com/maccleaner-ai/  |
| Space Hunter | verified | https://supasecret.com/  |
| SpaceBroom | verified | https://spacebroom.app/en/  |
| StorageRader | verified | https://storageradar.app/  |
| Techtool Lite | verified | https://www.micromat.com/products/techtool-lite/  |
| TechTool Pro | verified | https://www.micromat.com/products/techtool-pro/  |
| TidyBar | verified | https://tidy.bar/  |
| TinkerTool | verified | http://www.bresink.com/osx/TinkerTool.html  |
| Trace for macOS | verified | https://trace.argio.ch/en/  |
| TrashPanda | verified | https://trashpandamacos.vercel.app/  |
| WashAndGo | verified | https://www.abelssoft.de/en/windows/system-utilities/washandgo  |
| WeCleanse | blocked | https://www.minicreo.com/wecleanse/ https://www.minicreo.com/wecleanse/ — TLS certificate failure; NET::ERR_CERT_AUTHORITY_INVALID; webfetch transport error. No security warning bypassed. |
| 4-Organizer Ultra | verified | https://www.ambeteco.com/4-Organizer-Ultra/  |
| Acer Care Center | blocked | https://community.acer.com/en/kb/articles/145-acer-care-center-overview https://community.acer.com/en/kb/articles/145-acer-care-center-overview — HTTP 403 Forbidden; browser Cloudflare security verification in Russian. Stopped at gate. Directory discontinuation flag not verified. |
| Aomei Partition Assistant for Cleanup | verified | https://www.diskpart.com/free-up-pc/  |
| AVG PC TuneUp | verified | https://www.avg.com/en-us/avg-pctuneup  |
| AVS Registry Cleaner | verified | https://www.avs4you.com/avs-registry-cleaner.aspx Directory discontinuation flag is not confirmed: official page still documents a download. A download link alone does not prove maintained development. |
| BleachBit | verified | https://www.bleachbit.org/  |
| Canta | verified | https://samolego.github.io/Canta/  |
| CCleaner Cloud | verified | https://www.ccleanercloud.com/ Official page contains conflicting Windows minimums (Windows 7 and later versus Windows 10/Server 2016 and later). Exact minimum unresolved. |
| Clean Doctor | verified | https://apps.apple.com/us/app/ai-cleaner-max-clean-up-device/id855008026  |
| Clean My Ubuntu | verified | https://github.com/homielab/clean-my-ubuntu  |
| Clean Sweep | verified | https://indiegoodies.com/cleansweep  |
| CleanMyLinux | verified | https://www.cleanmylinux.com/  |
| Cleanup: Phone Storage Cleaner | partial | https://www.codeway.co/ Official directory destination is Codeway corporate homepage; exact Cleanup: Phone Storage Cleaner identity and baseline claims unverified from that source. |
| Click&Clean | verified | https://www.hotcleaner.com/clickclean_chrome.html  |
| DiskUsage | verified | https://github.com/ivanvolosyuk/diskusage  |
| EaseeControl | verified | https://easeecontrol.com/  |
| Eusing Cleaner | verified | https://www.eusing.com/free_system_cleaner/system_cleaner.htm  |
| Express Cleaner | partial | https://ngappstudio.in/ https://ngappstudio.in/ — only “Welcome / Hello from NG App Studio a” returned; no substantive product facts. No pricing/platform inferred. |
| Feex | verified | https://feex.it/  |
| FileCleaner | verified | https://www.filecleaner.com/?sv1=affiliate&sv_campaign_id=577485&sscid=90197_1792609994_fdf604e96e04c58003528ba7b0171b2f&awc=90197_1792609994_fdf604e96e04c58003528ba7b0171b2f  |
| Fortect | verified | https://www.fortect.com/  |
| Glary Disk Cleaner | verified | https://www.glarysoft.com/disk-cleaner/  |
| Glary Utilities | verified | https://www.glarysoft.com/glary-utilities/  |
| Keep-Only-Specified-Extensions | verified | https://cosmic-voyager.com/kose_en/  |
| Moppy - PC Cleaner | partial | https://apps.microsoft.com/detail/9p1ht617vstn?hl=en-US&gl=US https://apps.microsoft.com/detail/9P1HT617VSTN — official Microsoft Store HTML contains only title “Moppy - PC Cleaner - Download and install on Windows”; browser body empty. Not enough for baseline verification. |
| MyCleanPC | verified | https://www.mycleanpc.com/  |
| optimizerDuck | verified | https://optimizerduck.vercel.app/  |
| Outbyte PC Repair | verified | https://outbyte.com/software/pc-repair/  |
| PASPAS | verified | https://github.com/berkaygediz/PASPAS  |
| PC BOOSTER and ANTIVIRUS | verified | https://leaere.itch.io/pc-booster-and-antivirus  |
| PC Clean - Optimal Performance | partial | https://www.microsoft.com/store/apps/9PFG3F32J93L https://www.microsoft.com/store/apps/9PFG3F32J93L — HTTP 403; browser redirects to apps.microsoft.com/detail/9pfg3f32j93l and title, but empty body. Baseline facts unverified; directory discontinued flag not proof. |
| PC Tweaker | verified | https://pctweaker.app/  |
| Photo Sweep & Clean | verified | https://sweepandclean.netlify.app/  |
| PixWash | verified | https://orogenmaker.com/software.php?id=4  |
| QDirStat | verified | https://github.com/shundhammer/qdirstat#ready-made-packages  |
| Sifty | verified | https://sifty.tech/  |
| Sponge - Gallery Cleaner | verified | https://play.google.com/store/apps/details/Sponge_Gallery_Cleaner?id=com.prismtree.sponge&hl=en_US  |
| System Utilities | blocked | https://system-utilities.com/ https://system-utilities.com/ — DNS resolution failed: [Errno 8] nodename nor servname provided, or not known; browser DNS_PROBE_STARTED. No discontinued assertion. |
| TreeSize | verified | https://www.jam-software.com/treesize  |
| Wayne's GoldCore | verified | https://tweakmygame.com/  |
| WhaleClean | verified | https://www.whaleclean.app/  |
| WinCleanCat | verified | https://shaoyidi.github.io/WinCleanCat/  |
| WinExt Free | verified | https://www.trisunsoft.com/we/ Official suite page describes multiple editions. Per-feature Free edition scope and directory discontinuation flag unverified; no maintenance/availability inference from old changelog dates. |
| WinTrim | blocked | https://github.com/kdsmith10000/WinTrim https://github.com/kdsmith10000/WinTrim — HTTP 404 Not Found; browser Page not found · GitHub. This is an inaccessible public repository, not proof of discontinuation. |

## Evidence and limitations

Every claim in `batch-2.json` includes a source URL, normalized source excerpt and actual retrieval UTC. Source ledgers retain requested/final URLs, local raw capture paths and SHA-256. Directory captures establish discovery only. `unverifiedFields` means unknown, never absent. Baseline verified status requires substantive product-specific official content, not a title or HTTP success. Current prices are snapshots; currency codes are not inferred from dollar symbols. Vendor safety/performance language remains documentary attribution, not our test result.

Raw public evidence: `docs/content/.runtime/verification-2/`. No credentials, cookies, API extraction or account-specific data captured. Browser tab 16 was owned by this batch and closed at completion. Manifest, queues, site and other batches were not edited.
