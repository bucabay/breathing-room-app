use crate::{model::Settings, processes, storage, system};
use clap::{Args, Parser, Subcommand, ValueEnum};
use serde_json::json;
use std::sync::atomic::AtomicBool;

/// Public command-line interface for Breathing Room.
///
/// The desktop app remains the default when the binary is launched with no
/// arguments. This module only handles explicit commands, so it can also be
/// built without the `gui` feature for a small CLI-only binary.
#[derive(Parser)]
#[command(
    name = "breathing-room",
    version,
    about = "See what is using your Mac's disk space. Read-only by default.",
    long_about = None,
    arg_required_else_help = true
)]
pub struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Scan folders and report what uses space. Read-only.
    Scan(ScanArgs),
    /// Show app/process groups by memory or CPU. Read-only.
    Apps(AppsArgs),
    /// Show volume capacity and free space. Read-only.
    Disk(DiskArgs),
    /// Run one supported cache cleanup after review.
    Clean(CleanArgs),
}

#[derive(Args)]
struct ScanArgs {
    /// Folders to scan. Must be inside your home folder. Defaults to common home folders.
    #[arg(value_name = "PATH")]
    paths: Vec<String>,
    /// Print the full report as JSON.
    #[arg(long)]
    json: bool,
    /// Maximum rows in each section. Use 0 for all rows.
    #[arg(long, default_value_t = 15)]
    top: usize,
    /// Hide rows smaller than this size, for example 10MB or 1.5GB.
    #[arg(long, value_parser = parse_size)]
    min_size: Option<u64>,
}

#[derive(Args)]
struct AppsArgs {
    /// Print the full report as JSON.
    #[arg(long)]
    json: bool,
    /// Maximum rows. Use 0 for all rows.
    #[arg(long, default_value_t = 20)]
    top: usize,
    /// Sort order for the table.
    #[arg(long, value_enum, default_value_t = AppSort::Memory)]
    sort: AppSort,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, ValueEnum)]
enum AppSort {
    Memory,
    Cpu,
    Name,
}

#[derive(Args)]
struct DiskArgs {
    /// Print the report as JSON.
    #[arg(long)]
    json: bool,
}

#[derive(Args)]
struct CleanArgs {
    /// Cache rule to run: npm, uv, or pip.
    #[arg(value_parser = ["npm", "uv", "pip"])]
    rule: Option<String>,
    /// List the measured cleanup candidates and exit.
    #[arg(long)]
    list: bool,
    /// Execute the cleanup. Without this flag it is a dry run.
    #[arg(long)]
    yes: bool,
    /// Print the result as JSON.
    #[arg(long)]
    json: bool,
}

pub fn run() -> i32 {
    let cli = Cli::parse();
    let result = match cli.command {
        Command::Scan(args) => run_scan(args),
        Command::Apps(args) => run_apps(args),
        Command::Disk(args) => run_disk(args),
        Command::Clean(args) => run_clean(args),
    };
    match result {
        Ok(()) => 0,
        Err(error) => {
            eprintln!("error: {error}");
            1
        }
    }
}

fn run_scan(args: ScanArgs) -> Result<(), String> {
    let mut settings = Settings::default();
    settings.scan_paths = args.paths;
    let report = storage::scan(&settings, &AtomicBool::new(false))?;
    if args.json {
        println!(
            "{}",
            serde_json::to_string_pretty(&report)
                .map_err(|error| format!("Could not encode the report: {error}"))?
        );
        return Ok(());
    }
    print_scan(&report, args.top, args.min_size);
    Ok(())
}

