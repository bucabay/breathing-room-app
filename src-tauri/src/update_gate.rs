//! A short exclusive gate for app replacement/restart, not a second cleanup runner.
use std::sync::{RwLock, RwLockReadGuard, RwLockWriteGuard};

struct Gate(RwLock<()>);
static GATE: Gate = Gate(RwLock::new(()));

impl Gate {
    fn operation(&self) -> Result<RwLockReadGuard<'_, ()>, String> {
        self.0.try_read().map_err(|_| "An app update is being installed. Try again after it finishes.".into())
    }
    fn exclusive(&self) -> Result<RwLockWriteGuard<'_, ()>, String> {
        self.0.try_write().map_err(|_| "Wait for storage checks or cleanup to finish before updating or restarting.".into())
    }
}

pub(crate) fn operation() -> Result<RwLockReadGuard<'static, ()>, String> {
    GATE.operation()
}
pub(crate) fn exclusive() -> Result<RwLockWriteGuard<'static, ()>, String> {
    GATE.exclusive()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn update_gate_excludes_new_operations() {
        // Use a local lock so other parallel fixtures are not affected.
        let gate = Gate(RwLock::new(()));
        let operation = gate.operation().unwrap();
        assert!(gate.exclusive().unwrap_err().contains("cleanup"));
        drop(operation);
        let update = gate.exclusive().unwrap();
        assert!(gate.operation().unwrap_err().contains("update"));
        drop(update);
        assert!(gate.operation().is_ok());
    }
}
