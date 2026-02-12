package license

import (
	"fmt"
	"os"
	"strings"
	"sync"
	"time"
)

// Tier represents the license tier
type Tier int

const (
	FreeTier Tier = iota
	ProTier
	EnterpriseTier
)

// License holds the current license state
type License struct {
	Tier      Tier
	Key       string
	DailyRuns int
	MaxRuns   int
	LastReset time.Time
	mu        sync.Mutex
}

var (
	currentLicense *License
	once           sync.Once
)

// FreeTierLimits
const (
	FreeMaxRunsPerDay   = 5
	FreeMaxTokensPerRun = 1000
	ProMaxRunsPerDay    = 100
	ProMaxTokensPerRun  = 10000
	EnterpriseMaxRuns   = -1 // Unlimited
	EnterpriseMaxTokens = -1 // Unlimited
)

// Initialize checks for LICENSE_KEY and sets up the license
func Initialize() *License {
	once.Do(func() {
		key := os.Getenv("LICENSE_KEY")
		currentLicense = &License{
			Key:       key,
			LastReset: time.Now(),
		}

		if key == "" {
			currentLicense.Tier = FreeTier
			currentLicense.MaxRuns = FreeMaxRunsPerDay
			printFreeTierMessage()
		} else if validateKey(key) {
			if strings.HasPrefix(key, "ENT_") {
				currentLicense.Tier = EnterpriseTier
				currentLicense.MaxRuns = EnterpriseMaxRuns
				fmt.Println("✅ Enterprise License activated - Unlimited usage")
			} else {
				currentLicense.Tier = ProTier
				currentLicense.MaxRuns = ProMaxRunsPerDay
				fmt.Println("✅ Pro License activated - 100 runs/day, 10K tokens/run")
			}
		} else {
			currentLicense.Tier = FreeTier
			currentLicense.MaxRuns = FreeMaxRunsPerDay
			fmt.Println("⚠️  Invalid license key. Falling back to Free Tier.")
			printFreeTierMessage()
		}
	})
	return currentLicense
}

// validateKey checks if the license key is valid
// TODO: Connect to Gumroad/LemonSqueezy API for real validation
func validateKey(key string) bool {
	// Stub validation - accepts PRO_ or ENT_ prefixed keys
	if strings.HasPrefix(key, "PRO_") && len(key) >= 20 {
		return true
	}
	if strings.HasPrefix(key, "ENT_") && len(key) >= 20 {
		return true
	}
	return false
}

// CanRun checks if the user can perform another run
func (l *License) CanRun() (bool, string) {
	l.mu.Lock()
	defer l.mu.Unlock()

	// Reset daily counter if new day
	if time.Since(l.LastReset) > 24*time.Hour {
		l.DailyRuns = 0
		l.LastReset = time.Now()
	}

	// Enterprise has unlimited runs
	if l.Tier == EnterpriseTier {
		l.DailyRuns++
		return true, ""
	}

	// Check limits for Free/Pro
	if l.DailyRuns >= l.MaxRuns {
		return false, fmt.Sprintf("Daily limit reached (%d/%d runs). Upgrade at https://bakerstreetproject221B.store/pricing", l.DailyRuns, l.MaxRuns)
	}

	l.DailyRuns++
	return true, ""
}

// GetMaxTokens returns max tokens allowed per run
func (l *License) GetMaxTokens() int {
	switch l.Tier {
	case EnterpriseTier:
		return EnterpriseMaxTokens
	case ProTier:
		return ProMaxTokensPerRun
	default:
		return FreeMaxTokensPerRun
	}
}

// GetTierName returns human-readable tier name
func (l *License) GetTierName() string {
	switch l.Tier {
	case EnterpriseTier:
		return "Enterprise"
	case ProTier:
		return "Pro"
	default:
		return "Free"
	}
}

// GetStatus returns current license status
func (l *License) GetStatus() string {
	l.mu.Lock()
	defer l.mu.Unlock()

	if l.Tier == EnterpriseTier {
		return fmt.Sprintf("License: %s | Runs today: %d | Unlimited", l.GetTierName(), l.DailyRuns)
	}
	return fmt.Sprintf("License: %s | Runs: %d/%d | Tokens/run: %d", l.GetTierName(), l.DailyRuns, l.MaxRuns, l.GetMaxTokens())
}

// GetLicense returns the current license instance
func GetLicense() *License {
	if currentLicense == nil {
		return Initialize()
	}
	return currentLicense
}

func printFreeTierMessage() {
	fmt.Println(`
╔════════════════════════════════════════════════════════════════╗
║                    🔓 FREE TIER ACTIVE                         ║
╠════════════════════════════════════════════════════════════════╣
║  Limits: 5 runs/day • 1,000 tokens/run                         ║
║                                                                ║
║  🚀 Upgrade to Pro: $9/month                                   ║
║     → 100 runs/day • 10K tokens/run • Priority support         ║
║                                                                ║
║  🏢 Enterprise: Contact us for custom limits                   ║
║     → Unlimited runs • Custom integrations • SLA               ║
║                                                                ║
║  ➡️  https://bakerstreetproject221B.store/pricing              ║
║  📧  kiliaan@bakerstreetproject221B.store                      ║
╚════════════════════════════════════════════════════════════════╝
`)
}
