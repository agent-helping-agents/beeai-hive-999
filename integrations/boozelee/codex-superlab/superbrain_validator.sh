#!/bin/bash
mkdir -p "$HOME/my-gemini-cli"
cd "$HOME/my-gemini-cli" || { echo "Failed to navigate to ~/my-gemini-cli"; exit 1; }
SUPERBRAIN_DIR="$HOME/Desktop/superbrain-x/cmd/server"
if [ -d "$SUPERBRAIN_DIR" ]; then
  cd "$SUPERBRAIN_DIR"
  cat > validator.go << 'INNER_EOF'
package main
import (
"fmt"
"github.com/go-playground/validator/v10"
"github.com/gofiber/fiber/v2"
)
type ChaosMatrix [6][3]int
type Request struct {
UserID  string      json:"userId" validate:"required,uuid"
Action  string      json:"action" validate:"required,oneof=spin mutate query"
Payload interface{} json:"payload" validate:"required"
}
func main() {
app := fiber.New()
validate := validator.New()
app.Post("/validate", func(c *fiber.Ctx) error {
var req Request
if err := c.BodyParser(&req); err != nil {
return c.Status(400).SendString("Invalid request")
}
if err := validate.Struct(req); err != nil {
return c.Status(400).SendString(fmt.Sprintf("Validation error: %v", err))
}
return c.SendString("Valid request")
})
app.Listen(":8081")
}
INNER_EOF
go mod tidy
go run validator.go
echo "Validator run at $(date)" >> "$HOME/my-gemini-cli/brain_research_results.txt"
else
echo "Superbrain-x directory not found" >> "$HOME/my-gemini-cli/brain_research_results.txt"
exit 1
fi
cat brain_research_results.txt
