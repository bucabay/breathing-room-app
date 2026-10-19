import { Button } from "./ui/button";

export function AuthProviderButtons({ disabled, onSelect }: { disabled: boolean; onSelect: (provider: "google" | "github") => void }) {
  return <div className="agent-auth-actions auth-provider-buttons">
    <Button type="button" variant="outline" className="agent-provider-button" disabled={disabled} onClick={() => onSelect("google")}>
      <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" data-provider-icon="google">
        <path fill="#4285F4" d="M22.56 12.25c0-.73-.06-1.42-.19-2.09H12v3.96h5.92a5.06 5.06 0 0 1-2.2 3.32v2.76h3.56c2.08-1.92 3.28-4.75 3.28-7.95Z"/>
        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.8l-3.56-2.76c-.98.66-2.24 1.06-3.72 1.06-2.87 0-5.3-1.94-6.17-4.54H2.15v2.84A11 11 0 0 0 12 23Z"/>
        <path fill="#FBBC05" d="M5.83 13.96A6.61 6.61 0 0 1 5.48 12c0-.68.12-1.34.35-1.96V7.2H2.15A11 11 0 0 0 1 12c0 1.78.42 3.47 1.15 4.8l3.68-2.84Z"/>
        <path fill="#EA4335" d="M12 5.5c1.62 0 3.06.56 4.21 1.64l3.15-3.15A10.57 10.57 0 0 0 12 1a11 11 0 0 0-9.85 6.2l3.68 2.84C6.7 7.44 9.13 5.5 12 5.5Z"/>
      </svg>Continue with Google
    </Button>
    <Button type="button" variant="outline" className="agent-provider-button" disabled={disabled} onClick={() => onSelect("github")}>
      <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false" data-provider-icon="github"><path d="M12 .3a12 12 0 0 0-3.79 23.39c.6.11.82-.26.82-.58v-2.04c-3.34.73-4.04-1.42-4.04-1.42-.55-1.39-1.34-1.76-1.34-1.76-1.09-.75.08-.73.08-.73 1.2.08 1.84 1.23 1.84 1.23 1.07 1.83 2.81 1.3 3.49.99.11-.78.42-1.3.76-1.6-2.67-.3-5.47-1.34-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.3-.54-1.53.12-3.18 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.29-1.55 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.77.84 1.24 1.91 1.24 3.22 0 4.6-2.81 5.63-5.49 5.93.43.37.82 1.1.82 2.22v3.29c0 .32.22.69.83.57A12 12 0 0 0 12 .3Z"/></svg>Continue with GitHub
    </Button>
  </div>;
}