fn print_scan(report: &crate::model::StorageReport, top: usize, min_size: Option<u64>) {
    let floor = min_size.unwrap_or(0);
    let used = report.total_bytes.saturating_sub(report.available_bytes);

    println!(
        "Breathing Room {} - read-only scan\n",
        env!("CARGO_PKG_VERSION")
    );
    println!(
        "Volume     {} total | {} available | {} used",
        format_bytes(report.total_bytes),
        format_bytes(report.available_bytes),
        format_bytes(used)
    );
    println!(
        "Scanned    {} | {} files",
        format_bytes(report.scanned_bytes),
        report.file_count
    );
    if report.partial {
        println!("Coverage   partial - this is a bounded scan, not a full-disk measurement");
    } else {
        println!("Coverage   complete for the requested folders");
    }
    if report.skipped > 0 {
        println!("Skipped    {} unreadable paths", report.skipped);
    }
    if !report.roots.is_empty() {
        println!("\nROOTS");
        for root in report.roots.iter().take(12) {
            println!("  {root}");
        }
        if report.roots.len() > 12 {
            println!("  ... and {} more", report.roots.len() - 12);
        }
    }

    let mut groups: Vec<_> = report
        .groups
        .iter()
        .filter(|group| group.bytes >= floor)
        .collect();
    if top > 0 {
        groups.truncate(top);
    }
    println!("\nTOP GROUPS");
    if groups.is_empty() {
        println!("  No groups matched.");
    } else {
        println!(
            "  {:<10}  {:<14}  {:<24}  {}",
            "SIZE", "CATEGORY", "OWNER", "PROJECT"
        );
        for group in groups {
            println!(
                "  {:<10}  {:<14}  {:<24}  {}",
                format_bytes(group.bytes),
                clip(&group.category, 14),
                clip(&group.owner, 24),
                if group.project.is_empty() {
                    "-".to_string()
                } else {
                    clip(&group.project, 48)
                }
            );
        }
    }

    let candidates: Vec<_> = report
        .candidates
        .iter()
        .filter(|candidate| candidate.bytes >= floor)
        .collect();
    println!("\nCLEANUP CANDIDATES");
    if candidates.is_empty() {
        println!("  No supported cache candidates were measured.");
    } else {
        for candidate in candidates {
            println!(
                "  {:<10}  {}",
                format_bytes(candidate.bytes),
                candidate.name
            );
            println!("  {:<10}  {}", "", candidate.path);
            println!("  {:<10}  {}", "", candidate.method);
            if !candidate.description.is_empty() {
                println!("  {:<10}  {}", "", candidate.description);
            }
            println!();
        }
    }

    let mut large: Vec<_> = report
        .large_files
        .iter()
        .filter(|file| file.bytes >= floor)
        .collect();
    if top > 0 {
        large.truncate(top);
    }
    if !large.is_empty() {
        println!("LARGE FILES");
        for file in large {
            println!("  {:<10}  {}", format_bytes(file.bytes), file.path);
        }
        println!();
    }

    if !report.warnings.is_empty() {
        println!("NOTES");
        for warning in &report.warnings {
            println!("  - {warning}");
        }
    }
}

fn run_apps(args: AppsArgs) -> Result<(), String> {
    let mut groups = processes::groups()?;
    if args.json {
        println!(
            "{}",
            serde_json::to_string_pretty(&groups)
                .map_err(|error| format!("Could not encode app groups: {error}"))?
        );
        return Ok(());
    }

    match args.sort {
        AppSort::Memory => groups.sort_by(|a, b| b.memory_bytes.cmp(&a.memory_bytes)),
        AppSort::Cpu => groups.sort_by(|a, b| {
            b.cpu
                .partial_cmp(&a.cpu)
                .unwrap_or(std::cmp::Ordering::Equal)
        }),
        AppSort::Name => groups.sort_by_key(|group| group.name.to_ascii_lowercase()),
    }
    if args.top > 0 {
        groups.truncate(args.top);
    }

    println!(
        "Breathing Room {} - read-only app groups\n",
        env!("CARGO_PKG_VERSION")
    );
    println!(
        "  {:<34}  {:>10}  {:>7}  {:>5}  {}",
        "APP", "MEMORY", "CPU", "PROCS", "BUNDLE"
    );
    for group in groups {
        println!(
            "  {:<34}  {:>10}  {:>7}  {:>5}  {}",
            clip(&group.name, 34),
            format_bytes(group.memory_bytes),
            format!("{:.1}%", group.cpu),
            group.processes.len(),
            group.bundle_path.as_deref().unwrap_or("-")
        );
    }
    println!("\nSample only. No processes were changed.");
    Ok(())
}

