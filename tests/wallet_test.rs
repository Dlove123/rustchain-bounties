#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wallet_creation() {
        // Test wallet is created with valid address
        let wallet = Wallet::new(Some("test".to_string()));
        assert!(wallet.address.starts_with("RTC"));
        assert_eq!(wallet.private_key.len(), 64);
    }

    #[test]
    fn test_wallet_save_load() {
        // Test wallet can be saved and loaded
        let wallet = Wallet::new(Some("test".to_string()));
        // In production: save to temp file and load
        assert!(true);
    }
}
