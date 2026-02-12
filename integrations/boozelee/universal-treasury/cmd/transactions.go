package cmd

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/fatih/color"
	"github.com/gorilla/mux"
	"github.com/universal-treasury/cli/pkg/providers/wise"
)

// Transaction represents a payment transaction
type Transaction struct {
	ID            string    `json:"id"`
	Amount        float64   `json:"amount"`
	Currency      string    `json:"currency"`
	SourceAccount string    `json:"source_account"`
	TargetAccount string    `json:"target_account"`
	Status        string    `json:"status"`
	Description   string    `json:"description"`
	CreatedAt     time.Time `json:"created_at"`
	UpdatedAt     time.Time `json:"updated_at"`
}

// PaymentRequest represents a payment request payload
type PaymentRequest struct {
	Amount        float64 `json:"amount"`
	Currency      string  `json:"currency"`
	SourceAccount string  `json:"source_account"`
	TargetAccount string  `json:"target_account"`
	Description   string  `json:"description"`
}

// PaymentResponse represents a payment response
type PaymentResponse struct {
	Success     bool        `json:"success"`
	Transaction Transaction `json:"transaction"`
	Message     string      `json:"message"`
}

// ErrorResponse represents an error response
type ErrorResponse struct {
	Error   string `json:"error"`
	Message string `json:"message"`
}

// In-memory transaction store (for demo purposes)
var transactions = make(map[string]Transaction)

var transactionsCmd = &cobra.Command{
	Use:   "transactions",
	Short: "Manage payment transactions",
	Long:  `Create, list, and manage payment transactions through the Universal Treasury system.`,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Use subcommands to manage transactions:")
		fmt.Println("  transactions create - Create a new payment")
		fmt.Println("  transactions list - List all transactions")
		fmt.Println("  transactions serve - Start API server")
	},
}

var transactionsCreateCmd = &cobra.Command{
	Use:   "create",
	Short: "Create a new payment transaction",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Creating a new payment transaction...")
		// This will be handled by the API
	},
}

var transactionsListCmd = &cobra.Command{
	Use:   "list",
	Short: "List all transactions",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Listing all transactions...")
		// This will be handled by the API
	},
}

var transactionsServeCmd = &cobra.Command{
	Use:   "serve",
	Short: "Start the payment API server",
	Long:  `Start the REST API server for processing payment transactions.`,
	Run: func(cmd *cobra.Command, args []string) {
		startAPIServer()
	},
}

func startAPIServer() {
	green := color.New(color.FgGreen).SprintFunc()
	cyan := color.New(color.FgCyan).SprintFunc()
	
	fmt.Printf("🚀 Starting %s API Server...\n", cyan("Universal Treasury"))
	fmt.Println("🔌 Initializing payment endpoints...")
	
	// Initialize router
	r := mux.NewRouter()
	
	// API endpoints
	r.HandleFunc("/api/v1/health", healthCheckHandler).Methods("GET")
	r.HandleFunc("/api/v1/payments", createPaymentHandler).Methods("POST")
	r.HandleFunc("/api/v1/payments", listPaymentsHandler).Methods("GET")
	r.HandleFunc("/api/v1/payments/{id}", getPaymentHandler).Methods("GET")
	r.HandleFunc("/api/v1/webhooks/wise", wiseWebhookHandler).Methods("POST")
	
	// Add middleware for logging
	r.Use(loggingMiddleware)
	
	// Start server
	port := ":8080"
	fmt.Printf("🌐 Server listening on %s\n", green("http://localhost:"+port))
	fmt.Println("📡 Ready to process payments...")
	
	log.Fatal(http.ListenAndServe(port, r))
}

func healthCheckHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "healthy",
		"service": "universal-treasury-payment-api",
		"version": "1.0.0",
	})
}

func createPaymentHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	
	var paymentReq PaymentRequest
	err := json.NewDecoder(r.Body).Decode(&paymentReq)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	
	// Validate request
	if paymentReq.Amount <= 0 {
		json.NewEncoder(w).Encode(ErrorResponse{
			Error:   "invalid_amount",
			Message: "Amount must be greater than 0",
		})
		return
	}
	
	// Create transaction
	txID := strconv.Itoa(len(transactions) + 1)
	tx := Transaction{
		ID:            txID,
		Amount:        paymentReq.Amount,
		Currency:      paymentReq.Currency,
		SourceAccount: paymentReq.SourceAccount,
		TargetAccount: paymentReq.TargetAccount,
		Status:        "pending",
		Description:   paymentReq.Description,
		CreatedAt:     time.Now(),
		UpdatedAt:     time.Now(),
	}
	
	transactions[txID] = tx
	
	// Simulate payment processing
	go func() {
		time.Sleep(2 * time.Second)
		tx.Status = "processing"
		tx.UpdatedAt = time.Now()
		transactions[txID] = tx
		
		time.Sleep(3 * time.Second)
		tx.Status = "completed"
		tx.UpdatedAt = time.Now()
		transactions[txID] = tx
	}()
	
	json.NewEncoder(w).Encode(PaymentResponse{
		Success:     true,
		Transaction: tx,
		Message:     "Payment created successfully",
	})
}

func listPaymentsHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	
	// Convert map to slice for JSON response
	txList := make([]Transaction, 0, len(transactions))
	for _, tx := range transactions {
		txList = append(txList, tx)
	}
	
	json.NewEncoder(w).Encode(txList)
}

func getPaymentHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	
	vars := mux.Vars(r)
	txID := vars["id"]
	
	tx, exists := transactions[txID]
	if !exists {
		http.NotFound(w, r)
		return
	}
	
	json.NewEncoder(w).Encode(tx)
}

func wiseWebhookHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	
	// Verify webhook signature (in production)
	// signature := r.Header.Get("X-Signature")
	// if !verifyWebhookSignature(signature, r.Body) {
	//     http.Error(w, "Invalid signature", http.StatusUnauthorized)
	//     return
	// }
	
	var webhookData map[string]interface{}
	err := json.NewDecoder(r.Body).Decode(&webhookData)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	
	fmt.Printf("🔔 Received Wise webhook: %+v\n", webhookData)
	
	// Process webhook event
	eventType, ok := webhookData["event_type"].(string)
	if ok {
		switch eventType {
		case "transfer.state-change":
			processTransferStateChange(webhookData)
		case "recipient.created":
			processRecipientCreated(webhookData)
		}
	}
	
	json.NewEncoder(w).Encode(map[string]string{
		"status": "received",
	})
}

func processTransferStateChange(data map[string]interface{}) {
	// Extract transfer ID and state
	transferID := data["transfer_id"].(string)
	state := data["state"].(string)
	
	fmt.Printf("🔄 Transfer %s state changed to: %s\n", transferID, state)
	
	// Update transaction status based on webhook
	for id, tx := range transactions {
		if tx.Description == transferID {
			tx.Status = state
			tx.UpdatedAt = time.Now()
			transactions[id] = tx
			break
		}
	}
}

func processRecipientCreated(data map[string]interface{}) {
	recipientID := data["recipient_id"].(string)
	fmt.Printf("👤 New recipient created: %s\n", recipientID)
}

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		
		// Log request
		fmt.Printf("📥 %s %s %s\n", r.Method, r.URL.Path, r.RemoteAddr)
		
		// Call next handler
		next.ServeHTTP(w, r)
		
		// Log response time
		duration := time.Since(start)
		fmt.Printf("✅ %s %s completed in %v\n", r.Method, r.URL.Path, duration)
	})
}

func init() {
	rootCmd.AddCommand(transactionsCmd)
	transactionsCmd.AddCommand(transactionsCreateCmd)
	transactionsCmd.AddCommand(transactionsListCmd)
	transactionsCmd.AddCommand(transactionsServeCmd)
}