fn run_disk(args: DiskArgs) -> Result<(), String> {
    let (total, available) = system::disk_space()?;
    let used = total.saturating_sub(available);
    let percent = if total == 0 {
        0.0
    } else {
        used as f64 / total as f64 * 100.0
    };
    if args.json {
        println!(
            "{}",
            serde_json::to_string_pretty(&json!({
                "totalBytes": total,
                "usedBytes": used,
                "availableBytes": available,
                "usedPercent": percent,
            }))
            .map_err(|error| format!("Could not encode disk data: {error}"))?
        );
        return Ok(());
    }
    println!(
        "Breathing Room {} - read-only disk report\n",
        env!("CARGO_PKG_VERSION")
    );
    println!("Total      {}", format_bytes(total));
    println!("Used       {} ({:.1}%)", format_bytes(used), percent);
    println!("Available  {}", format_bytes(available));
    Ok(())
}

fn run_clean(args: CleanArgs) -> Result<(), String> {
    let report = storage::scan(&Settings::default(), &AtomicBool::new(false))?;

    if args.list {
        if args.json {
            println!(
                "{}",
                serde_json::to_string_pretty(&report.candidates)
                    .map_err(|error| format!("Could not encode candidates: {error}"))?
            );
        } else {
            println!(
                "Breathing Room {} - measured cleanup candidates\n",
                env!("CARGO_PKG_VERSION")
            );
            if report.candidates.is_empty() {
                println!("No supported cache candidates were measured.");
            } else {
                for candidate in &report.candidates {
                    println!(
                        "  {:<10}  {:<16}  {}",
                        format_bytes(candidate.bytes),
                        candidate.id,
                        candidate.name
                    );
                    println!("  {:<10}  {:<16}  {}", "", "", candidate.path);
                    println!("  {:<10}  {:<16}  {}", "", "", candidate.method);
                    println!();
                }
            }
        }
        return Ok(());
    }

    let rule = args
        .rule
        .ok_or("Choose a rule: npm, uv, or pip. Use --list to inspect measured candidates.")?;
    let candidate = report
        .candidates
        .iter()
        .find(|candidate| candidate.id == rule)
        .ok_or_else(|| {
            format!(
                "No measured {rule} candidate. Run `breathing-room clean --list`; the cache may be absent or the bounded scan may have missed it."
            )
        })?;

    let output = if args.yes {
        Some(storage::cleanup(&rule)?)
    } else {
        None
    };

    if args.json {
        println!(
            "{}",
            serde_json::to_string_pretty(&json!({
                "rule": candidate.id,
                "name": candidate.name,
                "path": candidate.path,
                "bytes": candidate.bytes,
                "method": candidate.method,
                "description": candidate.description,
                "executed": args.yes,
                "output": output,
            }))
            .map_err(|error| format!("Could not encode the result: {error}"))?
        );
        return Ok(());
    }

    println!(
        "Breathing Room {} - cache cleanup\n",
        env!("CARGO_PKG_VERSION")
    );
    println!("Rule       {}", candidate.name);
    println!("Path       {}", candidate.path);
    println!("Measured   {}", format_bytes(candidate.bytes));
    println!("Method     {}", candidate.method);
    println!("Note       {}", candidate.description);
    println!();
    if let Some(output) = output {
        println!("Cleanup finished. The owning tool reported:");
        if output.trim().is_empty() {
            println!("  (no output)");
        } else {
            for line in output.lines().take(40) {
                println!("  {line}");
            }
        }
    } else {
        println!("Dry run. Nothing was changed.");
        println!("Re-run with --yes to execute this exact owning-tool command.");
    }
    Ok(())
}

