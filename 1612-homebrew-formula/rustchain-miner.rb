class RustchainMiner < Formula
  desc "RustChain blockchain miner"
  homepage "https://rustchain.org"
  url "https://github.com/Scottcjn/rustchain-miner/archive/v1.0.0.tar.gz"
  sha256 "CHANGE_ME"
  license "MIT"

  depends_on "rust" => :build
  depends_on "openssl"

  def install
    system "cargo", "install", *std_cargo_args
  end

  test do
    output = shell_output("#{bin}/rustchain-miner --version")
    assert_match "1.0.0", output
  end
end
