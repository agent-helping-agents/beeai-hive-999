package license

import (
	"os"
	"sync"
	"testing"
)

func resetLicense() {
	currentLicense = nil
	once = sync.Once{}
}

func TestValidateKey(t *testing.T) {
	tests := []struct {
		name     string
		key      string
		expected bool
	}{
		{"Valid Pro Key", "PRO_1234567890123456", true},
		{"Valid Enterprise Key", "ENT_1234567890123456", true},
		{"Invalid Prefix", "FREE_1234567890123456", false},
		{"Too Short Pro", "PRO_123", false},
		{"Empty Key", "", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := validateKey(tt.key)
			if result != tt.expected {
				t.Errorf("validateKey(%s) = %v, want %v", tt.key, result, tt.expected)
			}
		})
	}
}

func TestFreeTierLimits(t *testing.T) {
	resetLicense()
	os.Unsetenv("LICENSE_KEY")

	license := Initialize()

	if license.Tier != FreeTier {
		t.Errorf("Expected FreeTier, got %v", license.Tier)
	}

	// Should allow 5 runs
	for i := 0; i < 5; i++ {
		canRun, msg := license.CanRun()
		if !canRun {
			t.Errorf("Run %d should be allowed: %s", i+1, msg)
		}
	}

	// 6th run should fail
	canRun, _ := license.CanRun()
	if canRun {
		t.Error("6th run should be blocked on free tier")
	}
}

func TestProTierLimits(t *testing.T) {
	resetLicense()
	os.Setenv("LICENSE_KEY", "PRO_12345678901234567890")
	defer os.Unsetenv("LICENSE_KEY")

	license := Initialize()

	if license.Tier != ProTier {
		t.Errorf("Expected ProTier, got %v", license.Tier)
	}

	if license.GetMaxTokens() != ProMaxTokensPerRun {
		t.Errorf("Expected %d tokens, got %d", ProMaxTokensPerRun, license.GetMaxTokens())
	}
}

func TestEnterpriseTier(t *testing.T) {
	resetLicense()
	os.Setenv("LICENSE_KEY", "ENT_12345678901234567890")
	defer os.Unsetenv("LICENSE_KEY")

	license := Initialize()

	if license.Tier != EnterpriseTier {
		t.Errorf("Expected EnterpriseTier, got %v", license.Tier)
	}

	// Enterprise should have unlimited runs
	for i := 0; i < 1000; i++ {
		canRun, _ := license.CanRun()
		if !canRun {
			t.Errorf("Enterprise run %d should be allowed", i+1)
			break
		}
	}
}

func TestGetTierName(t *testing.T) {
	tests := []struct {
		tier     Tier
		expected string
	}{
		{FreeTier, "Free"},
		{ProTier, "Pro"},
		{EnterpriseTier, "Enterprise"},
	}

	for _, tt := range tests {
		l := &License{Tier: tt.tier}
		if got := l.GetTierName(); got != tt.expected {
			t.Errorf("GetTierName() = %v, want %v", got, tt.expected)
		}
	}
}
