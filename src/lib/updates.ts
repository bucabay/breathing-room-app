export interface UpdateCheck {
  configured: boolean;
  currentVersion: string;
  version: string | null;
  notes: string | null;
  installed: boolean;
}
export function updateMessage(result: UpdateCheck | null): string {
  if (!result) return "Check for a newer version of Breathing Room.";
  if (result.installed) return "The update is installed. Restart when you’re ready to use the new version.";
  if (!result.configured) return "Automatic updates aren’t connected to a release feed in this build yet.";
  if (result.version) return "A new version is available. Its signature is verified before installation.";
  return `You’re up to date. Version ${result.currentVersion}.`;
}