/// Format an allocated byte count using binary units.
pub fn format_bytes(bytes: u64) -> String {
    const UNITS: [&str; 6] = ["B", "KB", "MB", "GB", "TB", "PB"];
    if bytes < 1024 {
        return format!("{bytes} B");
    }
    let mut value = bytes as f64;
    let mut unit = 0;
    while value >= 1024.0 && unit < UNITS.len() - 1 {
        value /= 1024.0;
        unit += 1;
    }
    if value >= 100.0 {
        format!("{value:.0} {}", UNITS[unit])
    } else if value >= 10.0 {
        format!("{value:.1} {}", UNITS[unit])
    } else {
        format!("{value:.2} {}", UNITS[unit])
    }
}

/// Parse a size such as `512`, `10MB`, `1.5 GB`, or `2GiB`.
///
/// Bare numbers are bytes. K/M/G/T use 1024-based units, matching the table
/// output. This is a display threshold, not a promise of reclaimable space.
pub fn parse_size(input: &str) -> Result<u64, String> {
    let compact: String = input.chars().filter(|c| !c.is_whitespace()).collect();
    if compact.is_empty() {
        return Err("Size cannot be empty".into());
    }
    let split = compact
        .find(|c: char| !(c.is_ascii_digit() || c == '.'))
        .unwrap_or(compact.len());
    let (number, suffix) = compact.split_at(split);
    if number.is_empty() {
        return Err(format!("Size `{input}` needs a number"));
    }
    let value: f64 = number
        .parse()
        .map_err(|_| format!("Size `{input}` is not a number"))?;
    if !value.is_finite() || value < 0.0 {
        return Err(format!("Size `{input}` must be zero or greater"));
    }
    let multiplier = match suffix.to_ascii_uppercase().as_str() {
        "" | "B" => 1.0,
        "K" | "KB" | "KIB" => 1024.0,
        "M" | "MB" | "MIB" => 1024.0_f64.powi(2),
        "G" | "GB" | "GIB" => 1024.0_f64.powi(3),
        "T" | "TB" | "TIB" => 1024.0_f64.powi(4),
        _ => {
            return Err(format!(
                "Size `{input}` has an unknown unit; use B, KB, MB, GB, or TB"
            ))
        }
    };
    Ok((value * multiplier).round() as u64)
}

fn clip(value: &str, max: usize) -> String {
    if value.chars().count() <= max {
        return value.to_string();
    }
    let mut clipped: String = value.chars().take(max.saturating_sub(3)).collect();
    clipped.push_str("...");
    clipped
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn formats_binary_sizes() {
        assert_eq!(format_bytes(0), "0 B");
        assert_eq!(format_bytes(1023), "1023 B");
        assert_eq!(format_bytes(1024), "1.00 KB");
        assert_eq!(format_bytes(1536), "1.50 KB");
        assert_eq!(format_bytes(10 * 1024 * 1024), "10.0 MB");
        assert_eq!(format_bytes(150 * 1024 * 1024), "150 MB");
    }

    #[test]
    fn parses_common_size_suffixes() {
        assert_eq!(parse_size("512").unwrap(), 512);
        assert_eq!(parse_size("10MB").unwrap(), 10 * 1024 * 1024);
        assert_eq!(parse_size("1.5 GB").unwrap(), 1_610_612_736);
        assert_eq!(parse_size("2GiB").unwrap(), 2 * 1024 * 1024 * 1024);
    }

    #[test]
    fn rejects_unknown_or_missing_size_units() {
        assert!(parse_size("").is_err());
        assert!(parse_size("MB").is_err());
        assert!(parse_size("10XB").is_err());
        assert!(parse_size("-1MB").is_err());
    }

    #[test]
    fn clips_long_labels_without_splitting_characters() {
        assert_eq!(clip("short", 10), "short");
        assert_eq!(clip("abcdefghijkl", 8), "abcde...");
    }
}
